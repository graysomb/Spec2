'''
Created on Dec 8, 2015

@author: graysomb
'''
from PyAPT import APTMotor
import Tkinter
import tkMessageBox
import ErrorHandler
import multiprocessing as mp

class MotorController(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        
        correct serial number:
        old 83863559
        83815746
        '''
        self.connectFailed = False
        try:
            self.Motor1 = APTMotor(83863559, HWTYPE=31)
            print self.Motor1.getHardwareInformation()
            print self.Motor1.getStageAxisInformation()
            print self.Motor1.getVelocityParameters()
#             self.degreeConv = 15.0156077
            self.degreeConv = 1
            self.Motor1.setVelocityParameters(0.0, 5.0, 5.99976)
            print self.Motor1.getVelocityParameters()
        except Exception as e:
            import ThreadedGUI
            self.connectFailed = True
            title = "Motor Connection Error"
            text = "Motor connection failed, make sure it is connected"
            p = mp.Process(target = ThreadedGUI.displayError, args =(title, text) )
            p.start()
            p.join()
    
    
    def moveMotor(self, ang):
        self.Motor1.mcRel(ang/self.degreeConv,5.99976)
#         ans = self.Motor1.getPos()*self.degreeConv
#         return ans
        return 1
    
    def Home(self):
        self.Motor1.go_home()
        return True
    
    def BlinkSomeLights(self):
        self.Motor1.identify()
        return True
    
    def getPosition(self):
        return self.Motor1.getPos()*self.degreeConv
    
    def moveTo(self, ang):
        return self.Motor1.mAbs(ang/self.degreeConv)*self.degreeConv
        