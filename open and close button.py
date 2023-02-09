from tkinter import *
from time import sleep, time
class Trash(Frame):
    # initialize an object of the class
    def __init__(self, parent):
        # call the parent's class initializer and make the background white
        Frame.__init__(self, parent, bg = "white")
        # make the window fullscreen
        parent.attributes("-fullscreen", True)
        self.setupGUI()

    def setupGUI(self):
        openButton = Button(window, text = "Open",\
                            command = lambda: self.stayOpen(openButton))
        openButton.pack(side = TOP, pady = 100)
        while True:
            window.update()

    def stayOpen(self, openButton):
        openButton.destroy()
        closeButton = Button(window, text = "Close",\
                             command = lambda: self.close(closeButton))
        closeButton.pack(side = TOP, pady = 100)
        #servo.value = 0.2
        sleep(0.5)
        while True:
            window.update()
            print("Open")

    def close(self, closeButton):
        #while(servo.value > -1):
            #servo.value -= 0.2
            #sleep(0.75)
        closeButton.destroy()
        sleep(0.5)
        self.setupGUI()


window = Tk()
p = Trash(window)
    


