#################################################################
#  Jacob Bordelon, Cody Holland, Brenden Mayhall
#  11/12/2018
#  Description: A wireless camera that works from the raspberry pi
#  through VNC
#################################################################




from Tkinter import*
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
from time import time, sleep
from random import choice
import RPi.GPIO as GPIO

##########################################################
# Connect servo to BOARD 22
# Connect PIR motion sensor to BOARD 40
# Positive wire to BOARD 2
# Negative wire to BOARD 6
# Need USB camera (raspbian camera module will not work)
##########################################################

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
        _, frame = self.cap.read(0)
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        resized = self.resize(cv2image)
        img = Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(5, self.show_frame)
        
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
        self.canvas = Canvas(frame, width = 10, height = 10, background = "white")
        self.canvas.place(relx = .32, rely=.02, anchor = N)
        self.square = self.canvas.create_rectangle(0,0,10,10,outline="red",fill="red")
        self.make_buttons()
        self.state =False

        
        
        

    def make_buttons(self):
        self.button1 = Button(self.frame, text='Center',width = 10, command=self.click)       
        self.button1.place(relx = .5, rely = .25, anchor = CENTER)

        self.button2 = Button(self.frame, text='Quit', width = 10,command=self.quit_x)       
        self.button2.place(relx = .85, rely = .05, anchor = CENTER)

        self.button3 = Button(self.frame, text='Button3', width = 10,command=self.click)       
        self.button3.place(relx = .5, rely = .75, anchor = CENTER)

        self.button4 = Button(self.frame, text='Turn Left', width = 10,command=lambda: self.Turn("Left"))       
        self.button4.place(relx = .15, rely = .5, anchor = CENTER)

        self.button5 = Button(self.frame, text='Turn Right', width = 10,command=self.Turn)       
        self.button5.place(relx = .85, rely = .5, anchor = CENTER)

        self.button6 = Button(self.frame, text='On/Off', width = 10,command=self.on_off)       
        self.button6.place(relx = .15, rely = .05, anchor = CENTER)

    def on_off(self):
        if(self.state == False):
            self.state = True
            #s.start()
            self.canvas.itemconfig(self.square,fill="green",outline="green")
        else:
            self.state = False
            #s.stop()
            self.canvas.itemconfig(self.square,fill="red",outline="red")

    def click(self):
        print "clicked"

    def Turn(self, direct="Right"):
        if(direct == "Left"):
            j.f['x']=30
        else:
            j.f['x']=300
        j.motor(1)
        sleep(0.7)
        j.motor(0)

    def quit_x(self):
        global master
        #s.stop()
        master.destroy()
        

# This class makes a joystick that will be used 
# to control the motor on the camera
# that will turn the direction it needs to look
# I uses its x and y event corrdinates to give a general location
class Joystick:
    def __init__(self,frame):
        self.servo = 22
        self.sensor = 40
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo, GPIO.OUT)
        GPIO.setup(self.sensor,GPIO.IN)
        GPIO.add_event_detect(self.sensor,GPIO.BOTH,callback= self.change,bouncetime=150)
        self.p = GPIO.PWM(self.servo,50)
        self.p.start(2.5)
        
        
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

        #self.canvas.create_rectangle((self.x/2)-self.space,self.pad,(self.x/2)+self.space,self.y-self.pad,fill="gray",outline="gray")
        self.canvas.create_rectangle(self.pad,(self.y/2)-self.space,self.x-self.pad,(self.y/2)+self.space,fill="gray",outline="gray")
        self.oval = self.canvas.create_oval(0, 0, 0, 0, fill = 'red')
        self.canvas.pack()

        self.canvas.bind('<B1-Motion>', self.check)
        self.canvas.bind('<ButtonRelease-1>',self.center)


    def draw(self,x,y):
        self.canvas.coords(self.oval, x-50, y-50, x+50, y+50)

    def change(self,a):
        if GPIO.input(self.sensor):
            self.canvas['bg']="darkred"
        else:
            self.canvas['bg']="lightgray"
            
    

    def center(self,u):
        self.draw(self.x/2,self.y/2)
        self.motor(0)

    def check(self,event):
        x = event.x
        y = event.y

        if(x+50>self.x):
            x=self.x-50
        if(x-50<0):
            x=50
        
        
        self.draw(x,self.y/2)
        self.f['x'] = x
        self.motor(1)
        
        
            
            
        
        
    def motor(self,c):
        if(c != 0):
            if(self.f['x'] >self.x/2):
                self.p.ChangeDutyCycle(6.5)# go right 6.5
            else:
                self.p.ChangeDutyCycle(7.3)# go left 7.3
                
                
        else:
            self.p.ChangeDutyCycle(0)# stop
        
            

    


    
           
#####################################################################

master=Tk()
WIDTH = master.winfo_screenwidth()
HEIGHT = master.winfo_screenheight()
master.geometry("{}x{}+0+300".format(WIDTH,HEIGHT))
master.resizable(0,0)
master.attributes("-fullscreen",True)

#Frame for the screen window
frame1=Frame(master, width=WIDTH/2, height=HEIGHT, background="blue")
frame1.grid(row=0, column=0, sticky="NS")
frame1.grid_propagate(0)
s=Screen(frame1)

print 'Camera Setup: Good'

#Frame for the joystick
frame3=Frame(master, width=WIDTH/2, height=HEIGHT/2, background="red")
frame3.grid(row=0, column=1, sticky="SE")
frame3.grid_propagate(0)
j=Joystick(frame3)

print "Joystick Setup: Good"

#Frame for the buttons
frame2=Frame(master, width=WIDTH/2, height=HEIGHT/2, background="white")
frame2.grid(row=0, column=1, sticky="NE")
frame2.grid_propagate(0)
Buttons(frame2)

print "Buttons Setup: Good"

print "Starting..."
sleep(3)


master.mainloop()
GPIO.cleanup()
