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
        on_release: root.start_timer_once()
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: "hoursbuttonID"
            text: "Every 30 seconds: "
        Button:
            id: "minutesbuttonID"
            text: "every 10 seconds: "
        Button:
            id: "secondsbuttonID"
            text: "every second: "
CustomBoxLayout:
'''

class CustomBoxLayout():
    seconds = 0
    ten_seconds = 0
    thirty_seconds = 0

    # def start_timers(self, *args):
    #     Clock.schedule_interval(updatecount, 1)
    #     Clock.schedule_interval(updatecountpartial, 10)
    #     Clock.schedule_interval(updatecountlambda, 30)

    def start_timer_once(self, *args):
        Clock.schedule_once(self.updatecount, 5)

    def updatecount(self, *args):
        self.seconds += 1
        self.ten_seconds += 1
        self.thirty_seconds += 1
    
    def updatecountpartial(self, *args):
    def updatecountlambda(self, *args):

class smApp(App):
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    smApp().run()
