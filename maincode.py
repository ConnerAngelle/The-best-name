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

#function to get the distance from one of the two sensors
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
        #checks distance from front sensor see if something is close to
        #it and tells the servo to open
        if(distance < 10):
            print("Open")
            servoDown(True, 3)
            
        else:
            print("Close")

#function to open the trash can using the servo
def servoDown(status, seconds):
    if(status == True):
        servo.min()
        sleep(seconds)
        servo.max()
        sleep(seconds)
        p, d = singleScan()
        showGui(p,d)
        # move servo to proper angle
        # sleep(seconds)
        # move servo back up
        # return True

#function to get the distance from the inside sensor
#and returns the distance and a percent for how full
#the trash can is
def singleScan():
    distance = getDistance(TRIGI, ECHOI)
    #percent based on the distance from the sensor based on the total
    #distance of an empty trash can
    percent = 100*(24.5 - distance)/24.5
    return percent, distance
    #send percent to GUI

#GUI that shows a percent of how full the trash can is
#and the distance between the trash and the sensor
def showGui(percent, insideDist):
    myText = ("The trash can is {} percent full. That is, there\nis a {} cm gap between the trash and the lid.".format(percent, insideDist))
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
#calibrate(TRIGF, ECHOF)
#calibrate(TRIGI, ECHOI)
servo.max()
frontScan()


