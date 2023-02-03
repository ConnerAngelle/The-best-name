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
global TRIGF, ECHOF, TRIGI, ECHOI, servo, button
TRIGF = 18
ECHOF = 27
#pins for inside
TRIGI = 22
ECHOI = 25
servo = Servo(12)

button = 5

GPIO.setup(TRIGF, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOF, GPIO.IN) # ECHO is an input
GPIO.setup(TRIGI, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOI, GPIO.IN) # ECHO is an input
GPIO.setup(button, GPIO.IN) # button is an input

class Trash(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "white")
        parent.attributes("-fullscreen", True)
        self.setupGUI()
    
    def close(self):
        window.destroy()
        
    def setupGUI(self):
        while True:
            percent, insideDist = self.singleScan()
            myText = ("The trash can is {} percent full".format(int(percent)))

            #myText = ("The trash can is {} percent full. That is, there\nis a {} cm gap\
            #           between the trash and the lid.".format(int(percent), int(insideDist)))
            text = Label(window, width = 400, height = 200, text=myText, font = ("Playbill", 16))
            text.pack(side = TOP)
            #button = Button(window, width = 400, height = 200, text = "Exit", font = ("Playbill", 16), command = quit)
            #button.pack(side = BOTTOM)
            if (GPIO.input(button) == GPIO.HIGH):
                break
            window.after(1000, window.quit)
            window.mainloop()
            self.frontScan()
            text.destroy()

    #function to get the distance from one of the two sensors
    def getDistance(self, TRIG, ECHO):
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

    def frontScan(self):
        # will take the distance from getDistance function and 
        # compare it to a specified value
        running = True
        while(running == True):
            sleep(0.5)
            distance = self.getDistance(TRIGF, ECHOF)
            #checks distance from front sensor see if something is close to
            #it and tells the servo to open
            if(distance < 10):
                print("Open")
                self.servoDown(True, 3)
                running = False
                
            else:
                print("Close")

    #function to open the trash can using the servo
    def servoDown(self, status, seconds):
        if(status == True):
            servo.min()
            sleep(seconds)
            servo.max()
            sleep(seconds)

    #function to get the distance from the inside sensor
    #and returns the distance and a percent for how full
    #the trash can is
    def singleScan(self):
        distance = self.getDistance(TRIGI, ECHOI)
        #percent based on the distance from the sensor based on the total
        #distance of an empty trash can
        percent = 100*(22 - distance)/22
        if percent <= 0:
            percent = 0
        if distance >= 22:
            distance = 22
        return percent, distance




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
window = Tk()
p = Trash(window)



