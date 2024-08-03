
#kivymdscalebehavior test
# https://kivymd.readthedocs.io/en/1.1.1/behaviors/scale/index.html

from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior

from kivymd.app import MDApp
from kivymd.uix.behaviors import ScaleBehavior
from kivymd.uix.boxlayout import MDBoxLayout

KV = '''
MDScreen:

    ScaleBox:
        size_hint: .5, .5
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: app.change_scale1(self)
        on_release: app.change_scale2(self)
        md_bg_color: "red"
'''


class ScaleBox(ButtonBehavior, ScaleBehavior, MDBoxLayout):
    pass


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def change_scale1(self, instance_button: ScaleBox) -> None:
        Animation(
            scale_value_x=0.5,
            scale_value_y=0.5,
            scale_value_z=0.5,
            d=0.3,
        ).start(instance_button)
    def change_scale2(self, instance_button: ScaleBox) -> None:
        Animation(
            scale_value_x=1,
            scale_value_y=1,
            scale_value_z=1,
            d=0.3,
        ).start(instance_button)

from kivy.core.window import Window

Window.always_on_top = True
Test().run()