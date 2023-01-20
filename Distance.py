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
# GPIO pins

TRIG = 18 # the sensor's TRIG pin
ECHO = 27 # the sensor's ECHO pin

GPIO.setup(TRIG, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHO, GPIO.IN) # ECHO is an input

distances = []

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
# uses the sensor to calculate the distance to an object
def getDistance():

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

def sorting(a):
    for i in range(len(a)):
        minimum = i
        for j in range(i+1,len(a)):
            if (a[j] < a[minimum]):
                minimum = j
        temp = a[i]
        a[i] = a[minimum]
        a[minimum] = temp
    return a

########
# MAIN #
########
# first, allow the sensor to settle for a bit
print("Waiting for sensor to settle({}s)...".format(SETTLE_TIME))
GPIO.output(TRIG, GPIO.LOW)
sleep(SETTLE_TIME)
# next, calibrate the sensor
correction_factor = calibrate()
# then, measure
input("Press enter to begin...")
print("Getting measurements:")
while (True):
    # get the distance to an object and correct it with the
    # correction factor
    print("-Measuring...")
    distance = getDistance() * correction_factor
    sleep(1)

    distance = round(distance, 4)
    distances.append(distance)
    print("--Distance measured: {}cm".format(distance))
    i = input("--Get another measurement (Y/n)? ")
    if (not i in [ "y", "Y", "yes", "Yes", "YES", "" ]):
        break
# finally, cleanup the GPIO pins

print("Done.")

print()
print("Unsorted measurements:")
print(distances)
sorted_distances = sorting(distances)
print("Sorted measurements:")
print(sorted_distances)
GPIO.cleanup()
