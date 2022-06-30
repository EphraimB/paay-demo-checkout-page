from flask import Flask
from flask_login import LoginManager
import mysql.connector
import os

app = Flask(__name__)

from app import routes

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "app":
  app.secret_key = os.urandom(12)