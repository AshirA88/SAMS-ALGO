import RPi.GPIO as GPIO
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint #this is for fp module
import mysql.connector
from mysql.connector import errorcode
import os
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import sys

lcd = LCD()

"""def safe_exit(signum, frame): #not exactly sure what this is
    exit(1)
"""

"""this is for db connection"""

db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sams")
curs = db.cursor(buffered=True)


"""
This part is for keypad
"""
 
"""L1 = 16
L2 = 20
L3 = 21
L4 = 5

C1 = 6
C2 = 13
C3 = 19
C4 = 26"""


L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    try:
        lcd.clear()
        lcd.text("FP Sesnor Issue", 1)
        lcd.text("Restart Raspberry Pi!", 2)
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()
    #exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
ids=f.getTemplateCount()

lcd.text("Welcome To Attendance",1)
time.sleep(5)
lcd.text('Current Enrolled Users '+ str(ids),1)
time.sleep(5)
lcd.text('1. Attendance',1)
lcd.text('2. Registration',2)

#this is for enrlling fp
def enrollfp():
    try:
        lcd.clear()
        lcd.text('Waiting for finger...',1)
        lcd.text('Place Your Right Thumb...',2)
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            lcd.text('User already exists '+ str(positionNumber),1)
            time.sleep(3)
            lcd.clear()
            #exit(0)
            return

        print('Remove finger...')
        lcd.text('Remove finger...',1)
        time.sleep(2)

        lcd.text('Waiting for same finger again...',1)
        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        lcd.text('FP enrolled successfully!',1)
        time.sleep(2)
        lcd.text('New template position #' + str(positionNumber),1)
        time.sleep(2)
        lcd.clear()
        characterics = str(f.downloadCharacteristics(0x02)).encode('utf-8')
        cre_hash = hashlib.sha256(characterics).hexdigest()
        rollno=positionNumber 
        
        try:
            #inserting id and rollnumber to a table fpstore
            
            insert = """INSERT INTO fpstore(roll, id, hash) VALUES(%s, %s, %s)"""
            
            record = (rollno, positionNumber, cre_hash)
            
            curs.execute(insert, record)
            lcd.text('FP stored successfully!',1)
            curs.close()
            db.commit()
            lcd.clear()
            print("Record inserted successfully into FP Store Table")
            
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            lcd.text('Database Issue',1)
            time.sleep(2)
            lcd.clear()

        
        
        

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        lcd.text('Operation failed!',1)
        time.sleep(2)
        lcd.clear()
        #exit(1)

#this is for seraching fp and taking attendance
def searchfp():
    try:
        lcd.clear()
        lcd.text('Waiting for finger...',1)
        lcd.text('Place Your Right Thumb...',2)
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            lcd.text('No match found!',1)
            time.sleep(2)
            lcd.clear()
            #exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            lcd.text('FP Found!',1)
            time.sleep(1)
            lcd.clear()
                        
            f.loadTemplate(positionNumber, 0x01)
            rollno = positionNumber
        ## Downloads the characteristics of template loaded in charbuffer 1
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
            print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
            cre_hash = hashlib.sha256(characterics).hexdigest()
            
            #adds attendance to db
            db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sams")
            curs2 = db.cursor(buffered=True)
            
            insert = """INSERT INTO attendance(rollno, accuracy) VALUES(%s, %s)"""
            
            record = (rollno, accuracyScore)
            
            curs2.execute(insert, record)
            
            print("Record inserted successfully into Attendance Table")
            lcd.text('Record Inserted to Server',1)
            time.sleep(2)
            lcd.clear()
            curs2.close()
            db.commit()

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        lcd.text('Operation failed!',1)
        time.sleep(2)
        lcd.clear()
        #exit(1)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    # if(GPIO.input(C1) == 1):
    #     print(characters[0])
       
    # if(GPIO.input(C2) == 1):
    #     print(characters[1])

    # if(GPIO.input(C3) == 1):
    #     print(characters[2])

    # if(GPIO.input(C4) == 1):
    #     print(characters[3])
    
    if(line==L1):
        if(GPIO.input(C1) == 1):        #1
            print("1")
            enrollfp()
        if(GPIO.input(C2) == 1):        #2
            print("2")
            searchfp()
        if(GPIO.input(C3) == 1):        #3
            print("3")
            os.system('python convert.py')
        if(GPIO.input(C4) == 1):        #A
            print("A")
    elif(line==L2):
        if(GPIO.input(C1) == 1):        #4
            print("4")
        if(GPIO.input(C2) == 1):        #5
            print("5")
        if(GPIO.input(C3) == 1):        #6
            print("6")
        if(GPIO.input(C4) == 1):        #B
            print("B")
    elif(line==L3):
        if(GPIO.input(C1) == 1):        #7
            print("7")
        if(GPIO.input(C2) == 1):        #8
            print("8")
        if(GPIO.input(C3) == 1):        #9
            print("9")
        if(GPIO.input(C4) == 1):        #C
            print("C")
    elif(line==L4):
        if(GPIO.input(C1) == 1):        #*
            print("*")
        if(GPIO.input(C2) == 1):        #0
            print("0")
        if(GPIO.input(C3) == 1):        ##
            print("#")
        if(GPIO.input(C4) == 1):        #D
            print("D")
            lcd.clear()
            lcd.text("Bye!",1)
            time.sleep(2)
            lcd.clear()
            quit()
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram is stopped")