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

GPIO.setup(TRIGF, GPIO.OUT)
GPIO.setup(ECHOF, GPIO.IN)

GPIO.setup(TRIGI, GPIO.OUT)
GPIO.setup(ECHOI, GPIO.IN)

distanceF = []
distanceI = []


def calibrate():
    print("Calibrating...")
    print("-Place the sensor a measured distance away from an \
     object.")
    known_distance = float(input("-What is the measured distance \
     (cm)? "))

    print("-Getting calibration measurements...")
    distance_avg = 0
    for i in range(CALIBRATIONS):
        distance = getDistance()
        if (DEBUG):
            print("--Got {}cm".format(distance))
        distance_avg += distance
        sleep(CALIBRATION_DELAY)

    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print("--Average is {}cm".format(distance_avg))
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print("--Correction factor is {}".format(correction_factor))
    print("Done.")
    print()
    return correction_factor

def getDistance(TRIG, ECHO):

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

frontDist = getDistance(TRIGF, ECHOF)
insideDist = getDistance(TRIGI, ECHOI)



#Main code

