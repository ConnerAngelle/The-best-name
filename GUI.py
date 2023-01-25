from tkinter import *

WIDTH = 500

#setup the text
def setupGUI():
    text_frame = Frame(width = WIDTH)
    GUI = Text(text_frame, bg = "lightgrey")
    GUI.insert(END, "test")
    



window = Tk()
window.title("The best name")
setupGUI()

window.mainloop()
