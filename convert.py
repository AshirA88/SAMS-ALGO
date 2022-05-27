from threading import current_thread
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
from mysql.connector import (connection)
import os
import platform

from datetime import datetime #for date and time

from numpy import insert

# for connecting to database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="sams"
)

check = 0

curr_date = date.today()        #date
print("Curent Date :=",curr_date)

now = datetime.now()            #time
curr_time = now.strftime("%H:%M:%S")
print("Current Time :=", curr_time)
#Cursors for interacting with Database and Buffered=True is to avoid Lazy Load from Database
Cursor1 = db.cursor(buffered=True)
Cursor2 = db.cursor(buffered=True)
Cursor3 = db.cursor(buffered=True)
Cursor4 = db.cursor(buffered=True)
Cursor5 = db.cursor(buffered=True)
Cursor6 = db.cursor(buffered=True)
Cursor7 = db.cursor(buffered=True)
query = ("SELECT id,attendee,timestamp,date FROM record") #fetch data from record
Cursor1.execute(query)
for (id,attendee,timestamp,date) in Cursor1:
  #To check if Data is already updated
      if(date!=curr_date): #check if date is similar
        check = 1
      if(date==curr_date):
        print("Attendance Already Updated for ", curr_date)
        exit(0)
#If data doesn't exist the new data for current date based attendance is inserted
if(check==1):
      max_id = ("SELECT * FROM fpstore")
      Cursor2.execute(max_id)
      max_value = None
      for (roll,id,hash) in Cursor2:
        if (max_value is None or roll > max_value):
          max_value = roll        
      for i in range(0,max_value+1):
        curr_date = date.today()
        insert = ("INSERT INTO record(id, attendee, timestamp, date) VALUES(%s, %s, %s, %s)")  
        record = (i, 0, curr_time, curr_date)
        Cursor3.execute(insert, record)
      db.commit()
      query = ("SELECT rollno,timestamp,date FROM attendance")
      Cursor4.execute(query)
#If Data is inserted the attendance has to be fetched from the attendance table and updated to record table
      for (rollno,timestamp,date) in Cursor4:          
          if(date==curr_date):
            attendee = 1
            insert = ("UPDATE record SET id = %s, attendee = %s, timestamp = %s, date = %s WHERE id = %s AND date = %s")        
            record = (rollno, attendee, timestamp, date, rollno, date)
            Cursor5.execute(insert, record)
            db.commit()
            # to increment the total count of attendance
      query7 = ("SELECT * FROM total") #fetch data from total
      Cursor7.execute(query7)
      for (id,total_count) in Cursor7:
          query6 = ("UPDATE total SET id = 1, total_count = total_count + 1 WHERE id = 1")    #update the total
          Cursor6.execute(query6)
          db.commit()

      print("Updation Completed")
      quit()
    
