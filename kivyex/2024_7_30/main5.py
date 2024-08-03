import os
import psutil
from kivy import Config, platform
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout

os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'
if platform=="linux":
    Config.set('graphics', 'width', '480')
    Config.set('graphics', 'height', '1280')
    Config.set('graphics', 'rotation', '90')
    Config.set('graphics', 'resizable', True)
    Config.set('graphics', 'borderless', '0')
elif platform=="win":
    Config.set('graphics', 'width', '1280')
    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'rotation', '0')
    Config.set('graphics', 'resizable', True)
    Config.set('graphics', 'borderless', '0')
class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn = Button(text = "+",size_hint = (None, None),height = 50,width = 50,on_press = self.add_a_im)
        self.add_widget(btn)
        im = Image(size_hint = (None, None),height = 50,width = 50)
        self.add_widget(im)
        Clock.schedule_interval(self.add_a_im,1)
    def add_a_im(self,*args):
        im = Image(size_hint = (None, None),height = 50,width = 50)
        self.add_widget(im)
class IMTestApp(App):
    def build(self):
        return StackLayoutExample()
#this is to make the Kivy window always on top
from kivy.core.window import Window
Window.always_on_top = True
IMTestApp().run()