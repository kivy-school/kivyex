from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from functools import partial

kv_string = '''
<CustomBoxLayout@BoxLayout>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        size_hint: (1, 0.2)
        Button:
            text: "start timer!"
            on_release: root.start_timers()
        Button:
            text: "cancel timer"
            on_release: root.cancel_all_timers()
    Button:
        size_hint: (1, 0.2)
        text: "timer only once in 5 seconds"
        on_release: 
            root.start_timer_once()
    Button:
        size_hint: (1, 0.2)
        text: "failed lambda example that will crash the app"
        on_release: 
            root.lambdafail()
    Button:
        size_hint: (1, 0.2)
        text: "working lambda example that increases 30 seconds"
        on_release: 
            root.lambdapass()
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'horizontal'
            Label: 
                text: "Every 30 seconds: "
            Button:
                id: thirtybuttonID
                text: str(root.thirty_seconds)
        BoxLayout:
            orientation: 'horizontal'
            Label: 
                text: "Every 10 seconds: "
            Button:
                id: tenbuttonID
                text: str(root.ten_seconds)
        BoxLayout:
            orientation: 'horizontal'
            Label: 
                text: "Every seconds: "
            Button:
                id: secondsbuttonID
                text: str(root.seconds)
CustomBoxLayout:
'''

class CustomBoxLayout(BoxLayout):
    seconds = NumericProperty(0)
    ten_seconds = NumericProperty(0)
    thirty_seconds = NumericProperty(0)

    def start_timers(self, *args):
        # self.single = Clock.schedule_interval(
        #     self.update_specific(), 1)
        self.single = Clock.schedule_interval(
            partial(self.update_specific, clockID = "single"), 1)
        self.ten =  Clock.schedule_interval(
            partial(self.update_specific, clockID = 'ten'), 10)
        self.thirty = Clock.schedule_interval(
            partial(self.update_specific, clockID = 'thirty'), 30)
    
    def cancel_all_timers(self, *args):
        if "single" in dir(self): 
            self.single.cancel()
        if "ten" in dir(self): 
            self.ten.cancel()
        if "thirty" in dir(self): 
            self.thirty.cancel()
        
    def start_timer_once(self, *args):
        Clock.schedule_once(self.updatecount, 5)

    def lambdafail(self): 
        self.lambdafail = Clock.schedule_interval(
            partial(self.lambdaexample, clockID = 'thirty'), 1)
    
    def lambdapass(self): 
        self.lambdapass = Clock.schedule_interval(
            lambda dt: self.lambdaexample(clockID = 'thirty'), 1)

    def lambdaexample(self, **kwargs):
        # *args is an easy way to accept the dt argument that is provided when using clock
        # this function does not have *args, and will fail if you try to use clock schedule and partial:
        # if you do not have access to the function (it's from some library that you do not want to modify), the simple answer is to use a lambda that passes dt as a variable
        if "clockID" in kwargs.keys(): 
            if kwargs['clockID'] == "thirty":
                self.thirty_seconds += 1
        else: 
            print("the function failed because it does not accept the dt arg: check for yourself. by adding *args to lambdaexample like this: def lambdaexample(self, *args, **kwargs): there will be 2 positional arguments, args = (1.0904659999941941,) and kwargs = {'clockID': 'thirty'} ")
        import pdb
        pdb.set_trace
        

    def update_specific(self, *args, **kwargs):
        import pdb
        pdb.set_trace()
        if 'clockID' in kwargs.keys():
            if kwargs['clockID'] == "single":
                self.seconds += 1
            elif kwargs['clockID'] == "ten":
                self.ten_seconds += 1
            elif kwargs['clockID'] == "thirty":
                self.thirty_seconds += 1
        else: 
            #default is to update all:
            self.seconds += 1
            self.ten_seconds += 1
            self.thirty_seconds += 1


    def updatecount(self, *args):
        self.seconds += 1
        self.ten_seconds += 1
        self.thirty_seconds += 1
        print("updated counts:", self.seconds, self.ten_seconds, self.thirty_seconds)
        # import pdb
        # pdb.set_trace()
    
    def updatecountpartial(self, *args):
        pass
    
    def updatecountlambda(self, *args):
        pass

class smApp(App):
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    smApp().run()
