from kivy.app import runTouchApp
from kivy.lang import Builder
kvString = '''
Button:
    text: "Hello world!"
'''
runTouchApp(Builder.load_string(kvString))
