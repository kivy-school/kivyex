# https://www.reddit.com/r/kivy/comments/1ddbwua/paint_in_an_image/
'''
Touch Tracer Line Drawing Demonstration
=======================================

This demonstrates tracking each touch registered to a device. You should
see a basic background image. When you press and hold the mouse, you
should see cross-hairs with the coordinates written next to them. As
you drag, it leaves a trail. Additional information, like pressure,
will be shown if they are in your device's touch.profile.

.. note::

   A function `calculate_points` handling the points which will be drawn
   has by default implemented a delay of 5 steps. To get more precise visual
   results lower the value of the optional keyword argument `steps`.

This program specifies an icon, the file icon.png, in its App subclass.
It also uses the particle.png file as the source for drawing the trails which
are white on transparent. The file touchtracer.kv describes the application.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/touchtracer on your Android device.

'''
__version__ = '1.0'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException
from kivy.metrics import dp
from random import random
from math import sqrt
from kivy.lang import Builder
from kivy.modules import inspector
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import StringProperty

kv_string = '''
#:kivy 1.0
#:import kivy kivy

<Touchtracer>:
    canvas:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            size: self.size

    AsyncImage:
        id: asyncimageID

    BoxLayout:
        padding: '10dp'
        spacing: '10dp'
        size_hint: 1, None
        pos_hint: {'top': 1}
        height: '44dp'
        Image:
            size_hint: None, None
            size: '24dp', '24dp'
            source: 'data/logo/kivy-icon-64.png'
            mipmap: True
        Label:
            height: '24dp'
            text_size: self.width, None
            color: (1, 1, 1, .8)
            text: 'Kivy %s - Touchtracer' % kivy.__version__
            valign: 'middle'

<MainBox@BoxLayout>:
    orientation: 'vertical'
    BoxLayout: 
        orientation: 'horizontal'
        Button:
            text: "load image using filechooser"
            on_release: 
                # import pdb
                # pdb.set_trace()
                root.parent.parent.current = 'chooser_screen_name'
        Button:
            text: "save png!"
            on_release: 
                # import pdb
                # pdb.set_trace()
                root.savepng()
    Touchtracer:
        id: touchtracerID

<CustomChooser@FileChooserListView>:
        
<ImagePainterManager>:
    id: image_painter_managerID
    StartScreen:
        id: start_screenID
        name: 'start_screen_name'
        manager: 'image_painter_managerID'
    ChooserScreen:
        id: chooser_screenID
        name: 'chooser_screen_name'

<StartScreen@Screen>:
    id: start_screenID
    MainBox:
        id: mainboxID

<ChooserScreen@Screen>:
    id: chooser_screenID
    BoxLayout:
        CustomChooser:
            id: filechooserID
        Button:
            text: "Cancel"
            on_release: 
                # import pdb
                # pdb.set_trace()
                root.parent.current = 'start_screen_name'
        Button:
            text: root.loadtext
            on_release: 
                # import pdb
                # pdb.set_trace()
                root.ids['filechooserID'].chooser_load()
        
ImagePainterManager:
'''

class ImagePainterManager(ScreenManager):
    pass

'''
#using @ kv syntax means you don't have to declare screen, see: https://kivy.org/doc/stable/guide/lang.html#dynamic-classes
class StartScreen(Screen):
    pass

'''

class MainBox(BoxLayout): #need to declare MainBox even with @ syntax in kv "<MainBox@BoxLayout>:" because we are adding a new method
    
    def savepng(self):
        #goal: get correct widget (in this case Touchtracer widget)
        #see: https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.export_to_png
        # import pdb
        # pdb.set_trace()
        self.parent.ids['mainboxID'].ids['touchtracerID'].export_to_png("PRINTEDIMAGE.png")

class ChooserScreen(Screen):
    loadtext = StringProperty("Load")

class CustomChooser(FileChooserListView): #need to declare FileChooserListView even with @ syntax in kv "<CustomChooser@FileChooserListView>:" because we are adding a new method

    def chooser_load(self):
        #make sure selection is nonempty AND has .jpg extension
        #checked: 
            #no selection
            #actual jpg
            #not a jpg
            #folder (not possible to choose apparently)
        if self.selection != [] and str(self.selection[0]).split(".")[-1] == "jpg": 
            print("is jpg!")
            import pdb
            pdb.set_trace()
            #hint: App.get_running_app().root
            #set the source of the image
            import os
            #TypeError: join() argument must be str, bytes, or os.PathLike object, not 'ObservableList'
            # safepath = os.path.join(self.path, self.selection) 
            safepath = os.path.join(self.path, self.selection[0]) #use os.path.join instead of string slicing, do not rewrite the wheel!

            App.get_running_app().root.ids['start_screenID'].ids['mainboxID'].ids['touchtracerID'].ids['asyncimageID'].source = safepath
            self.parent.parent.parent.current = 'start_screen_name'
            
        else: 
            self.parent.parent.loadtext = "Please choose a jpg file."
    


def calculate_points(x1, y1, x2, y2, steps=5):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return
    o = []
    m = dist / steps
    for i in range(1, int(m)):
        mi = i / m
        lastx = x1 + dx * mi
        lasty = y1 + dy * mi
        o.extend([lastx, lasty])
    return o


class Touchtracer(FloatLayout):

    def normalize_pressure(self, pressure):
        print(pressure)
        # this might mean we are on a device whose pressure value is
        # incorrectly reported by SDL2, like recent iOS devices.
        if pressure == 0.0:
            return 1
        return dp(pressure * 10)

    def on_touch_down(self, touch):
        # import pdb
        # pdb.set_trace()
        #problem is this also intercepts the button inputs, so only do something when the touch point collides with touchtracer class (which in this case is self)
        if self.collide_point(*touch.pos):
            win = self.get_parent_window()
            ud = touch.ud
            ud['group'] = g = str(touch.uid)
            pointsize = 5
            print(touch.profile)
            if 'pressure' in touch.profile:
                ud['pressure'] = touch.pressure
                pointsize = self.normalize_pressure(touch.pressure)
            ud['color'] = random()

            with self.canvas:
                Color(ud['color'], 1, 1, mode='hsv', group=g)
                ud['lines'] = [
                    Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                    Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                    Point(points=(touch.x, touch.y), source='particle.png',
                        pointsize=pointsize, group=g)]

            ud['label'] = Label(size_hint=(None, None))
            self.update_touch_label(ud['label'], touch)
            self.add_widget(ud['label'])
            touch.grab(self)
            return True

    def on_touch_move(self, touch):
        #problem is this also intercepts the button inputs, so only do something when the touch point collides with self (which in this case is the touchtracer class)
        if self.collide_point(*touch.pos):
            if touch.grab_current is not self:
                return
            ud = touch.ud
            ud['lines'][0].pos = touch.x, 0
            ud['lines'][1].pos = 0, touch.y

            index = -1

            while True:
                try:
                    points = ud['lines'][index].points
                    oldx, oldy = points[-2], points[-1]
                    break
                except IndexError:
                    index -= 1

            points = calculate_points(oldx, oldy, touch.x, touch.y)

            # if pressure changed create a new point instruction
            if 'pressure' in ud:
                old_pressure = ud['pressure']
                if (
                    not old_pressure
                    or not .99 < (touch.pressure / old_pressure) < 1.01
                ):
                    g = ud['group']
                    pointsize = self.normalize_pressure(touch.pressure)
                    with self.canvas:
                        Color(ud['color'], 1, 1, mode='hsv', group=g)
                        ud['lines'].append(
                            Point(points=(), source='particle.png',
                                pointsize=pointsize, group=g))

            if points:
                try:
                    lp = ud['lines'][-1].add_point
                    for idx in range(0, len(points), 2):
                        lp(points[idx], points[idx + 1])
                except GraphicException:
                    pass

            ud['label'].pos = touch.pos
            import time
            t = int(time.time())
            if t not in ud:
                ud[t] = 1
            else:
                ud[t] += 1
            self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        ud = touch.ud
        # self.canvas.remove_group(ud['group']) #this removes everything
        #remove lines only:

        for line in ud['lines'][:2]:
            self.canvas.remove(line)
        # import pdb
        # pdb.set_trace()
        self.remove_widget(ud['label'])
        '''
        pdb says:
        ud['lines'] is 3 objects:
        [
        <kivy.graphics.vertex_instructions.Rectangle object at 0x000002999A91E200>, 
        <kivy.graphics.vertex_instructions.Rectangle object at 0x000002999A91E2A0>, 
        <kivy.graphics.vertex_instructions.Point object at 0x000002999A91E340>
        ]
        point is what we wanna keep, so remove the other 2
        this is because the drawn shape is a sequence of points!
        '''

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id, touch.x, touch.y, touch.__class__.__name__)
        label.texture_update()
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


class TouchtracerApp(App):
    title = 'Image Painter Example'
    icon = 'icon.png'

    def build(self):
        inspector.create_inspector(Window, self)
        return Builder.load_string(kv_string)

    def on_pause(self):
        return True


if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    TouchtracerApp().run()
