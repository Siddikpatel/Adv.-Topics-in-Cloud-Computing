from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
app.json.sort_keys = False
base_path = './local/'

@app.route('/calculate', methods=['POST'])
def validate():

    data = request.get_json()

    if 'file' not in data or not data['file'] or 'product' not in data or not data['product']:
        return jsonify({'file': 'null', 'error': 'Invalid JSON input.'}), 400

    file_name = data['file']

    if not os.path.isfile(base_path + file_name):
        return jsonify({'file': file_name, 'error': 'File not found.'}), 404

    product = data['product']

    container2 = "http://container2:5100/"

    try:
        response = requests.post(container2, json={'file': file_name, 'product': product})
        return response.json(), response.status_code
    except:
        return jsonify({'error': "Couldn't communicate with container-2"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)