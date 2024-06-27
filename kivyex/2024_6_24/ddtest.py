from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior, RecycleKVIDsDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from  kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

Builder.load_string('''
<CustomDropDown>:
    Button:
        text: 'My first Item'
        size_hint_y: None
        height: 44
        on_release: root.select('item1')
    Label:
        text: 'Unselectable item'
        size_hint_y: None
        height: 44
    Button:
        text: 'My second Item'
        size_hint_y: None
        height: 44
        on_release: root.select('item2')
''')
class CustomDropDown(DropDown):
    pass

dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

class TestApp(App):
    def build(self):
        return mainbutton

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    #https://stackoverflow.com/questions/14014955/kivy-how-to-change-window-size
    # Window.size = (dp(400), 700)
    TestApp().run()