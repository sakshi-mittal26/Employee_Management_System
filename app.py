from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="employee_db",
    cursorclass=pymysql.cursors.DictCursor
)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return "Employee Management System Running 🚀"

# ---------------- EMPLOYEE CRUD ----------------

@app.route('/employees', methods=['GET'])
def get_employees():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM employees")
        data = cursor.fetchall()
    return jsonify(data)


@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        print("RECEIVED:", data)  # 🔥 DEBUG LINE

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO employees (name, email, position, salary) VALUES (%s, %s, %s, %s)",
                (
                    data.get("name"),
                    data.get("email"),
                    data.get("position"),
                    int(data.get("salary"))
                )
            )
            conn.commit()

        return jsonify({"message": "Employee added"}), 201

    except Exception as e:
        print("ERROR:", e)  # 🔥 SHOW ACTUAL ERROR
        return jsonify({"error": str(e)}), 500


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE employees SET name=%s, email=%s, position=%s, salary=%s WHERE id=%s",
            (data["name"], data["email"], data["position"], data["salary"], id)
        )
        conn.commit()

    return jsonify({"message": "Employee updated"})


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
        conn.commit()

    return jsonify({"message": "Employee deleted"})



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (data["email"], generate_password_hash(data["password"]))
        )
        conn.commit()

    return jsonify({"message": "User registered"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    with conn.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE email=%s", (data["email"],))
        user = cursor.fetchone()

    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"}), 401


from flask import render_template

@app.route("/employees-ui")
def employee_ui():
    return render_template("employee.html")


if __name__ == "__main__":
    app.run(debug=True)
