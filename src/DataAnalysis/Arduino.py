'''
Created on Dec 8, 2015

@author: graysomb
'''
from subprocess import call
import serial
import numpy as np
import time
import multiprocessing as mp
class Arduino(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        path = "C:\Users\graysomb\Desktop\Spectrometer\Spectometer\CheckAndRead.ino\CheckAndRead.ino.ino"
        command = ["cd", "C:\Program Files (x86)\Arduino", "&&", "arduino", "--board", "arduino:sam:due", "--port", "COM6", "--upload", path]
        subCall = call(command, shell = True)
#         This might work
        subCall.check_call() 
        time.sleep(20)
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
#         for i in range(len(ans)):
#             value = ans[i]
#             data = "";
#             for j in range(len(value)):
#                 if (value[j] == '1' or value[j] == '2' or value[j] == '3' or value[j] == '4' or value[j] == '5' or value[j] == '6' or value[j] == '7' or value[j] == '8' or value[j] == '9' or value[j] == '0'):
#                     data = data+value[j]
#                 else:
#                     break
#             if data =='':
#                 self.dataList.append(0)
#             else:
#                 self.dataList.append(int(data))
#   
        print [ans]
        return ans
        
        
    def saveData(self):
        name = input('Enter your filename: ')
        np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\ '+name+'.txt', self.dataList, delimiter=',')
        print("Donzo")
        
    def testConnection(self):
        self.arduino.write("0")
        ans = self.arduino.readline()
        print ans
    
        
        