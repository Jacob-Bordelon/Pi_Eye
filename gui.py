from Tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk

class Camera(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master.geometry('{}x{}'.format(WIDTH,HEIGHT))
        self.master.resizable(0,0)

        self.make_frames()
        self.make_buttons()



    def make_frames(self):
        # Frame for buttons
        self.right_frame = Frame(width=WIDTH/2, height=HEIGHT/2,bg="gray")
        self.right_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=1, sticky='N')

        # Joystick
        self.canvas = Canvas(width=WIDTH/2, height=HEIGHT/2,background="white")
        self.canvas.grid_propagate(0)
        self.canvas.grid(row=0,column=1,sticky='S')
        
        # Camera view
        self.left_frame = Frame(width=WIDTH/2, height=HEIGHT,bg="lightgray")
        self.left_frame.grid_propagate(0)
        self.left_frame.grid(row=0,column=0, sticky="S")
        self.lmain = Label(self.left_frame)
        self.lmain.grid(row=0, column=0)
        self.cap = cv2.VideoCapture(0)

    def joystick(self):
        RADIUS = 0
        #x = (int(self.canvas["width"])/2)
        #y = (int(self.canvas["height"])/2)
        x = 200
        y = 150
        self.canvas.create_oval(x,y,x+RADIUS*2,y+RADIUS*2)


    def make_buttons(self):
        self.button1 = Button(self.right_frame, text='Button1', command=self.click)       
        self.button1.grid(column=0,row=0)

        self.button2 = Button(self.right_frame, text='Button2', command=self.click)       
        self.button2.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        resized = self.resize(cv2image)
        img = Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame) 

    def resize(self,cv_img):
        r = ((self.left_frame["height"]*1.0)+200)/cv_img.shape[1]
        dim = (WIDTH/2, int(cv_img.shape[0] * r))
        resized = cv2.resize(cv_img, dim, interpolation = cv2.INTER_AREA)
        return resized

    def click(self):
        print "Clicked"






	    

################################################
WIDTH = 800
HEIGHT=600

window = Tk()
window.title("Camera")

c = Camera(window)
c.show_frame()





window.mainloop()


