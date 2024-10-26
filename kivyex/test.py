'''
Kivy Screenmanager example
'''
import trio
from kivy_reloader.app import App
from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior

#5 screens:
#home page
#settings page
#user profile
#media page
#trending page

#:import operating_system os
kv_string = '''
BoxLayout:
    ButtonText2:
        sel_color: 1, 0, 0, 1
        text: "wkejrhewhr"
        canvas.before:
            Color:
                rgba: self.sel_color  # Red background color
            Rectangle:
                pos: self.pos
                size: self.size
    Button:
    Button:
    Button:
'''


'''
<-ButtonText>:
    color: root.color if self.state == 'normal' else root.color_down

    canvas.before:
        Color:
            rgba: (1,0,0,1)
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)

ButtonText:
    text: 'CHANGE'
    size_hint: None, None  
    size: 100,100
    # color: (0,1,0,1)
    # color_down: (0,0,1,1)
    font_size: dp(15)
    pos_hint: {'center_y': .5}
'''


'''
#:set fast_animal "cheetah"

<FancyButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0,0,0,0
    pos: 50,50
    size_hint: None, None
    size: 150,150
    bg_color: 0,0,1,0.99
    canvas.before: 
        Color:
            rgba: self.bg_color
        Rectangle:
            pos: self.pos
            size: self.size
FloatLayout:
    FancyButton:
        text: "Kivy School1"
        pos: 50,50
        bg_color: 0,0,1,0.99
    FancyButton:
        text: "Kivy School1"
        pos: 250,0
        bg_color: 0,1,0,0.99
    FancyButton:
        text: "Kivy School1"
        pos: 450,250
        bg_color: 1,0,0,0.99
    Image:
        size_hint: None, None
        size: 100, 100 
        source: "icon.png" 

    Button:
        background_normal: '' 
        background_color: rgba("#304FFE")
        pos: 250,450
        size_hint: None, None
        size: 100,100
        on_release: print("right one")

        canvas:
            Color: 
                rgba: rgba("#304FFE")
            RoundedRectangle:
                # radius: [dp(28), dp(4), dp(8), dp(12)]
                # radius: [dp(28)]
                radius: [(dp(10), dp(20)), (dp(30), dp(40)), (dp(30), dp(40)), (dp(30), dp(40))]

    Button:
        text: "text example"
        pos: 250,250
        size_hint: None, None
        size: 100,100
        on_press: print(fast_animal)
        on_release: print(f"position is: {self.pos}")
        canvas:
            Color: 
                rgba: rgba("#304FFE")
            Rectangle:
                size: ( self.width/2, self.height/2)
                pos: ( self.width/4 + self.pos[0], self.height/4 + self.pos[1])
            Line:
                points: 100, 190, 200, 0
'''


'''
BoxLayout:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle: 
            pos: 200,200
            size: self.size
'''

class ButtonText2(ButtonBehavior, Label):
    def on_touch_down(self, *args): 
        touch = args[0]
        print("data", self.collide_point(*touch.pos))
        if self.collide_point(*touch.pos) and self.state == 'normal':
            self.sel_color = 0, 1, 0, 1 # Change color when pressed
            self.state = 'down'
            return True # Capture the touch event
    def on_touch_up(self, *args): 
        touch = args[0]
        print("data up", self.collide_point(*touch.pos), self.state)
        if self.state == 'down':
            self.sel_color = 1, 0, 0, 1  # Reset to original color
            self.state = 'normal'

class ButtonText(ButtonBehavior, Label):
    color_down: list | tuple = ColorProperty()

class smApp(App):
    title = "screen manager example"
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    # smApp().run()
    app = smApp()
    trio.run(app.async_run, "trio")
