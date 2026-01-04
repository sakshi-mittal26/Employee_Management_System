# Employee Management System (CRUD)

This project is a full-stack Employee Management System built using Flask and MySQL.

## Features
- Add new employees
- View employee list
- Update employee details
- Delete employees
- Simple UI connected to Flask backend

## Tech Stack
- Backend: Flask (Python)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- ORM/Driver: PyMySQL

## API Endpoints
- GET /employees
- POST /employees
- PUT /employees/<id>
- DELETE /employees/<id>

## How to Run
1. Install dependencies  
   `pip install flask flask-cors pymysql python-dotenv cryptography`

2. Configure `.env` file with DB credentials

3. Run the app  
   `python app.py`

4. Open in browser  
   `http://127.0.0.1:5000/employees-ui`
