# https://www.reddit.com/r/kivy/wiki/snippets/#wiki_hover_cursor
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory as F
from kivy.core.window import Window

class HoverManager(object):
    default_cursor = "arrow"

    def __init__(self):
        Window.bind(mouse_pos=self._on_hover_mouse_pos)
        Window.bind(on_cursor_leave=self._on_hover_cursor_leave)

    def _on_hover_mouse_pos(self, win, mouse_pos):
        cursor = None
        for toplevel in Window.children:
            for widget in toplevel.walk_reverse(loopback=True):
                if isinstance(widget, HoverCursorBehavior):
                    collided = widget._on_hover_mouse_pos(win, mouse_pos)
                    if collided and not cursor:
                        cursor = widget.hover_cursor
                        # Don't break here, because we need to process
                        # all instances to update hover_active
        new_cursor = cursor if cursor else self.default_cursor
        Window.set_system_cursor(new_cursor)

    def _on_hover_cursor_leave(self, win):
        for toplevel in Window.children:
            for widget in toplevel.walk_reverse(loopback=True):
                if isinstance(widget, HoverCursorBehavior):
                    widget.hover_active = False
        Window.set_system_cursor(self.default_cursor)


class HoverCursorBehavior(object):
    hover_active = F.BooleanProperty(False)
    hover_cursor = F.StringProperty("crosshair")

    def _on_hover_mouse_pos(self, win, mouse_pos):
        self.hover_active = mouse_collided = self.collide_point(*mouse_pos)
        return mouse_collided

class HoverLabel(HoverCursorBehavior, F.Label):
    pass

KV = '''
#:import F kivy.factory.Factory

<TestPopup@Popup>:
    size_hint: .5, .5
    BoxLayout:
        HoverLabel:
            hover_cursor: "wait"

<HoverLabel>:
    canvas:
        Color:
            rgba: 1, int(self.hover_active), 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size

FloatLayout:
    BoxLayout:
        HoverLabel:
            hover_cursor: "hand"
        HoverLabel:
            hover_cursor: "size_all"
        HoverLabel:
        HoverLabel:
        HoverLabel:
        HoverLabel:
        Button:
            on_press: F.TestPopup().open()
    HoverLabel:
        hover_cursor: "no"
        size_hint: 1, 0.25
        pos_hint: {'y': .5}
'''

class HoverApp(App):
    def build(self):
        self.hover_manager = HoverManager()
        return Builder.load_string(KV)

HoverApp().run()