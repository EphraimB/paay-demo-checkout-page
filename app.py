from flask import Flask, render_template
import datetime
import config

app = Flask(__name__)

# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="admin@paayco",
#   database="paay"
# )

@app.route('/')
def index():
    cursor = config.db.cursor()

    cursor.execute("SELECT * from products")

    rows = cursor.fetchall()

    return render_template('index.html', products = rows)