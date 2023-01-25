import RPi.GPIO as GPIO
from time import sleep, time

# constants
DEBUG = False 
SETTLE_TIME = 2   # seconds to let the sensor settle
CALIBRATIONS = 5  # number of calibration measurements to take
CALIBRATION_DELAY = 1 # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001 # seconds needed to trigger the sensor(to get a measurement)
SPEED_OF_SOUND = 343 # speed of sound in m/s set the RPi to the Broadcom pin layout

GPIO.setmode(GPIO.BCM)

#pins for front
TRIGF = 
ECHOF =
#pins for inside
TRIGI =
ECHOI =

GPIO.setup(TRIGF, GPIO.OUT)
GPIO.setup(ECHOF, GPIO.IN)

GPIO.setup(TRIGI, GPIO.OUT)
GPIO.setup(ECHOI, GPIO.IN)

distanceF = []
distanceI = []

