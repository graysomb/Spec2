'''
Created on Dec 8, 2015

@author: Michael Grayson
This is the threaded implementation of a GUI (graphical USer Interface)
It contains buttons, input text boxes, and methods which control the
rest of the program
'''


# the GUI class is dependent on the dataCollector class which handles motor control
# and data collection
import DataCollecter, ErrorHandler

# this is used for timing various parts of the program during testing
import time

# Multiprocesscing is a python library used to create subprocesses that can run 
# independently of the original code (does not share memory)
import multiprocessing as mp
# thread or threading is a library for generation of new processes that are dependent
# on the original code (shares memory)
import thread
# serial is the library used to communicate with the arduino over USB
import serial 
# numpy is the standard numerical library for python is very similar to Matlab 
# in implementation, Matplotlib is a plotting library for numpy
import numpy as np
import matplotlib.pyplot as plt



# these libraries are separate libraries for error messages Tkinter is the standard python gui
import os
import Tkinter
import tkMessageBox
import tkSimpleDialog
import tkFileDialog
import tkCommonDialog

def displayCon(PIPE): #Displays output of console commands called as a subprocess
    root = Tkinter.Tk()
    var = Tkinter.StringVar()
    ans = ' '
    var.set(ans)
    l = Tkinter.Label(root, textvariable = var)
    l.pack()
    while True:
        ans = ans+PIPE.recv()
        var.set(ans)
        root.update_idletasks()
    
def displayError( titl, error): # takes text input and generates a Tkinter error message
    root = Tkinter.Tk()
    root.withdraw()
    tkMessageBox.showerror( parent = root, title = titl, message = error)   
    
def getText( titl, text, Q): # takes a text intput from a tkinter window and sends it over a pipe 
    root = Tkinter.Tk()
    root.withdraw()
    ans = tkSimpleDialog.askstring(titl, text)
    Q.put(ans)

def getDir( titl,Q): # gets a directory from a Tkinter window and sends it over a pipe
    root = Tkinter.Tk()
    root.withdraw()
    currdir = os.getcwd()
    tempdir = tkFileDialog.askdirectory(parent = root, initialdir=currdir, title = titl)
    Q.put(tempdir)

# These commands are for multiprocessing calls, multiprocessing can only use function defined at the highest level in the code.
def getData(Pipe,q):
    '''
    Receives data from the end of a Pipe (multiprocessing) until it receives "end" and places the data in a Queue.
    Pipes have a limited number of elements and this is used to prevent overflow
    '''
    ans = Pipe.recv() 
    data = []
    while ans != "end":
        data.append(ans) # saves data in list
        ans = Pipe.recv() # gets data off of pipe
    q.put(data) #puts all the data in a Queue and closes
    
def plotData(lightPipe, angPipe):
    '''
    Receives data from the end of a Pipe (multiprocessing) until it receives "end" and plots the data
    '''
    
    y = []
    x = []
   
    plt.ion()
   
    fig = plt.figure() # creates a figure
    
    while lightPipe.poll() == False or angPipe.poll() == False: # this is used to wait for data to reach the end of the Pipe
        pass
    light = lightPipe.recv() # get data from pipe
    ang = angPipe.recv()
    start = time.clock()
    while light != "end":
        y.append(light) # add data to x and y
        x.append(ang)
        while lightPipe.poll() == False or angPipe.poll() == False: # wait for more data
            pass
        light = lightPipe.recv()
        ang = angPipe.recv()
        if (time.clock()-start)>.5: # if time before last plot is greater than 0.5s make a new plot.
            start = time.clock()
            ax = fig.add_subplot(111)
            line1, = ax.plot(x, y, 'r-')
            fig.canvas.draw()

def SubArd(LightPipe,startPipe):
            '''
            Creates an arduino serial object, reads data, and sends it over a pipe.
            Used in multiprocessing for concurrent data collection
            this function has an infinite loop and must be ended with Process.terminate()
            '''
            baudrate = 250000
            arduino2 = serial.Serial("COM6",baudrate,timeout=1) # create arduino object
            connected = False
            while not connected:  # wait to be connected
                serin = arduino2.read()
                connected = True;
            print("Connected")
            arduino2.readline()
            arduino2.readline()
            arduino2.readline() # flush out the serial line
            startPipe.send(True) # send that data collection is about to begin
            while True: # collect data forever
                arduino2.write("1") # tell arduino to collect data
                ans = float(arduino2.readline()) # get data over serial 
                LightPipe.send(ans) # send over pip
        
        
        
# These imports are for different parts of the GUI, Kivy is the graphics library
# that was used
import kivy
from kivy.uix.gridlayout import GridLayout
kivy.require('1.0.7')
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker

class Menu(GridLayout): 
    '''
    This is the main GUI class and is build off of a GridLayout. It contains all the buttons and text boxes used in the GUI.
    It has methods which are used to create DataCollectors
    '''
    
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.cols = 4 # set the number of columns in the grid to 4
        self.saucier = None # initialize with no dataCollector
        

#         Window.clearcolor = [1.0, 0.6774193548387096, 0.0, 1.0]
        
        # sets the button spacing to 5
        self.spacing = [5,5]

#         clr_picker = ColorPicker()
#         self.add_widget(clr_picker)
# 
#         # To monitor changes, we can bind to color property changes
#         def on_color(instance, value):
#             print "RGBA = ", str(value)  #  or instance.color
#             print "HSV = ", str(instance.hsv)
#             print "HEX = ", str(instance.hex_color)
# 
#         clr_picker.bind(color=on_color)


        # buttons are created then added to the menu
        # connect button
        self.connectButton = Button( text='Connect',
                        on_press=self.connect) # create button that when pressed calls self.connect
        self.connectButton.background_normal = '' # set color to none
        self.connectButton.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667] # change color to blue
        self.add_widget(self.connectButton) # adds the button to the menu
        
#         settings button
        self.SettingsButton = Button( text='Settings',
                        on_press=self.settings)
        self.SettingsButton.background_normal = ''
        self.SettingsButton.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667]
        self.add_widget(self.SettingsButton)
        # Stop Button
#         self.stopButton = Button(text = 'Stop', on_press=self.stop)
#         self.stopButton.background_normal = ''
#         self.stopButton.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667]
#         self.add_widget(self.stopButton)
        # plot button
        self.plotButton = Button(text = 'Plot', on_press=self.plot)
        self.plotButton.background_normal = ''
        self.plotButton.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667]
        self.add_widget(self.plotButton)
        #save button
        self.saveButton = Button(text = 'Save', on_press = self.save)
        self.saveButton.background_normal = ''
        self.saveButton.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667]
        self.add_widget(self.saveButton)
        #threadTest
        self.threadTest = Button(text = 'Start', on_press = self.thread)
        self.threadTest.background_normal = ''
        self.threadTest.background_color = [0.0, 0.903225806451613, 1.0, 0.4666666666666667]
        self.add_widget(self.threadTest)
        
        # text inputs and labels as a sub gridlayout
        self.LambInp = GridLayout(cols=2)
        self.LambInp.add_widget(Label(text='Min Lambda \n (microns)'))
        self.minLamb = TextInput( multiline=True)
        self.LambInp.add_widget(self.minLamb)
        self.LambInp.add_widget(Label(text='Max Lambda \n (microns)'))
        self.maxLamb = TextInput( multiline=True)
        self.LambInp.add_widget(self.maxLamb)
        self.add_widget(self.LambInp)
        
        
        
    def save(self, i):
        '''
        Soves the current data to a CSV
        '''
        if self.saucier != None:
            self.saucier.saveData()
        else:
            title = "Save Error"
            text  = "Data collection not initiated"
            p = mp.Process(target = displayError, args =(title, text) )
            p.start()
            p.join()
            
    def plot(self, i):
        '''
        Plots the current data in an Interactive plot
        '''
        if self.saucier != None:
            self.saucier.plot()
        else:
            title = "Plot Error"
            text  = "Data collection not initiated"
            p = mp.Process(target = displayError, args =(title, text) )
            p.start()
            p.join()
        
    def connect(self,i):
        '''
        Creates new DataCollector and creates two new threads to connect to the arduino and motor simultaneously
        '''
        self.saucier = DataCollecter.DataCollecter(False)
        self.maxLamb.text  = "2.1"
        self.minLamb.text = "1.4"
        thread.start_new_thread(self.saucier.connectArd,())
        thread.start_new_thread(self.saucier.connectMotor,())

    def start(self,i):
        '''
        Checks if there is a dataCollector and begins a defualt scan that moves in steps
        (slow and steps have round off error)
        '''
        if self.saucier != None :
            thread.start_new_thread(self.saucier.collectData, (0.0, 25.0, 2000, True))
        else:
            print "CONNECT FIRST"
            
            
    def settings(self,i):
        if self.saucier != None:
            self.saucier.arduino.createSettingsFiles()
            self.saucier.arduino.writeSettingsFiles()
        else:
            title = "Settings Error"
            text  = "Attempt to Connect First"
            p = mp.Process(target = displayError, args =(title, text) )
            p.start()
            p.join()
            
        
    def thread(self,i):
        '''
        Takes the min and max input and runs a continous scan over the range
        '''
        if self.saucier != None:
            if self.saucier.arduino != None and self.saucier.motor != None:
                if self.saucier.arduino.connectFailed == False and self.saucier.motor.connectFailed == False:
                    max = float(self.maxLamb.text)
                    min = float(self.minLamb.text)
                    if min>=.8 and max<=2.3:
                        thread.start_new_thread(self.saucier.CollectDataCont,(min,max))
                    else:
                        title = "Range Error"
                        text  = "Outside range of Spectrometer"
                        p = mp.Process(target = displayError, args =(title, text) )
                        p.start()
                        p.join()
                else:
                    title = "Connection Error"
                    text  = "Arduino and Motor are still not connected"
                    p = mp.Process(target = displayError, args =(title, text) )
                    p.start()
                    p.join()
            else:
                title = "Connection Error"
                text  = "Connect to Arduino and Motor First"
                p = mp.Process(target = displayError, args =(title, text) )
                p.start()
                p.join()
        else:
            title = "Connection Error"
            text  = "Connect to Arduino and Motor First"
            p = mp.Process(target = displayError, args =(title, text) )
            p.start()
            p.join()
        
            
class ThreadGooy(App):
    '''
    This is the app which contains the GUI.
    the GUI runs as a loop that iterates over event checks which check whether or not a button has been pressed
    '''
    def __init__(self, **kwargs):
        super(ThreadGooy, self).__init__(**kwargs)
        
    def build(self):
        return Menu() #App builds the menu we originally created
     
     
    
if __name__ == '__main__': # this is were the program actually beings running
    mp.freeze_support() # must be used when multiprocessing is used on windows
    ThreadGooy().run() # Runs the GUI
    
    
    