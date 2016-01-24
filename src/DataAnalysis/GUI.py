'''
Created on Dec 8, 2015

@author: graysomb
'''
import kivy
import time
from kivy.uix.gridlayout import GridLayout
kivy.require('1.0.7')
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from DataAnalysis import DataCollecter

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class Menu(GridLayout):
    
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.cols = 4
        self.saucier = None
        '''
        # maximum lambda input
        self.add_widget(Label(text='Max'))
        self.max = TextInput(multiline=False)
        self.add_widget(self.max)
        # minimum lambda input
        self.add_widget(Label(text='Min'))
        self.min = TextInput( multiline=False)
        self.add_widget(self.min)
        # step input
        self.add_widget(Label(text='steps'))
        self.step = TextInput( multiline=False)
        self.add_widget(self.step)
        '''
        # connect button
        self.connectButton = Button( text='Connect',
                        on_press=self.connect)
        self.add_widget(self.connectButton)
        # start button
        self.StartButton = Button( text='Start',
                        on_press=self.start )
        self.add_widget(self.StartButton)
        # plot button
        self.plotButton = Button(text = 'Plot', on_press=self.plot)
        self.add_widget(self.plotButton)
        #save button
        self.saveButton = Button(text = 'Save', on_press = self.save)
        self.add_widget(self.saveButton)
        
        
    def save(self, i):
        self.saucier.saveData()
    def plot(self, i):
        self.saucier.plot()
        
    def connect(self,i):
        self.saucier = DataCollecter.DataCollecter()
        
    def start(self,i):
        if self.saucier != None :
            start = time.clock()
            ans = self.saucier.collectData(0.0, 25.0, 2000)
            print time.clock()-start
            print ans
        else:
            print "CONNECT"

class Gooy(App):

        
    def build(self):
        return Menu()
    
        
        
if __name__ == '__main__':
    Gooy().run()