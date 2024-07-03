from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from api.index import start_injection
from api.src.utils.functions.read_dataframe import read_dataframe
from api.src.utils.logger.index import log
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/unique-register', methods=['POST'])
def unique_registering():
    data = request.get_json()
    print(data)  # Print the incoming request data
    return jsonify({"message": "Dados recebidos com sucesso!"}), 200

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

        start_injection(df, 'multiple_injection')
        return jsonify({'message': 'File successfully uploaded and processed'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')