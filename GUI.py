from tkinter import *

WIDTH = 500

#setup the text
class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        


    def setupGUI(self):
        
        # setup the text to the right of the GUI
        # first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH // 2 )
        # the widget is a Tkinter Text 
        # disable it by default
        # don't let the widget control the frame's size
        GUI.text = Text(text_frame, bg = "lightgrey", state=DISABLED)
        GUI.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

    def setStatus(self, status):
        # enable the text widget, clear it, set it, and disabled
        GUI.text.config(state=NORMAL)
        GUI.text.insert(END, status)


status = "Test"
window = Tk()
t = GUI(window)
t.setupGUI()
t.setStatus(status)


window.mainloop()
