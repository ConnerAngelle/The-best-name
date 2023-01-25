# import our libraries
import RPi.GPIO as GPIO
from time import sleep, time
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
TRIGF = 18
ECHOF = 27
#pins for inside
TRIGI = 22
ECHOI = 25

GPIO.setup(TRIGF, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOF, GPIO.IN) # ECHO is an input
GPIO.setup(TRIGI, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOI, GPIO.IN) # ECHO is an input

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

    GPIO.cleanup()
    
    return distance



mytext = getDistance(TRIGI, ECHOI)
window = Tk()
text = Label(window, text=mytext)
text.pack()
window.mainloop()
