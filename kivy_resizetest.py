# To change the kivy default settings
# we use this module config
from kivy.config import Config
 
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)
 
# import kivy module
import kivy
 
# this restrict the kivy version i.e
# below this kivy version you cannot use the app
kivy.require("1.9.1")
 
# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App
 
# if you not import label and use it through error
from kivy.uix.label import Label
 
# defining the App class
class MyLabelApp(App):
    def build(self):
        # label display the text on screen
        # markup text with different colour
        l2 = Label(text ="[color = ff3333][b]Hello !!!!!!!!!!![/b] [color]\n [color = 3333ff]GFG !!:):):):)[/color]",
                   font_size ='20sp', markup = True)    
        return l2
     
# creating the object
label = MyLabelApp()
 
# run the window
label.run()
