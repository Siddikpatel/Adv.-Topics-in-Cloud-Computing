from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
app.json.sort_keys = False
base_path = './local/'

@app.route('/', methods=['POST'])
def calculate_sum():

    data = request.get_json()

    file_name = data['file']
    product = data['product']

    sum = 0

    try: 
        with open(base_path + file_name, 'r') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:
                if row['product'] == product:
                    sum += int(row['amount'])

        return jsonify({"file": file_name, "sum": sum}), 200
    
    except:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 500
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)