from tkinter import*
import cv2
import numpy as np
from PIL import Image, ImageTk
from time import time

# The screen is the class im expecting to change the most
# It is currently using the cv2 library to pull screenshots from 
# a laptops built in camera. Since the pi doesnt have that, changes will probably be made
# It then uses Pillow to contruct, resize, and display a constant feed to the screen
# The Image and imagetk are used to fit it in the Tkinter window
class Screen:
    def __init__(self,frame=None):
        self.frame = frame
       
        self.lmain = Label(self.frame)
        self.lmain.grid(row=(self.frame.grid_info()["row"]), column=(self.frame.grid_info()['column']))

        self.cap = cv2.VideoCapture(0)

        self.show_frame()

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
        r = ((self.frame["height"]*1.0)+200)/cv_img.shape[1]
        dim = (WIDTH/2, int(cv_img.shape[0] * r))
        resized = cv2.resize(cv_img, dim, interpolation = cv2.INTER_AREA)
        return resized

# This class makes the buttons for the camera
# intended on the buttons being able to toggle the 
# sonic sensor on the camera, manual 90 degree turns (if you don't want to use the joystick),
# center function, and, of course, turn the camera on and off

# the only issue im having is the layout of the buttons
# i want the buttons in a cross like formation in the frame but 
# having a hard time placinf them
class Buttons:
    def __init__(self,frame):
        self.frame = frame
        self.make_buttons()
        

    def make_buttons(self):
        self.button1 = Button(self.frame, text='Button1',width = 20, command=self.click)       
        self.button1.grid(row = 0, column = 0)

        self.button2 = Button(self.frame, text='Button2', width = 20,command=self.click)       
        self.button2.grid(row = 1, column = 0)

    def click(self):
        print "Clicked"


# This class makes a joystick that will be used 
# to control the motor on the camera
# that will turn the direction it needs to look
# I uses its x and y event corrdinates to give a general location
class Joystick:
    def __init__(self,frame):
        self.frame = frame
        self.f = {'x':int(self.frame['width']/2), 'y':int(self.frame['height']/2)}
        self.build()
        self.center(0) #Pointless variable
        
    def build(self):
        self.canvas = Canvas(self.frame,width=self.frame['width'],height=self.frame['height'])
        self.x = int(self.canvas['width'])
        self.y = int(self.canvas['height'])

        self.space = 25
        self.pad = 50

        self.canvas.create_rectangle((self.x/2)-self.space,self.pad,(self.x/2)+self.space,self.y-self.pad,fill="gray",outline="gray")
        self.canvas.create_rectangle(self.pad,(self.y/2)-self.space,self.x-self.pad,(self.y/2)+self.space,fill="gray",outline="gray")
        self.oval = self.canvas.create_oval(0, 0, 0, 0, fill = 'red')
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.move)
        self.canvas.bind('<ButtonRelease-1>',self.center)


    def draw(self,x,y):
        self.canvas.coords(self.oval, x-50, y-50, x+50, y+50)
    

    def center(self,u):
        self.draw(self.x/2,self.y/2)
        
        

    def move(self,event):
        x = event.x
        y = event.y

        
        if((x<(self.x/2) or x>(self.x/2)) and ((self.y/2)-25<y<(self.y/2)+25)):
            self.draw(event.x, self.y/2)
            self.motor(x)
            self.f['x'] = event.x
            self.f['y'] = self.y/2
        
        if((y<(self.y/2) or y>(self.y/2)) and ((self.x/2)-25<x<(self.x/2)+25)):
            self.draw(self.x/2, event.y)
            self.motor(y)
            self.f['x'] = self.x/2
            self.f['y'] = event.y
        
        
    def motor(self,c):
        print c

    

    
           
#####################################################################
WIDTH = 600
HEIGHT = 600
master=Tk()
master.geometry("{}x{}".format(WIDTH,HEIGHT))
master.resizable(0,0)

#Frame for the screen window
frame1=Frame(master, width=WIDTH/2, height=HEIGHT, background="blue")
frame1.grid(row=0, column=0, sticky="NS")
frame1.grid_propagate(0)
Screen(frame1)

#Frame for the buttons
frame2=Frame(master, width=WIDTH/2, height=HEIGHT/2, background="white")
frame2.grid(row=0, column=1, sticky="NE")
frame2.grid_propagate(0)
Buttons(frame2)

#Frame for the joystick
frame3=Frame(master, width=WIDTH/2, height=HEIGHT/2, background="red")
frame3.grid(row=0, column=1, sticky="SE")
frame3.grid_propagate(0)
Joystick(frame3)




master.mainloop()
