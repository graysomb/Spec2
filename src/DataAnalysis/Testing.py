'''
Created on Oct 13, 2015

@author: graysomb
'''
import numpy as np
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

import Tkinter
import tkMessageBox
import os

import tkSimpleDialog



def f(child_conn):
    for i in range(1,1000):
        print i
        child_conn.send(i)
        
import kivy
from kivy.uix.gridlayout import GridLayout
kivy.require('1.0.7')
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker




# class ThreadGooy(App):

#     def __init__(self, **kwargs):
#         super(ThreadGooy, self).__init__(**kwargs)
        
#     def build(self):
#         return None


  
    
if __name__ == '__main__':
    pass

root = Tkinter.Tk()
var = Tkinter.StringVar()
var.set('buts')

l = Tkinter.Label(root, textvariable = var)
l.pack()
count = 0
while True:
    var.set(count)
    root.update_idletasks()
    count = count +1


# from Tkinter import *
# import subprocess as sub
# currdir = os.getcwd()
# print currdir
# from Tkinter import *
# import sys



#     root = Tkinter.Tk()
#     root.withdraw() #use to hide tkinter window
#     currdir = os.getcwd()
#     print os.getcwd()
#     tempdir = tkSimpleDialog.askstring("Wow", "what is your name")
#     if len(tempdir) > 0:
#         print "You chose %s" % tempdir
#          
#     tkMessageBox.showerror("wow", tempdir+" fucking sucks")
     





#     parent_conn, child_conn = mp.Pipe()
#     p = mp.Process(target=f, args=(child_conn,))
#     p.start()
#     time.sleep(2)
#     while parent_conn.poll():
#         print parent_conn.recv()
#         
        
    

# '''
# x = np.linspace(0, 6*np.pi, 100)
# y = np.sin(x)
# 
# # You probably won't need this if you're embedding things in a tkinter plot...
# plt.ion()
# 
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma
# 
# for phase in np.linspace(0, 10*np.pi, 500):
#     line1.set_ydata(np.sin(x + phase))
#     fig.canvas.draw()
# '''
    
    
    