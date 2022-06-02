import mysql_connection
import datetime

mydb = mysql_connection.mysql_connection.mysql.connector.connect(
  host="localhost",
  user="root",
  password="paayco",
  database="products"
)

mycursor = mydb.cursor()

x = datetime.datetime.now()
print(x)

sql = "INSERT INTO products (ProductTitle, ProductDescription, DateCreated, DateModified) VALUES (%s, %s, %i, %i)"
val = ("JavaScript API key", "JavaScript API key for 3D secure.", x, x)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")