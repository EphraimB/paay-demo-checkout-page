from flask import Flask, render_template
from flaskext.mysql import MySQL
import datetime
# import config

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'paayco'
app.config['MYSQL_DATABASE_DB'] = 'products'
app.config['MYSQL_DATABASE_HOST'] = 'db'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.get_db().cursor()

    cursor.execute("SELECT * from products")

    rows = cursor.fetchall()

    return render_template('index.html', products = rows)