from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

kv = """
<IconLabel@Label>:
    font_name: "materialdesignicons-webfont.ttf"
    font_size: "48sp"
    # color: 1, 1, 1, 1

<RootWidget>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    IconLabel:
        text: u"\U000F05C7 "  # mdi-home
    IconLabel:
        text: u"\\F0A95"  # mdi-account
    IconLabel:
        text: u"\\F04FE"  # mdi-email
    Label:
        text: "yo yo yo"
    Label:
        text: u'\u00A9 ' + chr(97)
"""

class RootWidget(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        Builder.load_string(kv)
        return RootWidget()

if __name__ == '__main__':
    MyApp().run()
