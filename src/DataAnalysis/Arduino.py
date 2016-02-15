'''
Created on Dec 8, 2015

@author: Michael Grayson
'''
from subprocess import call
import subprocess
import serial
import numpy as np
import time
import multiprocessing as mp


import Tkinter
import tkFileDialog
import os
import tkSimpleDialog
import tkMessageBox
import ErrorHandler

class Arduino(object):
    '''
    this controls connection to the arduino and collecting data
    '''


    def __init__(self,loadScript):
        '''
        Constructs the arduino, if loadscript is true then the arduino code will be loaded. 
        If the arduino has not been disconnected from the computer from the last load it will not need to be loaded again
        '''
        self.connectFailed = False
        
        try:
            self.loadSettingsFiles()
        except:
            self.createSettingsFiles()
            self.writeSettingsFiles()

#         self.path = "C:\Users\graysomb\Desktop\Spectrometer\Spectometer\CheckAndRead.ino\CheckAndRead.ino.ino"
#         self.ardPath = "C:\Program Files (x86)\Arduino"
#         self.COM = "6"
            
            
        if loadScript ==True:
            command = ["cd", self.ardPath, "&&", "arduino", "--board", "arduino:sam:due", "--port", "COM"+self.COM, "--upload", self.path]

            import ThreadedGUI
            p = subprocess.Popen(command,stdout=subprocess.PIPE, shell = True)
            parent_comPipe, child_comPipe = mp.Pipe()
            p2 = mp.Process(target =ThreadedGUI.displayCon, args = (child_comPipe,) )
            p2.start()
            while p.poll()==None:
                ans = p.communicate()[0]
                parent_comPipe.send(ans)
            p2.terminate()
#             subprocess.check_output(command, shell = True)
            print "Loaded"
        
        
        self.dataList = []
        baudrate = 250000
        
        try:
            self.arduino = serial.Serial("COM6",baudrate,timeout=1)
            connected = False
            while not connected:
                serin = self.arduino.read()
                connected = True;
            print("Connected")
        except serial.serialutil.SerialException as e:
            print e
            import ThreadedGUI
            self.connectFailed = True
            title = "Arduino Connection Error"
            text = "Could not connect to COM"+self.COM+" make sure Arduino is connected \n and is at the correct COM"
            p = mp.Process(target = ThreadedGUI.displayError, args =(title, text) )
            p.start()
            p.join()
    
    def readDataCont(self, readTime):
      
      
        start = time.clock()
        ans=[]
        t=0
        totalT = readTime;
        while t<totalT:
            ans.append( self.arduino.readline())
            t = time.clock()-start
  
        print("Done Read")


        for i in range(len(ans)):
            value = ans[i]
            data = "";
            for j in range(len(value)):
                if (value[j] == '1' or value[j] == '2' or value[j] == '3' or value[j] == '4' or value[j] == '5' or value[j] == '6' or value[j] == '7' or value[j] == '8' or value[j] == '9' or value[j] == '0'):
                    data = data+value[j]
                else:
                    break
            if data =='':
                self.dataList.append(0)
            else:
                self.dataList.append(int(data))

        return self.dataList
    
    def readDataDisc(self):
        self.arduino.write("1")
        ans = self.arduino.readline()
#         print [ans]
        return ans
        
        
    def saveData(self):
        name = input('Enter your filename: ')
        np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'.txt', self.dataList, delimiter=',')
        print("Donzo")
        
    def testConnection(self):
        self.arduino.write("0")
        ans = self.arduino.readline()
        print ans
    
        
    def askForPath(self):
        import ThreadedGUI
        Q = mp.Queue()
        titl = "Locate Arduino Script Path"
        p = mp.Process(target =ThreadedGUI.getDir , args = ( titl,Q))
        p.start()
        ans = Q.get()
        p.join()
        if len(ans)>0:
            self.path = ans+"/CheckAndRead.ino.ino"
            print ans
            
    def askForArdPath(self):
        import ThreadedGUI
        Q = mp.Queue()
        titl = "Locate Arduino Program Path"
        p = mp.Process(target =ThreadedGUI.getDir , args = ( titl,Q))
        p.start()
        ans = Q.get()
        p.join()
        if len(ans)>0:
            self.ardPath = ans
            print ans
            
    def askForCom(self):
        import ThreadedGUI
        Q = mp.Queue()
        titl = "COM"
        text = "Enter Arduino COM Port Number"
        p = mp.Process(target =ThreadedGUI.getText , args = ( titl,text,Q))
        p.start()
        ans = Q.get()
        p.join()
        if len(ans)>0:
            self.COM = ans
            
    def testConntection(self):
        baudrate = 250000
        
        try:
            self.arduino = serial.Serial("COM6",baudrate,timeout=1)
            connected = False
            while not connected:
                serin = self.arduino.read()
                connected = True;
            print("Connected")
        except serial.serialutil.SerialException as e:
            print e
        return connected
    
    def createSettingsFiles(self):
        np.savetxt('ardScriptPath.txt',[])
        np.savetxt('ardPath.txt',[])
        np.savetxt('comNum.txt',[])
    
    def loadSettingsFiles(self):
        f1 = open('ardPath.txt', 'r')
        self.ardPath = f1.readline()
        f1.close()
        f2 = open('ardScriptPath.txt', 'r')
        self.path = f2.readline()
        f2.close()
        f3 = open('comNum.txt','r')
        self.COM = f3.readline()
        f3.close()
    
    def writeSettingsFiles(self):
        self.askForCom()
        self.askForPath()
        self.askForArdPath()
        f1 = open('comNum.txt','w')
        f1.write(self.COM)
        f1.close()
        f2 = open('ardScriptPath.txt', 'w')
        f2.write(self.path)
        f2.close()
        f3 = open('ardPath.txt', 'w')
        f3.write(self.ardPath)
        f3.close()
        command = ["cd", self.ardPath, "&&", "arduino", "--install-boards", "arduino:sam"]
        subprocess.check_output(command, shell=True)
        

        