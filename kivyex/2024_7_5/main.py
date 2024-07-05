from kivy.app import App
from kivy.lang import Builder

kv_string = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        size_hint: (1, 0.2)
        Button:
            text: "start timer!"
        Button:
            text: "cancel timer"
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: "hoursbuttonID"
            text: "hours"
        Button:
            id: "minutesbuttonID"
            text: "minutes"
        Button:
            id: "secondsbuttonID"
            text: "seconds"
'''

class smApp(App):
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    smApp().run()
