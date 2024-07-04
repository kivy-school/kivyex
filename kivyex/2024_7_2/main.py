'''
Kivy Screenmanager example
'''
from kivy.app import App
from kivy.lang import Builder

#5 screens:
#home page
#settings page
#user profile
#media page
#trending page

kv_string = '''
#:import os os

<ScreenManagerExample@ScreenManager>:
    id: ScreenManagerID
    # By default, the first screen added into the ScreenManager will be
    # displayed. You can then change to another screen.
    # https://kivy.org/doc/stable/api-kivy.uix.screenmanager.html
    StartScreen:
        manager: 'ScreenManagerID'
        id: StartScreenID 
        name: 'startscreen'
    SettingsScreen:
        manager: 'ScreenManagerID'
        id: SettingsScreenID 
        name: 'settingsscreen'
    UserScreen:
        manager: 'ScreenManagerID'
        id: UserScreenID 
        name: 'userscreen'
    MediaScreen:
        manager: 'ScreenManagerID'
        id: MediaScreenID 
        name: 'mediascreen'
    TrendingScreen:
        manager: 'ScreenManagerID'
        id: TrendingScreenID 
        name: 'trendingscreen'

<StartScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        id: 'mainboxlayout'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: (1, 0.1)
            id: 'topboxlayout'
            Button: 
                text: "\U000F107D"
                # text: "transition to settings screen"
                font_name: os.path.join(os.path.split(os.getcwd())[0], "0_resources", 'materialdesignicons-webfont.ttf')
                font_size: dp(40)
                on_release: 
                    # import pdb
                    # pdb.set_trace()
                    #app.get_running_app().root.current
                    root.parent.current = 'settingsscreen'
            Button: 
                text: "\U000F0630"
                # text: "transition to user screen"
                font_name: os.path.join(os.path.split(os.getcwd())[0], "0_resources", 'materialdesignicons-webfont.ttf')
                font_size: dp(40)
                on_release: root.parent.current = 'userscreen'
            Button: 
                text: "\U000F1B97"
                # text: "transition to media screen"
                font_name: os.path.join(os.path.split(os.getcwd())[0], "0_resources", 'materialdesignicons-webfont.ttf')
                font_size: dp(40)
                on_release: root.parent.current = 'mediascreen'
            Button: 
                text: "\U000F0238"
                # text: "transition to trending screen"
                font_name: os.path.join(os.path.split(os.getcwd())[0], "0_resources", 'materialdesignicons-webfont.ttf')
                font_size: dp(40)
                on_release: root.parent.current = 'trendingscreen'

        Button: 
            text: "Start Screen!"
            on_release: 
                import pdb
                pdb.set_trace()
                app.get_running_app().root.ids["MediaScreenID"].ids["'mediabuttonID'"].text = "changed text from main screen"
                self.text = "changed text in media screen"

<SettingsScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        Button: 
            text: "Back to start"
            size_hint: (1, 0.1)
            on_release: root.parent.current = 'startscreen'
        Button: 
            text: "Settings screen!"
            on_release:
                self.text = app.get_running_app().root.current 

<UserScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        Button: 
            text: "Back to start"
            size_hint: (1, 0.1)
            on_release: root.parent.current = 'startscreen'
        Button: 
            text: "User screen!"

<MediaScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        Button: 
            id: 'startbuttonID'
            text: "Back to start"
            size_hint: (1, 0.1)
            on_release: root.parent.current = 'startscreen'
        Button: 
            id: 'mediabuttonID'
            text: "Media screen!"

<TrendingScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        Button: 
            text: "Back to start"
            size_hint: (1, 0.1)
            on_release: root.parent.current = 'startscreen'
        Button: 
            text: "Trending screen!"
            
ScreenManagerExample:
'''

class smApp(App):
    title = "screen manager example"
    def build(self):
        return Builder.load_string(kv_string)

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    smApp().run()
