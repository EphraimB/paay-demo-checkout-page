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

    return render_template('index.html', products = rows, loggedIn = session.get('logged_in'))

@app.route('/login', methods=['POST'])
def login():
    login = request.form

    username = login['username']
    password = login['password']

    cursor = config.dbUsers.cursor(buffered=True)

    data = cursor.execute('SELECT * FROM Users LEFT JOIN Roles ON Users.RoleId = Roles.RoleId WHERE username=%s', (username,))
    data = cursor.fetchone()[2]

    if sha256_crypt.verify(password, data):
        account = True
    else:
        account = False

    if account == True:
        session['logged_in'] = True
    else:
        session['logged_in'] = False
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    signup = request.form

    username = signup['username']
    password = sha256_crypt.encrypt(signup['password'])
    email = signup['email']

    cursor = config.dbUsers.cursor(buffered=True)

    cursor.execute('INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))

    config.dbUsers.commit()

    cursor.close()

    return index()

@app.route('/logout/')
def logout():
  session['logged_in'] = False
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port=5000)

if __name__ == "app":
    app.secret_key = os.urandom(12)