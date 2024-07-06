from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from api.index import Starter
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.logger.index import log
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

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
        df = read_dataframe(file)
        process_in_chunks(df, headless_option)
        return jsonify({'message': 'File successfully uploaded and processed'}), 200


def process_in_chunks(df, headless):
    starter = Starter()
    chunk_size = 5
    threads = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size].copy()  
        thread = threading.Thread(target=starter.start_dataframe_injection, args=(chunk, headless, 'dataframe_injection'))
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')