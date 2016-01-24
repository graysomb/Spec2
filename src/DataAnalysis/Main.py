'''
Created on Sep 20, 2015

@author: graysomb
'''
import serial
import arduino_sketch
from subprocess import call
import numpy as np
import time
import matplotlib.pyplot as plt
from DataAnalysis import Arduino, MotorController
if __name__ == '__main__':
    pass

''' Arduino Test'''
# robit = Arduino.Arduino()
# print robit.testConnection()

'''motor test'''

# motor = MotorController.MotorController()
# start = time.clock()
# motor.moveMotor(20.0/700.0)
# print time.clock()-start

nam = input('Enter your filename: ')



''' GARBAGE'''

# path = "C:\Users\graysomb\Documents\Arduino\Voltmeter\Voltmeter2\ReadAnalogVoltage\ReadAnalogVoltage.ino"
# command = ["cd", "C:\Program Files (x86)\Arduino", "&&", "arduino", "--board", "arduino:sam:due", "--port", "COM6", "--upload", path]
# call(command, shell = True)
# 
# baudrate = 250000
# run =1
#  
# ser = serial.Serial("COM6",baudrate)
# connected = False
# while not connected:
#     serin = ser.read()
#     connected = True;
#     print("Connected")
#       
#       
# start = time.clock()
# ans=[]
# t=0
# totalT = 700;
# while t<totalT:
#     ans.append( ser.readline())
#     t = time.clock()-start
#   
# # print(ans)
# # print("time: ")
# # print(t)
# print("Done Read")
# 
# 
# dataList=[];
# errorNum = 0
# for i in range(len(ans)):
#     value = ans[i]
#     data = "";
#     for j in range(len(value)):
#         if (value[j] == '1' or value[j] == '2' or value[j] == '3' or value[j] == '4' or value[j] == '5' or value[j] == '6' or value[j] == '7' or value[j] == '8' or value[j] == '9' or value[j] == '0'):
#             data = data+value[j]
#         else:
#             break
#     if data =='':
#         dataList.append(0)
#     else:
#         dataList.append(int(data))
# 
# print("Done Conversion")
# 
# np.savetxt('C:\Users\graysomb\Desktop\Spectrometer\Spectometer\Data'+'_'+str(len(ans)/t)+'_Speed_'+str(run)+'.txt', dataList, delimiter=',')
# print("Donzo")
# Intensity  = np.array(dataList)
# x = np.arange(1,len(dataList)+1,1)
# plt.plot(x,Intensity)
# plt.show()