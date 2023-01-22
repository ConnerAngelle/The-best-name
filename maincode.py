# import our libraries
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
TRIGF = 18
ECHOF = 27
#pins for inside
TRIGI = 22
ECHOI = 25

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
    return distance
    

def frontScan():
    # will take the distance from getDistance function and 
    # compare it to a specified value
    while True:
        distance = getDistance()
        if(distance < 10):
            print("Open")
            servoDown(True, 1)
        else:
            print("Close")
        
    # 
    pass

def servoDown(status, seconds):
    # if status == True:
    # move servo to proper angle
    # sleep(seconds)
    # move servo back up
    # return True
    "singleScan(True)"
    pass

def singleScan(status):
    # 
    pass

def calculatePrcnt(d):
    pass

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
d = singleScan()
calculatePrcnt(d)

frontScan()
