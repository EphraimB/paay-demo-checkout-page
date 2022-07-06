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
        userId = result[0]
        username = result[1]
        data = result[2]
        role = result[4]

    if sha256_crypt.verify(password, data):
        account = True
        session['logged_in'] = userId
        session['role'] = role
    else:
        account = False
        session['logged_in'] = None
    print(account)
    return redirect(url_for("index"))

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

@app.route('/addToCart')
def addToCart():
    userId = session.get('logged_in')
    productId = request.args.get("productId")

    cursor = config.dbPAAY.cursor(buffered=True)

    cursor.execute('INSERT INTO cart (ProductId, UserId, Quantity) VALUES (%s, %s, %s)', (productId, userId, 1))

    config.dbPAAY.commit()

    cursor.close()

    return redirect(url_for("index"))

@app.route('/checkout/', methods=['GET'])
def checkout():
    userId = session.get('logged_in')

    PaayApiKey = config.PaayApiKey

    cursor = config.dbPAAY.cursor(buffered=True)

    products = cursor.execute('SELECT * FROM paay.cart t1 JOIN paay.products t2 ON t1.ProductId = t2.ProductId JOIN Users.Users t3 ON t1.UserId = t3.uid WHERE t1.userId=%s', (userId,))
    products = cursor.fetchall()

    productsSum = cursor.execute('SELECT SUM(price) AS price FROM paay.cart t1 JOIN paay.products t2 ON t1.ProductId = t2.ProductId JOIN Users.Users t3 ON t1.UserId = t3.uid WHERE t1.userId=%s', (userId,))
    productsSum = cursor.fetchone()[0]

    if (productsSum == None):
        productsSum = 0

    if (session.get('logged_in') == None):
        return redirect(url_for("index"))
    else:
        return render_template('checkout/index.html', products = products, sum = productsSum, apiKey = PaayApiKey, loggedIn = session.get('logged_in'), role = session.get('role'))

@app.route('/checkout/delete/')
def deleteItem():
    cartId = request.args.get("id")

    cursor = config.dbPAAY.cursor(buffered=True)
    cursor.execute('DELETE FROM cart WHERE CartId=%s', (cartId,))

    config.dbPAAY.commit()

    cursor.close()

    return redirect(url_for("checkout"))

@app.route('/logout/')
def logout():
  session['logged_in'] = None
  session['role'] = None

  return redirect(url_for("index"))