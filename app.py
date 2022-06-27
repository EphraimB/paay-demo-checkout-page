from flask import Flask, flash, redirect, render_template, request, session, abort
from passlib.hash import sha256_crypt
import datetime
import config
import os
import operator

app = Flask(__name__)

@app.route('/')
def index():
    cursor = config.dbPAAY.cursor()

    cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()

    return render_template('index.html', products = rows, loggedIn = session.get('logged_in'), role = session.get('role'))

@app.route('/login', methods=['POST'])
def login():
    login = request.form

    username = login['username']
    password = login['password']

    cursor = config.dbUsers.cursor(buffered=True)

    results = cursor.execute('SELECT * FROM Users LEFT JOIN Roles ON Users.RoleId = Roles.RoleId WHERE username=%s', (username,))
    results = cursor.fetchall()

    for result in results:
        username = result[1]
        data = result[2]
        role = result[4]

    session['role'] = role;

    if sha256_crypt.verify(password, data):
        account = True
    else:
        account = False

    if account == True:
        session['logged_in'] = username
    else:
        session['logged_in'] = None
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    signup = request.form

    username = signup['username']
    password = sha256_crypt.encrypt(signup['password'])
    email = signup['email']
    roleId = 0

    cursor = config.dbUsers.cursor(buffered=True)

    cursor.execute('INSERT INTO Users (username, password, email, RoleId) VALUES (%s, %s, %s, %s)', (username, password, email, roleId))

    config.dbUsers.commit()

    cursor.close()

    return redirect('/')

@app.route('/addProduct', methods=['POST'])
def addProduct():
    addProduct = request.form
    
    productTitle = addProduct['productTitle']
    productDescription = addProduct['productDescription']

    cursor = config.dbPAAY.cursor(buffered=True)

    cursor.execute('INSERT INTO products (productTitle, productDescription) VALUES (%s, %s)', (productTitle, productDescription))

    config.dbPAAY.commit()

    cursor.close()

    return redirect('/')

@app.route('/checkout/index.html', methods=['GET'])
def checkout():
    productId = request.args.get('productId')

    cursor = config.dbPAAY.cursor(buffered=True)

    product = cursor.execute('SELECT * FROM products WHERE productID=%s', (productId,))
    product = cursor.fetchall()

    return render_template('checkout/index.html', products = product, loggedIn = session.get('logged_in'), role = session.get('role'))

@app.route('/logout/')
def logout():
  session['logged_in'] = None
  session['role'] = None
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "app":
    app.secret_key = os.urandom(12)