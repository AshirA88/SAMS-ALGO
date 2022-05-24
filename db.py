import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
from mysql.connector import (connection)
import os
import platform

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="sams"
)



Cursor = db.cursor()

query = ("SELECT * FROM record")
Cursor.execute(query)

for (id, Attende,Timestamp) in Cursor:
    print("                                                                   ")
    print("id :",id)
    print("Attende :",Attende)
    print("Timestamp: ",Timestamp)
    print("\n")
    

