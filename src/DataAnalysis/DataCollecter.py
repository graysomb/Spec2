'''
Created on Dec 8, 2015

@author: Michael Grayson

'''
# See GUI for notes on imports
import Arduino
import MotorController
import time
import numpy as np
import dateutil
import matplotlib.pyplot as plt
import multiprocessing as mp
import thread
import threading
import serial

class DataCollecter(object):
    '''
    This is the class that handles data collection and motor control. 
It also handles the data once it has been captured.
    '''


    def __init__(self,connect):
        '''
        Creates Lists for each variable and if connect is True, connects to both the arduino and the Motor
        '''
        self.motorData = []
        self.lightData = []
        self.lamb = []
        self.arduino = None
        self.motor = None
        if connect == True:
            self.motor = MotorController.MotorController()
            self.arduino  = Arduino.Arduino(True)
        
    def connectMotor(self):
        '''
        Creates a new motor object which can controll the motor and is connected to it
        '''
        self.motor = MotorController.MotorController()
        
    def connectArd(self):
        '''
        creates a new arduino and Loads the arduino script onto it
        '''
        self.arduino  = Arduino.Arduino(True) # if arduino is passed false it will connect but will not load the arduino script
        
    def collectData(self, start,stop,steps,thread):
        '''
        Collects data in discrete steps
        The motor moves the predefined step size and then data is taken from the arduino
        This function suffers from slow collection time and round off in angle steps
        '''
        self.motor.moveTo(self.LambdaToTheta(1.61593))
        self.motor.moveMotor(-22.3175)
#         while True:
#             self.motor.moveTo(21.00)
#             self.motor.moveTo(23.00)
        
        
        
        dlam = (stop-start)/steps
#         self.arduino.readDataDisc()
#         self.arduino.readDataDisc()
#         self.arduino.readDataDisc() # flush out serial line
#         for i in range(steps):
#             self.lamb.append(start+dlam*i)
#             self.takeData(dlam) # get the data from the motor and arduino
#             print float(i)/steps # print how far the loop has gotten
#         if thread == False: # return the data if not in a thread.
#             return [self.lightData,self.lamb,self.motorData]
    
    def takeData(self,dlam):
        '''
        Take data from the arduino and motor and time how long it takes
        data is saved by appending to self variables
        '''
        start = time.clock()
        self.lightData.append(float(self.arduino.readDataDisc())) # converts arduino data which is a string to a float and adds it
        end = time.clock()
        print "time ard:"
        print end-start # print how long that took
        start = time.clock()
        self.motorData.append(self.motor.moveMotor(dlam)) # move the motor dlam and read the position.
        end = time.clock()
        print "time mot:"
        print end-start # print how long it took
        
    def test(self):
        '''
        Test the connection of both the arduino and Motor
        '''
        print self.arduino.testConnection() # arduino will return "Roger"
        print self.motor.BlinkSomeLights() # motor will blink the light on the motor controller
        

    def saveData(self):
        '''
        ask for the name of the data and saves the data as three comma seperated files
        Name input must be a string
        '''
        if self.lightData != [] and self.lamb != [] and self.motorData != []:
#             name = input('Enter your filename: ') # asks for the file name
            import ThreadedGUI
            import os
            titl = "Save"
            text  = "Enter a filename"
            Q = mp.Queue()
            p = mp.Process(target = ThreadedGUI.getText(titl, text, Q))
            p.start()
            name = Q.get()
            p.join()
            dir = os.getcwd()
            np.savetxt(dir+'\ ' -' '+ name+'_light' +'.txt', self.lightData, delimiter=',') # saves the intensity data
            np.savetxt(dir+'\ ' -' ' + name+'_lamb' +'.txt', self.lamb, delimiter=',') # saves the lambda data
            np.savetxt(dir+'\ ' -' ' + name+'_motor' +'.txt', self.motorData, delimiter=',') # saves the angle data
#             np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'_light' +'.txt', self.lightData, delimiter=',') # saves the intensity data
#             np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'_lamb' +'.txt', self.lamb, delimiter=',') # saves the lambda data
#             np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'_motor' +'.txt', self.motorData, delimiter=',') # saves the angle data
            print("Donzo")
        else:
            import ThreadedGUI
            title = "Data Save Error"
            text  = "No data to save"
            p = mp.Process(target = ThreadedGUI.displayError, args =(title, text) )
            p.start()
            p.join()
    def plot(self):
        '''
        plots the data collected over lambda
        '''
        plt.plot(self.lamb,self.lightData)
        plt.show()

#         length = len(self.lightData)
#         print length
#         plt.plot(np.transpose(np.linspace(0, length, length)), self.lightData)
#         plt.show()
        
    def CollectDataCont(self,start,stop):
        '''
        Collects data continously in multiple threads as the motor moves at .01 degrees per second
        and plots it in another subprocess 
        '''
        self.lightData = []
        self.motorData = []
        self.lamb = []
        angStop = self.LambdaToTheta(stop)
        angStart = self.LambdaToTheta(start)
        print angStop
        print angStart

        self.motor.moveTo(angStart) # move the motor to the start of the range in degrees
        ang = angStop-angStart # calculate the angle to move over

        self.arduino.readDataDisc()
        self.arduino.readDataDisc()
        self.arduino.readDataDisc()# flush out the serial line
        
        
        
        thread.start_new_thread(self.motor.Motor1.mcRel,(ang,0.05)) # begin moving hte motor in one thread
        thread.start_new_thread(self.ThreadCollect, (angStart,angStop,True)) # begin collecting data in another

        # used to collect arduino data in another subprocess, has more data points, but also more noise
#         self.arduino.arduino.close()
#         thread.start_new_thread(self.motorThreadCollect, (start, stop))
        
        
    def thetaToLamba(self,theta):
        '''
        converts degrees to microns using the grating equation and a calibration angle
        This is the angle between the grating and the concave mirror
        '''
        self.calAng = 0.09117894270
        thetaNP = np.array(theta)
        ThetaRadNP = np.deg2rad(thetaNP)
        lamNP = np.divide(np.sin(ThetaRadNP-self.calAng)+np.sin(self.calAng + ThetaRadNP),0.6)
        return lamNP

    def LambdaToTheta(self,lamb):
        '''
        converts lambda in microns to degrees using a taylor approximation to the solution of the grating equation for theta
        '''
        theta = 31.93825809+20.40947690*(lamb-1.750)+2.265992195*(lamb-1.750)**2+0.9347877972*(lamb-1.750)**3 # taylor expansion
        return theta
    
    
    def ThreadCollect(self, angStart,angStop, plot):
        '''
        the threaded version of data collection meant for using with continous motor movement. 
        Continously collects data from the motor and arduino while the motor has not reached the end of its motion.
        If plot is true it generates a subprocces which plots the data
        ''' # Convert lambda to theta
        
        if plot == True: # this starts plotting the data in a separate process so it does not slow data capture
            import ThreadedGUI # import method for threading
            parent_lightPipe, child_lightPipe=mp.Pipe() # create pipes for data
            parent_angPipe, child_angPipe = mp.Pipe()
            p = mp.Process(target = ThreadedGUI.plotData, args = (parent_lightPipe, parent_angPipe)) # target function
            p.start() # start process
        
        ang = self.motor.Motor1.getPos()
        while angStop>(ang+.01) : # While the motor has not reached its final destination
            print 100*(1-(angStop-ang)/(angStop-angStart)) # print progress
            ang = self.motor.Motor1.getPos() # get the motor angle
            light = float(self.arduino.readDataDisc()) # get the arduino reading
            self.lightData.append(light) # save both data points
            self.motorData.append(ang)
            if plot == True:
                child_angPipe.send(ang) # send data over the pipes to plot
                child_lightPipe.send(light)
            
        if plot == True:
            p.terminate() # kill the plot process
            
        self.lamb = self.thetaToLamba(self.motorData) # covert thetas to lambdas
        print "size:"
        print len(self.motorData) # print number of points
        
    def motorThreadCollect(self, angStart,angStop):
        '''
        This method is design to collect data from the motor and the arduino simultaneously to increase the number of data points.
        It is not complete
        '''
        import ThreadedGUI
        
        # arduino subprocess
        parent_lightPipe, child_lightPipe = mp.Pipe()
        parent_startPipe, child_startPipe = mp.Pipe()
        p = mp.Process(target = ThreadedGUI.SubArd, args = (child_lightPipe,child_startPipe))
        #monitors pipe
        p.start()
        

        #wait for arduino
        while parent_startPipe.recv() != True:
            print "waiting for Ard"
            pass
        
        # start collection
        thread.start_new_thread(self.motor.Motor1.mcRel,(angStop-angStart,0.1))
        ang = self.motor.Motor1.getPos()
        
        q = mp.Queue()
        p2 = mp.Process(target = ThreadedGUI.getData, args = (parent_lightPipe, q))
        p2.start()
        while angStop>(ang+.01) :
            print 100*(1-(angStop-ang)/(angStop-angStart))
            ang = self.motor.Motor1.getPos()
            self.motorData.append(ang)
            
        print p.is_alive()
        print "done angle"
        #kill arduino
        p.terminate()
        print "ard closed"
        child_lightPipe.send("end")
        
#         while parent_lightPipe.poll():
#             ans1 = parent_lightPipe.recv()
#             self.lightData.append(ans1)
        self.lightData = q.get()
        print "lightData length"
        print len(self.lightData)
        print "motorData length"
        print len(self.motorData)
        print "done Mot"
        
        
        
        
        