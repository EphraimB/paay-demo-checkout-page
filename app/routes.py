from app import app
from flask import redirect, render_template, request, session, url_for
from passlib.hash import sha256_crypt
from flask_login import current_user, login_user
import datetime
from app import config
import os
import operator

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

    session['role'] = role

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

    return redirect(url_for("index"))

@app.route('/addProduct', methods=['POST'])
def addProduct():
    addProduct = request.form
    
    productTitle = addProduct['productTitle']
    productDescription = addProduct['productDescription']
    productPrice = addProduct['productPrice']

    cursor = config.dbPAAY.cursor(buffered=True)

    cursor.execute('INSERT INTO products (productTitle, productDescription, price) VALUES (%s, %s, %s)', (productTitle, productDescription, productPrice))

    config.dbPAAY.commit()

    cursor.close()

    return redirect(url_for("index"))

@app.route('/checkout/index.html', methods=['GET'])
def checkout():
    productId = request.args.get('productId')

    cursor = config.dbPAAY.cursor(buffered=True)

    product = cursor.execute('SELECT * FROM products WHERE productID=%s', (productId,))
    product = cursor.fetchall()

    return render_template('checkout/index.html', product = product[0], loggedIn = session.get('logged_in'), role = session.get('role'))

@app.route('/logout/')
def logout():
  session['logged_in'] = None
  session['role'] = None
  return redirect(url_for("index"))