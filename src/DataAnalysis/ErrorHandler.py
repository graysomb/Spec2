'''
Created on Feb 4, 2016

@author: graysomb
'''
import Tkinter
import tkFileDialog
import os
import tkSimpleDialog
import tkMessageBox

class ErrorHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.root = Tkinter.Tk()
        self.root.withdraw()
        
    def displayError(self, titl, error):
        self.root.quit()
        self.root = Tkinter.Tk()
        self.root.withdraw()
        tkMessageBox.showerror( parent = self.root, title = titl, message = error)
    
    def getText(self, titl, text):
        self.root.quit()
        self.root = Tkinter.Tk()
        self.root.withdraw()
        return tkSimpleDialog.askstring(parent = self.root, title = titl, message = text)
    
    def getDir(self, titl):
        self.root.quit()
        self.root = Tkinter.Tk()
        self.root.withdraw()
        currdir = os.getcwd()
        tempdir = tkFileDialog.askdirectory(parent = self.root, initialdir=currdir, title = titl)
        return tempdir
        
