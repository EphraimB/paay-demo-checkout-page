from flask import Flask, render_template
import datetime
import config

app = Flask(__name__)

@app.route('/')
def index():
    cursor = config.db.cursor()

    cursor.execute("SELECT * from products")

    rows = cursor.fetchall()

    title = "Home"

    return render_template('index.html', title = title, products = rows)