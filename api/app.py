from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from api.index import Starter
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.logger.index import log
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/unique-register', methods=['POST'])
def unique_registering():
    data = request.get_json()
    print(data)  # Print the incoming request data
    if data:
        log.info('Starting single injection via JSON.')
        starter = Starter()
        starter.start_injection(data, 'json_injection')
        return jsonify({'message': 'JSON successfully loaded and processed'}), 200
    return jsonify({'message': 'ERROR: JSON not loaded'}), 400
    


@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        log.info(f'Recieved file: {filename}')
        df = read_dataframe(file)
        starter = Starter()
        starter.start_injection(df, 'dataframe_injection')
        return jsonify({'message': 'File successfully uploaded and processed'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')