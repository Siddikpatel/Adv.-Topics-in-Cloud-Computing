from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
base_path = '/siddik_PV_dir/'

@app.route('/store-file', methods=['POST'])
def store_file():

    data = request.get_json()

    if 'file' not in data or not data['file'] or 'data' not in data or not data['data']:
        return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

    file_name = data['file']
    file_data = data['data'].replace('\\n', '\n').replace(' ','')

    try:
        with open(os.path.join(base_path, file_name), 'w') as file:
            file.write(file_data)
        return jsonify({'file': file_name, 'message': "Success."}), 200
    except:
        return jsonify({'file': file_name, 'error': 'Error while storing the file to the storage.'}), 500

    
@app.route('/calculate', methods=['POST'])
def validate():

    data = request.get_json()

    if 'file' not in data or not data['file'] or 'product' not in data or not data['product']:
        return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

    file_name = data['file']

    if not os.path.isfile(base_path + file_name):
        return jsonify({'file': file_name, 'error': 'File not found.'}), 404

    product = data['product']

    container2 = "http://localhost:5100/"

    try:
        response = requests.post(container2, json={'file': file_name, 'product': product})
        return response.json(), response.status_code
    except:
        return jsonify({'error': "Couldn't communicate with container-2"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)