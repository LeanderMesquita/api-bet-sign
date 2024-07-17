from time import sleep
from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from api.index import Starter
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.logger.index import log
from flask_cors import CORS
import threading
import threading

app = Flask(__name__)
CORS(app)

def process_in_chunks(df):
    starter = Starter()
    chunk_size = 5
    threads = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size].copy()  # Garantir que estamos passando uma cópia do dataframe
        print(f'Processing chunk:\n{chunk}\nTipo: {type(chunk)}')  # Log para verificar o chunk
        thread = threading.Thread(target=starter.start_injection, args=(chunk, 'dataframe_injection'))
        threads.append(thread)
        thread.start()

        # Join threads to limit simultaneous browser instances to 5
        if len(threads) >= chunk_size:
            for t in threads:
                t.join()
            threads = []

    # Join remaining threads
    for t in threads:
        t.join()

@app.route('/unique-register', methods=['POST'])
def unique_registering():
    data = request.get_json()
    if data:
        log.info('Starting single injection via JSON.')
        starter = Starter()
        starter.start_JSON_injection(data)
        return jsonify({'message': 'JSON successfully loaded and processed'}), 200
    return jsonify({'message': 'ERROR: JSON not loaded'}), 400

@app.route('/upload-file', methods=['POST'])
def upload_file():
    headless_option = request.form['headless']
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        log.info(f'Recieved file: {filename}')
        log.debug(f'Headless option == {headless_option}')
        df = read_dataframe(file)
        log.debug(f'The current dataframe has {len(df)} rows')
        process_in_chunks(df, headless_option)
        return jsonify({'message': 'File successfully uploaded and processed'}), 200


def process_in_chunks(df, headless, num_workers:int = 3):
    if len(df) < num_workers:
        num_workers = len(df)
    starter = Starter()
    chunk_size = int(len(df) / num_workers)
    threads = []
    thread_id = 1

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size].copy()  
        log.warning(f'initiating thread n-{thread_id}')
        log.info(f'chunk has {len(chunk)} rows.')
        thread = threading.Thread(target=starter.start_dataframe_injection, args=(chunk, headless))
        threads.append(thread)
        thread.start()
        thread_id += 1

        if len(threads) >= chunk_size:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
