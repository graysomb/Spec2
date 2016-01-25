'''
Created on Dec 8, 2015

@author: graysomb
'''
from Cython.Shadow import NULL
from DataAnalysis import Arduino
from DataAnalysis import MotorController
import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
class DataCollecter(object):
    '''
    classdocs
    '''


    def __init__(self,connect):
        '''
        Constructor
        '''
        self.motorData = []
        self.lightData = []
        self.lamb = []
        if connect == True:
            self.motor = MotorController.MotorController()
            self.arduino  = Arduino.Arduino()
        
    def connectMotor(self):
        self.motor = MotorController.MotorController()
        
    def connectArd(self):
        self.arduino  = Arduino.Arduino()
        
    def collectData(self, start,stop,steps,thread):
        dlam = (stop-start)/steps
        self.arduino.readDataDisc()
        self.arduino.readDataDisc()
        self.arduino.readDataDisc()
        for i in range(steps):
            self.lamb.append(start+dlam*i)
            self.takeData(dlam)
        if thread == False:
            return [self.lightData,self.lamb,self.motorData]
    
    def takeData(self,dlam):
        start = time.clock()
        self.lightData.append(float(self.arduino.readDataDisc()))
        end = time.clock()
        print "time ard:"
        print end-start
        start = time.clock()
        self.motorData.append(self.motor.moveMotor(dlam))
        end = time.clock()
        print "time mot:"
        print end-start
        
    def test(self):
        print self.arduino.testConnection()
        print self.motor.BlinkSomeLights()
        
    def theta(self,lam):
        #add taylor expansion
        return lam
    def saveData(self):
        self.dataList = [self.lightData,self.lamb, self.motorData]
        name = input('Enter your filename: ')
        np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'.txt', self.dataList, delimiter=',')
        print("Donzo")
    def plot(self):
        plt.plot(self.lamb,self.lightData)
        plt.show()
        
    def CollectDataCont(self,start,stop):
        ang = stop-start
        
        #pipes for data
        parent_lightPipe, child_lightPipe = mp.Pipe()
        parent_angPipe, child_angPipe = mp.Pipe()
        
        #move process
        p1 = mp.Process(
                        target = self.motor.Motor1.mcRel, 
                        args = (ang,2.0))
        
        #read process
        p2 = mp.Process(target = self.ThreadCollect, args =(ang,child_angPipe,child_lightPipe))
        p1.start()
        p2.start()
        
        p2.join()
        
        ans1 = 0
        while ans1 != "end":
            ans1 = parent_lightPipe.recv()
            self.lightData.append(ans1)
            ans2 = parent_angPipe.recv()
            self.motorData.append(ans2)
        
        
    
    def TThreadCollect(self,ang,angPipe, lightPipe):
        start = time.clock()
        angPipe.send("end")
        lightPipe.send("end")
        while time.clock()-start<(ang/2.0):
            light = self.arduino.readDataDisc()
            ang = self.motor.Motor1.getPos()
            angPipe.send(ang)
            lightPipe.send(light)
        lightPipe.close()
        angPipe.close()
        
    def printStuff(self):
        print time.clock()
        
        