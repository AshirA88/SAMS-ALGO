import RPi.GPIO as GPIO
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint #this is for fp module
import mysql.connector
from mysql.connector import errorcode

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
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


#this is for enrlling fp
def enrollfp():
    try:
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
            exit(0)

        print('Remove finger...')
        
        time.sleep(2)

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
        
        characterics = str(f.downloadCharacteristics(0x02)).encode('utf-8')
        cre_hash = hashlib.sha256(characterics).hexdigest()
        rollno=positionNumber 
        
        try:
            #inserting id and rollnumber to a table fpstore
            
            insert = """INSERT INTO fpstore(roll, id, hash) VALUES(%s, %s, %s)"""
            
            record = (rollno, positionNumber, cre_hash)
            
            curs.execute(insert, record)
            db.commit()
            print("Record inserted successfully into FP Store Table")
            
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))

        curs.close()
        db.close()
        
        

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

#this is for seraching fp and taking attendance
def searchfp():
    try:
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
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
           
            
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
            curs = db.cursor()
            
            insert = """INSERT INTO attendance(rollno, accuracy) VALUES(%s, %s)"""
            
            record = (rollno, accuracyScore)
            
            curs.execute(insert, record)
            db.commit()
            print("Record inserted successfully into Attendance Table")
            curs.close()
            db.close()

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)


def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print(characters[0])
        enrollfp()
    if(GPIO.input(C2) == 1):
        print(characters[1])
        searchfp()
    if(GPIO.input(C3) == 1):
        print(characters[2])
        quit()
    if(GPIO.input(C4) == 1):
        print(characters[3])
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
