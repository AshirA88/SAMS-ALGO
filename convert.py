from threading import current_thread
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
from mysql.connector import (connection)
import os
import platform

from datetime import datetime

from numpy import insert #for date

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sams"
)


curr_date = date.today()        #date
print(curr_date)

now = datetime.now()            #time
curr_time = now.strftime("%H:%M:%S")
print("Current Time =", curr_time)




Cursor1 = db.cursor()
Cursor2 = db.cursor()
Cursor3 = db.cursor()
Cursor4 = db.cursor()
Cursor5 = db.cursor()
query = ("SELECT id,attendee,timestamp,date FROM record")
Cursor1.execute(query)


for (id,attendee,timestamp,date) in Cursor1:
      print("                                                                   ")
      if(date==curr_date):
        exit(0)
      else:
        max_id = ("SELECT * FROM fpstore")
        Cursor2.execute(max_id)

        max_value = None
        for (roll,id,hash) in Cursor2:
          if (max_value is None or roll > max_value):
            max_value = roll
          for i in range(0,max_value):
            curr_date = date.today()
            insert = ("INSERT INTO record(id, attendee, timestamp, date) VALUES(%s, %s, %s, %s)")        
            record = (i, 0, curr_time, curr_date)
            Cursor3.execute(insert, record)
          db.commit()
        print(max_value)




        query = ("SELECT rollno,timestamp,date FROM attendance")
        Cursor4.execute(query)







        for (rollno,timestamp,date) in Cursor4:
            print("                                                                   ")
            if(date==curr_date):
              attendee = 1
              insert = ("UPDATE record SET id = %s, attendee = %s, timestamp = %s, date = %s WHERE id = %s")        
              record = (rollno, attendee, timestamp, date, rollno)
              Cursor5.execute(insert, record)
              db.commit()


'''
query = ("SELECT * FROM record")
Cursor.execute(query)

for (id, Attende,Timestamp) in Cursor:
    print("                                                                   ")
    print("id :",id)
    print("Attende :",Attende)
    print("Timestamp: ",Timestamp)
    print("\n")'''
    
