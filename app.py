from flask import Flask, render_template
import mysql.connector
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    mydb = mysql.connector.connect(
        host="localhost",
        user="paay",
        password="123",
        database="products"
    )

    # mycursor = mydb.cursor()

    # x = datetime.datetime.now()

    # sql = "INSERT INTO products (ProductTitle, ProductDescription, DateCreated, DateModified) VALUES (%s, %s, %s, %s)"
    # val = ("JavaScript API key", "JavaScript API key for 3D secure.", x, x)
    # mycursor.execute(sql, val)

    mydb.commit()
    return render_template('index.html')