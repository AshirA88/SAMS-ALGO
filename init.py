import RPi.GPIO as GPIO
import time
import os
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import sys
from subprocess import check_output
import socket


lcd = LCD()

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

time.sleep(10)

def ip_add():  
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))   
    ip = s.getsockname()[0]
    return ip

def boot():
    lcd.clear()
    lcd.text('1. Attendace System',1)
    lcd.text('2. Reboot',2)
    time.sleep(5)
    lcd.clear()
    lcd.text('3. Shutdown',1)
    lcd.text('4. Ip Address',2)
boot()

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
            os.system('/bin/python /home/pi/Desktop/SAMS/display.py')
        if(GPIO.input(C2) == 1):        #2
            print("2")
            os.system('sudo reboot')
            #searchfp()
        if(GPIO.input(C3) == 1):        #3
            print("3")
            os.system('sudo shutdown -h now')
            #choice()
        if(GPIO.input(C4) == 1):        #A
            print("A")
    elif(line==L2):
        if(GPIO.input(C1) == 1):        #4
            print("4")
            lcd.clear()
            lcd.text("IP",1)
            lcd.text(ip_add(),2)
            time.sleep(5)
            lcd.clear()
            boot()
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