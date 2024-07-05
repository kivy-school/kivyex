from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

kv_string = '''
<CustomBoxLayout@BoxLayout>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        size_hint: (1, 0.2)
        Button:
            text: "start timer!"
        Button:
            text: "cancel timer"
    Button:
        size_hint: (1, 0.2)
        text: "timer only once"
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: "hoursbuttonID"
            text: "30 seconds"
        Button:
            id: "minutesbuttonID"
            text: "10 seconds"
        Button:
            id: "secondsbuttonID"
            text: "seconds"
'''

class CustomBoxLayout():
    def start_timers(self, *args):
        Clock.schedule_interval(updatecount, 1)
        Clock.schedule_interval(updatecount, 10)
        Clock.schedule_interval(updatecount, 30)

    def start_timer_once(self, *args):
        Clock.schedule_once(my_callback, 5)

class smApp(App):
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    smApp().run()
