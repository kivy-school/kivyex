from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.uix.image import AsyncImage
from kivy.core.window import Window

class ZoomScatter(Scatter):
    def on_scroll(self, touch, *args):
        # Zoom in or out based on the scroll direction
        if touch.button == 'scrolldown':
            self.scale -= 0.1
        elif touch.button == 'scrollup':
            self.scale += 0.1
        self.scale = max(0.1, min(self.scale, 10))  # Limit the zoom scale
    #reference:
    # https://stackoverflow.com/a/49905915
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.scale = self.scale *1.1
                print('down')
            elif touch.button == 'scrollup':
                self.scale = self.scale *0.9
                print('up')
        # App.get_running_app().root.
        # GridLayout.on_touch_down(self, touch)

class ZoomApp(App):
    def build(self):
        return Builder.load_string(
            """
<ZoomScatter>:
    id: ZS_ID
    do_translation: False
    do_rotation: False
    size_hint: None, None
    # pos: float(root.size[0])*0.5,  float(root.size[1])*0.5
    pos: root.parent.size[0]*0.5,  root.parent.size[1]*0.5
    AsyncImage:
        source: 'https://images.unsplash.com/photo-1630629701731-56481a2dd34a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1502&q=80'

Screen:
    ZoomScatter:
"""
        )
    

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.always_on_top = True
    ZoomApp().run()


# try:
#     ZoomApp().run()
# except Exception as e:
#     import traceback
#     print("full exception", "".join(traceback.format_exception(*sys.exc_info())))
#     # https://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid
#     import psutil
#     import os
#     p = psutil.Process(os.getpid())
#     p.terminate()