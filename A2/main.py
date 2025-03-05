from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

@app.route('/store-products', methods=['POST'])
def store_data():
    data = request.get_json()
    
    try:
        with connection.cursor() as cursor:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS products_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price VARCHAR(255) NOT NULL,
                availability BOOLEAN NOT NULL
            )
            """
            cursor.execute(create_table_sql)
            sql = "INSERT INTO products_table (name, price, availability) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['name'], data['price'], data['availability']))
        connection.commit()
    finally:
        connection.close()
    
    return jsonify({'message': 'Success.'}), 200
    
@app.route('/list-products', methods=['GET'])
def retrieve_data():
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products_table"
            cursor.execute(sql)
            result = cursor.fetchall()
            products = []
            for row in result:
                products.append({
                    'name': row[1],
                    'price': row[2],
                    'availability': row[3]
                })
    finally:
        connection.close()
    
    return jsonify({'products': products}), 200

connection = pymysql.connect(
    host='products-instance-1.c4xrlsohiz8m.us-east-1.rds.amazonaws.com',
    user='admin',
    password='Admin_123456',
    database='products'
)

if __name__ == '__main__':
    app.run(debug=True)
