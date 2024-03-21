from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database file
DATABASE = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    # Create table and insert data
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if table already exists to prevent overwriting
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if cursor.fetchone() is None:
        cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);')
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35);")
        conn.commit()
    conn.close()

@app.route('/users', methods=['GET'])
def get_user():
    name = request.args.get('name')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vulnerable SQL Query
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)

    # # Fixed SQL Query using parameterized queries
    # query = "SELECT * FROM users WHERE name = ?"
    # cursor.execute(query, (name,))
    
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "age": user[2]})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    init_db()  # Initialize the database and populate it
    app.run(debug=True)
