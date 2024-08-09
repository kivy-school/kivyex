from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

#kv language setting the main widget to be a button
kvString = '''
Button:
    text: "Hello world!"
'''
import sys
import pathlib

class MyApp(App):
    def build(self):
        self.title = 'Welcome to Kivy School!'
        if hasattr(sys, "_MEIPASS"):
            meipass_icon_path = str(pathlib.Path(sys._MEIPASS) / 'icons8-discord-48.png')
            self.icon = meipass_icon_path
            # print("?", meipass_icon_path)
        else:
            self.icon = 'icons8-discord-48.png'
        return Builder.load_string(kvString)


if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    #checking for errors and making sure the pyinstaller exe is open so I can read the code
    try:
        #run Kivy app
        MyApp().run()  
    except Exception as e:
        import traceback
        print("full exception", "".join(traceback.format_exception(*sys.exc_info())))
        import time
        time.sleep(10)