from flask import Flask, request, jsonify, Response
import sqlite3
from flask_cors import CORS

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

    # # Vulnerable SQL Query from raw string concatenation
    # query = f"SELECT * FROM users WHERE name = '{name}'"
    # cursor.execute(query)

    # Fixed SQL Query using parameterized queries
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (name,))
    
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "age": user[2]})
    else:
        return jsonify({"error": "User not found"}), 404

# @app.route('/.env', methods=['GET'])
# def get_env():
#     env_content = """
# DB_NAME=crapi
# DB_USER=crapi
# DB_PASSWORD=crapi
# DB_HOST=postgresdb
# DB_PORT=5432
# SERVER_PORT=8080
# MONGO_DB_HOST=mongodb
# MONGO_DB_PORT=27017
# MONGO_DB_USER=crapi
# MONGO_DB_PASSWORD=crapi
# MONGO_DB_NAME=crapi
# """
#     return Response(env_content, headers={
#         "Content-Disposition": "attachment; filename=env"
#     })

# Initialize Flask-CORS with your app and specify allowed origins
origins = [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
]
CORS(app, resources={r"/*": {"origins": origins}})

@app.after_request
def add_security_headers(response):
    # Add security headers to the response
    csp_policy = {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "https://code.jquery.com",
            "https://cdn.jsdelivr.net",
            "https://pagead2.googlesyndication.com",
            "cdn.datatables.net",
            "cdnjs.cloudflare.com",
            "www.googletagmanager.com",
            "partner.googleadservices.com",
            "tpc.googlesyndication.com",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "cdn.datatables.net",
            "fonts.googleapis.com",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://pagead2.googlesyndication.com",
        ],
        "font-src": [
            "'self'",
            "fonts.gstatic.com",
        ],
        "connect-src": [
            "'self'",
            "pagead2.googlesyndication.com",
            "www.google-analytics.com",
        ],
        "frame-src": [
            "'self'",
            "https://www.youtube.com",
            "googleads.g.doubleclick.net",
            "tpc.googlesyndication.com",
            "www.google.com",
        ],
    }
    csp_header_value = "; ".join(
        [f"{key} {' '.join(value)}" for key, value in csp_policy.items()]
    )
    response.headers["Content-Security-Policy"] = csp_header_value
    # Add other security headers
    response.headers["X-Frame-Options"] = "same-origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains;"
    )
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["X-XSS-Protection"] = "0; mode=block"

    response.headers["Content-Security-Policy-Report-Only"] = (
        "default-src 'self'; script-src 'self' https://cdn.example.com; style-src 'self' https://cdn.example.com; img-src 'self' data: https://cdn.example.com;"
    )
    ## this is causing issues remove from the sting above
    # report-uri /csp-report-endpoint;

    response.headers["Permissions-Policy"] = (
        "geolocation=(), camera=(), microphone=(), fullscreen=(), autoplay=(), payment=(), encrypted-media=(), midi=(), accelerometer=(), gyroscope=(), magnetometer=()"
    )

    # this one breaks the tiny chocobo icon
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

if __name__ == '__main__':
    init_db()  # Initialize the database and populate it
    app.run(host="0.0.0.0", debug=True)
