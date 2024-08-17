from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import ColorProperty

kv = """
<LCARSButton>:
    size_hint: None, None
    size: dp(300), dp(48)
    color: 'black'
    canvas.before:
        Color:
            rgb: self.background_color if self.state == 'normal' else self.active_color
        Rectangle:
            size: self.size
            pos: self.pos

AnchorLayout:
    LCARSButton:
        text: 'test button'
        on_release: print(f'button pressed, state: {self.state}')
"""

class LCARSButton(ToggleButtonBehavior, Label):
    background_color = ColorProperty('orange')
    active_color = ColorProperty('darkred')

class DrawButtonApp(App):
    def build(self):
        return Builder.load_string(kv)


DrawButtonApp().run()