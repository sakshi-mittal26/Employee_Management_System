from flask import Flask, render_template, redirect, url_for
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MySQL connection
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

# ---------------- PRODUCTS PAGE ----------------
@app.route("/")
def products():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("index.html", products=products)

# ---------------- ADD TO CART ----------------
@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (product_id) VALUES (%s)", (id,))
    conn.commit()
    return redirect(url_for("products"))

# ---------------- VIEW CART ----------------
@app.route("/cart")
def cart():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cart.id, products.name, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
    """)
    items = cursor.fetchall()
    return render_template("cart.html", items=items)

# ---------------- REMOVE FROM CART ----------------
@app.route("/remove/<int:id>")
def remove(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)
