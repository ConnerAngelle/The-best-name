# import our libraries
import RPi.GPIO as GPIO
from time import sleep, time
from gpiozero import Servo
from tkinter import *

# constants
DEBUG = False
SETTLE_TIME = 2   # seconds to let the sensor settle
CALIBRATIONS = 5  # number of calibration measurements to take
CALIBRATION_DELAY = 1 # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001 # seconds needed to trigger the sensor(to get a measurement)
SPEED_OF_SOUND = 343 # speed of sound in m/s set the RPi to the Broadcom pin layout

GPIO.setmode(GPIO.BCM)

#pins for front
global TRIGF, ECHOF, TRIGI, ECHOI, servo
TRIGF = 18
ECHOF = 27
#pins for inside
TRIGI = 22
ECHOI = 25
servo = Servo(12)

GPIO.setup(TRIGF, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOF, GPIO.IN) # ECHO is an input
GPIO.setup(TRIGI, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOI, GPIO.IN) # ECHO is an input

# Functions
def calibrate(TRIG, ECHO):
    pass

def getDistance(TRIG, ECHO):
    # will return a single distance
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)

    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
        end = time()

    duration = end - start

    distance = duration * SPEED_OF_SOUND

    distance /= 2
    
    distance *= 100

    #GPIO.cleanup()
    
    return distance

def frontScan():
    # will take the distance from getDistance function and 
    # compare it to a specified value
    while True:
        sleep(0.5)
        distance = getDistance(TRIGF, ECHOF)
        if(distance < 10):
            print("Open")
            servoDown(True, 1)
        else:
            print("Close")

def servoDown(status, seconds):
    if(status == True):
        servo.min()
        sleep(2)
        servo.mid()
        sleep(2)
        servo.max()
        sleep(seconds)
        singleScan(True)
        # move servo to proper angle
        # sleep(seconds)
        # move servo back up
        # return True

def singleScan(status):
    if(status == True):
        distance = getDistance(TRIGI, ECHOI)
        percent = 100*(23 - distance)/23
        #send percent to GUI

#def calculatePrcnt(d):
    
 #   pass

def showGui(insideDist):
    myText = ("{}".format(insideDist))
    window = Tk()
    text = Label(window, text=myText)
    text.pack()
    window.mainloop()

## overall ideas:
# front sensor will read constantly and as soon as it receives a distance of less than 10 cm
# the compareDistance function will open for 10 seconds 
# best case scenario: GUI gives options for how long to leave the lid open
# Also at the beginning (while closed) the inside sensor will record a single measurement of the interior
# and return that to the GUI
# Once open the user will theoretically put whatever they need to inside 
# Once timer is up, the servo will go back to its original position
# Once closed the interior sensor will take another single measurement of the interior
# and display result on GUI
# Also once closed, the front sensor will go back to its constant state of sensing


## Main Program
calibrate(TRIGF, ECHOF)
calibrate(TRIGI, ECHOI)
d = singleScan(True)
showGui(d)

