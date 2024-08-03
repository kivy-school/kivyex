from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

#kv language setting the main widget to be a button
kvString = '''
Button:
    text: "Hello world!"
'''

class MyApp(App):
    def build(self):
        self.icon = 'icons8-discord-48.png'
        return Builder.load_string(kvString)


if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    #run Kivy app
    MyApp().run()