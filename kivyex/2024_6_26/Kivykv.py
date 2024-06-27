# https://kivy.org/doc/stable/guide/lang.html#how-to-load-kv
'''
By name convention:

Kivy looks for a Kv file with the same name as your App class in lowercase, minus “App” if it ends with ‘App’ e.g:

MyApp -> my.kv

If this file defines a Root Widget it will be attached to the App’s root attribute and used as the base of the application widget tree.

'''

from kivy.app import App
class hwkvApp(App):
    pass

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    hwkvApp().run()