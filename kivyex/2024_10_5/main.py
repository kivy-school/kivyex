import trio
from kivy.lang import Builder

from kivy_reloader.app import App

from kivy.core.window import Window
Window.show_cursor = False
from kivy.clock import Clock
from kivy.graphics import Rectangle

from kivy.core.image import Image as CoreImage

import pathlib
from kivy.resources import resource_add_path, resource_find
resource_add_path(pathlib.Path(__file__).parent / "resources")

kv = """
#:import app kivy_reloader.app.App
#:import Window kivy.core.window.Window

#:import resource_find kivy.resources.resource_find

#:set app_obj app.get_running_app()

BoxLayout:
    Button:
        text: "Reveal Mouse"
        on_release:
            print("window state:", Window.show_cursor)
            # from Chatgpt, very big brain solution
            Window.show_cursor = not Window.show_cursor

    Button:
        text: "change image"
        on_release: 
            app_obj.change_cursor_image(app_obj.cycle_image())
            # app_obj.change_cursor_image(resource_find("cat2.jpg"))

"""

class MainApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.cursor_show, 0)
    
    def build(self):
        return Builder.load_string(kv)
    
    def cursor_show(self, *args):
        self.image = 'Clippy.png'
        with Window.canvas.after:
            self.cursor_rect = Rectangle(source= 'Clippy.png', size=(128, 128), pos=(Window.mouse_pos[0],Window.mouse_pos[1])) 
        Clock.schedule_interval(self.cursorPosition, 1/60)
    
    def cursorPosition(self, *args):
        # Get the mouse position and move the cursor image
        mouse_pos = Window.mouse_pos
        self.cursor_rect.pos = (
            (mouse_pos[0] - self.cursor_rect.size[0] / 2), 
            (mouse_pos[1] - self.cursor_rect.size[1] / 2)) 

    def change_cursor_image(self, new_image_path):
        # Load a new image texture
        new_texture = CoreImage(new_image_path).texture
        # Apply the new texture to the existing rectangle
        if self.cursor_rect:
            self.cursor_rect.texture = new_texture

    def cycle_image(self):
        #there is a smarter way to do this but for the sake of time will do it the quick way
        if self.image == 'Clippy.png':
            self.image = 'cat1.jpg'
        elif self.image == 'cat1.jpg':
            self.image = 'cat2.jpg'
        elif self.image == 'cat2.jpg':
            self.image = 'Clippy.png'
        return resource_find(self.image)

app = MainApp()
trio.run(app.async_run, "trio")