from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

kv = """
<CustomBoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    height: 44
    Label:
        text: root.text
    DropdownButton:
        id: dropdown_button
        text: 'Open Dropdown'

<RV>:
    viewclass: 'CustomBoxLayout'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<RootWidget>:
    orientation: 'vertical'
    RV:
"""

class DropdownButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = DropDown()
        for i in range(3):
            btn = Button(text=f'Option {i+1}', size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.dropdown.add_widget(btn)

    def on_release(self):
        self.dropdown.open(self)

    def select(self, text):
        self.text = text
        self.dropdown.dismiss()

class CustomBoxLayout(RecycleDataViewBehavior, BoxLayout):
    text = ''

    def refresh_view_attrs(self, rv, index, data):
        self.ids.dropdown_button.text = data['text']
        return super().refresh_view_attrs(rv, index, data)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': f'Item {i}'} for i in range(20)]

class TestApp(App):
    def build(self):
        Builder.load_string(kv)
        return RootWidget()

class RootWidget(BoxLayout):
    pass

if __name__ == '__main__':
    TestApp().run()
