# import our libraries
import RPi.GPIO as GPIO
from time import sleep, time
from gpiozero import Servo
from tkinter import *
        
# constants
TRIGGER_TIME = 0.00001 # seconds needed to trigger the sensor(to get a measurement)
SPEED_OF_SOUND = 343 # speed of sound in m/s set the RPi to the Broadcom pin layout

GPIO.setmode(GPIO.BCM)

# pins for front sensor
global TRIGF, ECHOF, TRIGI, ECHOI, servo
TRIGF = 18
ECHOF = 27
# pins for inside sensor
TRIGI = 22
ECHOI = 25
servo = Servo(12)

GPIO.setup(TRIGF, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOF, GPIO.IN) # ECHO is an input
GPIO.setup(TRIGI, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHOI, GPIO.IN) # ECHO is an input

# creates a Trash class inheriting from Tkinter's frame class
class Trash(Frame):
    # initialize an object of the class
    def __init__(self, parent):
        # call the parent's class initializer and make the background white
        Frame.__init__(self, parent, bg = "white")
        # make the window fullscreen
        parent.attributes("-fullscreen", True)
        # call the setupGUI function to run the main program
        self.setupGUI(0)

    def Quit(self):
        global buttonPressed
        window.destroy()
        buttonPressed = 1

    #funtion to keep the lid open
    def stayOpen(self, openButton):
        openButton.destroy()
        closeButton = Button(window, text = "Close",\
                             command = lambda: self.close(closeButton))
        closeButton.pack(side = BOTTOM, anchor = "e")
        servo.value = 0.3
        while True:
            window.update()
        
    
    def close(self, closeButton):
        while(servo.value > -0.9):
            servo.value -= 0.2
            sleep(0.75)
        closeButton.destroy()
        sleep(0.5)
        self.setupGUI(0)
    
    # a GUI-based function that the entire program flows through
    def setupGUI(self, c):
        global buttonPressed
        buttonPressed = c
        exitButton = Button(window, text = "Exit",\
                            command = lambda: self.Quit())
        exitButton.pack(side = BOTTOM, anchor = "w")

        #button to keep the lid open
        openButton = Button(window, text = "Open",\
                            command = lambda: self.stayOpen(openButton))
        openButton.pack(side = BOTTOM, anchor = "e")

        # set the servo to its starting position
        servo.min()
        sleep(0.5)
        # run indefinitely
        while True:
            # find the percentage of the trash can that is full
            # and display it to the GUI
            percent = self.singleScan()
            myText = ("The trash can is {} percent full".format(int(percent)))
            text = Label(window, text=myText, font = ("Playbill", 16))
            text.pack(side = TOP, pady = 100)
            window.update()
            # check how close the nearest object is to the
            # front of the trash can
            self.frontScan()
            if(buttonPressed == 1):
                break
            # reset the text on the GUI
            text.destroy()

    # function to get the distance from one of the two sensors
    def getDistance(self, TRIG, ECHO):
        # setup the sensor's pins
        GPIO.output(TRIG, GPIO.HIGH)
        sleep(TRIGGER_TIME)
        GPIO.output(TRIG, GPIO.LOW)
        
        # record the duration between the sound being emitted
        # and the echo being heard
        while (GPIO.input(ECHO) == GPIO.LOW):
            start = time()
        while (GPIO.input(ECHO) == GPIO.HIGH):
            end = time()
        duration = end - start

        # Find the distance by multiplying the duration by a constant 
        distance = ( duration * SPEED_OF_SOUND * 50 )
        return distance
    # search for a close object forever, and open the trash can when found
    def frontScan(self):
        global buttonPressed
        # takes the distance from getDistance function and 
        # compares it to a specified value
        running = True
        while(running == True):
            sleep(0.5)
            distance = self.getDistance(TRIGF, ECHOF)
            window.update()
            if(buttonPressed == 1):
                break

            # checks distance from front sensor see if something is close to
            # it and tells the servo to open
            elif(distance < 10):
                #print("Open")
                # make the servo go down for 5 seconds
                self.servoDown(True, 5)
                running = False

    # function to open the trash can using the servo
    def servoDown(self, status, seconds):
        # makes the servo turn to push down the lever
        if(status == True):
            servo.value = 0.3
            sleep(seconds)
            #loops with a delay to allow the servo to turn back
            #up while the lever slowly rises back up
            while (servo.value > -0.9):
                servo.value -= 0.2
                sleep(0.75)
            sleep(1.5)

    # function to get the distance from the inside sensor
    # and returns the percent for how full
    # the trash can is
    def singleScan(self):
        distance = self.getDistance(TRIGI, ECHOI)
        #percent based on the distance from the sensor based on the total
        #distance of an empty trash can
        percent = 100*(21.5 - distance)/21.5
        if percent <= 0:
            percent = 0
        return percent

## Main Program

window = Tk()
p = Trash(window)
