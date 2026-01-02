from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MySQL connection (from .env)
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    return "Server is running!"


@app.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    email = data.get('email')
    password = data.get('password')

    hashed_password = generate_password_hash(password)

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except:
        return jsonify({"message": "User already exists"}), 400


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    email = data.get('email')
    password = data.get('password')

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/dashboard')
def dashboard():
    return "Welcome to protected page"


if __name__ == "__main__":
    app.run(debug=True)
