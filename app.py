from flask import Flask, render_template
import datetime
import config

app = Flask(__name__)

@app.route('/')
def index():
    cursor = config.db.cursor()

    cursor.execute("SELECT * from products")

    rows = cursor.fetchall()

    return render_template('index.html', products = rows)

@app.route('/admin-login/')
def login():
    return render_template('/admin-login/index.html')

@app.route('/signup', methods=['POST'])
def signup():
    return