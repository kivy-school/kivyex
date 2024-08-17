# https://www.reddit.com/r/kivy/comments/1epwbh1/i_want_to_create_an_lcars_gui_for_my_project_but/
'''
stupid's guide to cool GUI
draw image 
fill image with clickable buttons

problem:
it should actually be drawn with canvas instructions, this is because pngs are not the best when rescaled

- Use RelativeLayout because it moves the children (aka buttons) correctly when the window is resized

- to see the button, draw a x and start manually moving

- use DP!, kivy's density independent pixels, that way it looks the same on any device

- the struggle will be manually sizing the buttons on the layout based on the layoutsize (which is root.size in this case). not impossible, just tedious

-left the red backgrounds because that's how I see the buttons when manually moving

- I cheated and used kivy-loader

- (NOT NECESSARY) modify the background_X properties if you want button responsiveness (incorrect, to remove the original button just do `background_color = 0, 0, 0, 0`)

- to make bg color of a button transparent just set: 
background_color: 0, 0, 0, 0 in KV
background_color = 0, 0, 0, 0 in python (because it's a property)

- I used microsoft powertoys START+SHIFT+C to get the correct rgba color from ur reference image

- kivy sometimes is reverse (aka BGR instead of RGB) (was a problem when setting textcolors, it's BGR format)

- i used kivy reloader because restarting the app every second hurt my fingers

- # calculate stardate from this repo
# https://github.com/Goddard/stardate/blob/master/stardate/stardate.py

- how i got the font: 
https://www.thelcars.com/fonts.php
https://fonts.google.com/specimen/Antonio

'''

# from kivy_reloader.app import App
from kivy.app import App
# import trio
# from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty
import time
from kivy.clock import Clock

# calculate stardate from this repo
# https://github.com/Goddard/stardate/blob/master/stardate/stardate.py

import math
from dateutil.parser import parse
from datetime import datetime
import sys
import argparse
import time
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter

class StarDate():
    verbose = False
    date = None
    stardate = None

    def __init__(self, date=None, verbose=False):
        if(self.verbose):
            print("---Initializing---")

        self.date = date
        self.verbose = verbose

    def setDate(self, date):
        self.date = date

    def to_seconds(self, date):
        return time.mktime(date.timetuple())

    def getStardate(self):
        # print("self date", self.date)
        if(self.date != None):
            stardateRequested = parse(self.date)
        else:
            stardateRequested = datetime.now()

        stardateOrigin = parse("1987-07-15T00:00:00-00:00")

        if(self.verbose):
            print("Start Date : " + stardateRequested.strftime('%Y-%m-%d %H:%M:%S'))
            print("Origin Date : " + stardateOrigin.strftime('%Y-%m-%d %H:%M:%S'))
            print("---------------------")

        if(self.verbose):
            year = stardateRequested.strftime('%Y')
            month = stardateRequested.strftime('%m')
            day = stardateRequested.strftime('%d')
            hour = stardateRequested.strftime('%H')
            minutes = stardateRequested.strftime('%M')
            seconds = stardateRequested.strftime('%S')
            print("Year : " + year)
            print("Month : " + month)
            print("Day : " + day)
            print("Hour : " + hour)
            print("Minutes : " + minutes)
            print("Seconds : " + seconds)
            print("---------------------")

        self.stardate = self.to_seconds(
            stardateRequested) - self.to_seconds(stardateOrigin)
        self.stardate = self.stardate / (60.0 * 60.0 * 24.0 * 0.036525)
        self.stardate = math.floor(self.stardate + 410000.0)
        self.stardate = self.stardate / 10.0

        if(self.verbose):
            print("Selection Date - Origin Date = " + str(self.stardate))
            print("---------------------")

            print("Previous Value / (60.0 * 60.0 * 24.0 * 0.036525) = " +
                  str(self.stardate))
            print("---------------------")

            print("Floor(Previous Value + 410000.0) = " + str(self.stardate))
            print("---------------------")

            print("Previous Value / 10.0 = " + str(self.stardate))
            print("---------------------")

        if(self.verbose):
            print()
            print("Stardate Final : " + str(self.stardate))

        return self.stardate

    def main(self):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument(
                '-v', '--verbose', help='if you want to see more variables and the calculation process', action='store_true')
            parser.add_argument(
                '-d', '--date', help='Enter the date to convert to stardate, format YYYY-MM-DD', metavar='D', type=str, default=None)
            args = parser.parse_args()

            self.verbose = args.verbose
            self.date = args.date

            if(self.verbose):
                print("Argument Verbose : " + str(self.verbose))
                if(self.date != None):
                    print("Argument Date : " + self.date)
                else:
                    print("Argument Date : " +
                          datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print()

            self.getStardate()

        except SystemExit:
            e = sys.exc_info()[0]
            # if(self.verbose):
            print(e)


kvstring = '''
#:import time time

<CustomButton@Button>:
    background_normal: ''
    background_down: ''
    background_disabled_normal: ''
    background_disabled_down: ''

<CustomLayout>:
    id: mainRL_ID
    canvas:
        Rectangle:
            source: 'LCARSBLANK.png'
            size: self.parent.size if self.parent is not None else self.size
    # CustomButton:
    CustomButton:
        canvas.after:
            Color:
                rgba: 1, 0, 0, 0.5
            Rectangle:
                size: self.size
                pos: self.pos
        font: 'Antonio-VariableFont_wght.ttf'
        text: 'MOZILLA FIREFOX'
        text_size: self.size
        color: 1,0,1,1
        halign: 'right'
        size_hint: None, None #need to turn this off so custom sizing applies
        size: root.size[0] * 0.107, root.size[1] * 0.03
        pos: root.size[0] * 0.04, root.size[1] * 0.62

    CustomButton:
        # canvas.after:
        #     Color:
        #         rgba: 1, 0, 0, 0.5
        #     Rectangle:
        #         size: self.size
        #         pos: self.pos
        font: 'Antonio-VariableFont_wght.ttf'
        text: 'ACOSEE 12'
        text_size: self.size
        color: 0,0,0,1
        halign: 'right'
        size_hint: None, None #need to turn this off so custom sizing applies
        size: root.size[0] * 0.107, root.size[1] * 0.03
        pos: root.size[0] * 0.04, root.size[1] * 0.585
        
    CustomTimeButton:
        canvas.after:
            Color:
                rgba: 1, 0, 0, 0.5
            Rectangle:
                size: self.size
                pos: self.pos
        # canvas: 
        #     Color:
        #         # rgba: self.color
        #         rgba: 0,0,0,0
        font: 'Antonio-VariableFont_wght.ttf'
        font_size: dp(root.size[1] * 0.06)
        text: self.strtime
        text_size: self.size
        color: 50,153,255,1
        # color: 0,0,1,1
        # rgb(255, 153, 50)
        halign: 'right'
        valign: 'center'
        size_hint: None, None #need to turn this off so custom sizing applies
        size: root.size[0] * 0.2, root.size[1] * 0.1
        pos: root.size[0] * 0.38, root.size[1] * 0.85
    
    CustomButton:
        canvas.after:
            Color:
                rgba: 1, 0, 0, 0.5
            Rectangle:
                size: self.size
                pos: self.pos
        font: 'Antonio-VariableFont_wght.ttf'
        text: self.stardate()
        text_size: self.size
        color: 50,153,255,1
        halign: 'center'
        valign: 'center'
        size_hint: None, None #need to turn this off so custom sizing applies
        size: root.size[0] * 0.1, root.size[1] * 0.05
        pos: root.size[0] * 0.61, root.size[1] * 0.85

CustomLayout:        
'''

class CustomLayout(Scatter):
    def on_scroll(self, touch, *args):
        # Zoom in or out based on the scroll direction
        if touch.button == 'scrolldown':
            self.scale -= 0.1
        elif touch.button == 'scrollup':
            self.scale += 0.1
        self.scale = max(0.1, min(self.scale, 10))  # Limit the zoom scale
    #reference:
    # https://stackoverflow.com/a/49905915
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.scale = self.scale *1.1
                print('down')
            elif touch.button == 'scrollup':
                self.scale = self.scale *0.9
                print('up')
        # App.get_running_app().root.
        # GridLayout.on_touch_down(self, touch)
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if touch.is_mouse_scrolling and touch.button == 'scrolldown':
            self.scale = self.scale *1.1
            print('down')
        if touch.is_mouse_scrolling and touch.button == 'scrollup':
            self.scale = self.scale *0.9
            print('up')
        return False
    def on_touch_move(self, *args):
        super().on_touch_move(*args)
        return False
    def on_touch_up(self, *args):
        super().on_touch_up(*args)
        return False

    def on_press(self):
        #MAKE SURE THE PRESS IS IN THE STENCIL WIDGET BEFORE ACCEPTING, OTHERWISE IGNORE
        # https://stackoverflow.com/questions/65600949/kivy-widgets-underneath-other-widgets-are-interactable-how-to-prevent-this
        '''A True return means "do not continue dispatching" and a False return means "continue dispatching"'''
        return False
class CustomButton(Button):
    opacity = NumericProperty(1)
    background_color = 0, 0, 0, 0
    stardateObj = StarDate()
    def __init__(self, *args, **kwargs):
        super().__init__()
        # self.opacity = 0
        print("CustomButtons are all opacity", self.opacity)
        #all bold text
        self.bold = True
    def on_release(self, *args, **kwargs):
        super().on_release()
        print(f'{self.text} is pressed!, {self.text_size}')

    def stardate(self, *args, **kwargs):
        # return str(StarDate.getStardate())
        try:
            print("needs self", self.stardateObj.getStardate())
            print("needs self", type(self.stardateObj.getStardate()))
            # print("what is this", type(StarDate.getStardate()), StarDate.getStardate())
            return str(self.stardateObj.getStardate())
        except Exception as e:
            import traceback
            print("full exception", "".join(traceback.format_exception(*sys.exc_info())))

class CustomTimeButton(CustomButton):
    #all this does is set a StringProperty which is the current time, I don't want ALL the widgets to get the time update
    strtime = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__()
        #start a timer to update every second
        Clock.schedule_once(self.get_time, 0)
        Clock.schedule_interval(self.get_time, 1)
    def get_time(self, *args, **kwargs):
        # self.strtime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        # self.strtime = datetime.datetime.now().strftime("%H:%M:%S")
        self.strtime = datetime.now().strftime("%H:%M:%S")

    def on_release(self, *args, **kwargs):
        super().on_release()


class LCARS(App):
    def build(self):
        self.title = 'LCARS GUI PROTOTYPE'
        return Builder.load_string(kvstring)

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.always_on_top = True
    app = LCARS()
    # trio.run(app.async_run, "trio")
    LCARS().run()