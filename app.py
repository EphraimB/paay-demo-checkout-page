from flask import Flask, render_template
import mysql.connector
import datetime
# import config

app = Flask(__name__)

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="paayco"
)

@app.route('/')
def index():
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * from products")

    rows = cursor.fetchall()

    return render_template('index.html', products = rows)