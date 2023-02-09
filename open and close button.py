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

    def Quit(self):
        global buttonPressed
        window.destroy()
        buttonPressed = 1

    def setupGUI(self):
        exitButton = Button(window, text = "Exit",\
                            command = lambda: self.Quit())
        exitButton.pack(side = BOTTOM, anchor = "w")
        openButton = Button(window, text = "Open",\
                            command = lambda: self.stayOpen(openButton))
        openButton.pack(side = BOTTOM, anchor = "e")
        while True:
            window.update()
            print("u")

    def stayOpen(self, openButton):
        global ocPressed
        ocPressed = 0
        openButton.destroy()
        closeButton = Button(window, text = "Close",\
                             command = lambda: self.close(closeButton))
        closeButton.pack(side = BOTTOM, anchor = "e")
        #servo.value = 0.2
        sleep(0.5)
        while(ocPressed == 0):
            window.update()
            print("Open")

    def close(self, closeButton):
        global ocPressed
        #while(servo.value > -1):
            #servo.value -= 0.2
            #sleep(0.75)
        closeButton.destroy()
        openButton = Button(window, text = "Open",\
                            command = lambda: self.stayOpen(openButton))
        openButton.pack(side = BOTTOM, anchor = "e")
        sleep(0.5)
        ocPressed = 1


window = Tk()
p = Trash(window)
    


