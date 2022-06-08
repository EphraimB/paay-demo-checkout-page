# from flask import Flask
# from flaskext.mysql import MySQL

# app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'paayco'
app.config['MYSQL_DATABASE_DB'] = 'products'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

# mysql = MySQL(app)