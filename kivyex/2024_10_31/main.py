import trio
from kivy.lang import Builder

from kivy_reloader.app import App
from kivy.uix.button import Button

kv = """
BoxLayout:
    orientation: 'vertical'
    Button:
        text: "standard button"
    CustomButton:
        text: "custom button"
    ClearedButton:
        text: "cleared button"

# <CustomButton>:
#     background_color: [0,0,0,0]
#     background_normal: ""
#     background_down: ""
#     background_disabled_normal: ""
#     background_disabled_down: ""
#     border: [0,0,0,0]

# https://kivy.org/doc/stable/api-kivy.lang.html#redefining-a-widget-s-style
<-ClearedButton@Button>:
"""

class CustomButton(Button):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_string(kv)


app = MainApp()
trio.run(app.async_run, "trio")