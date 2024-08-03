from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
# from kivymd.uix.behaviors import DeclarativeBehavior, ScaleBehavior
from kivymd.uix.behaviors import DeclarativeBehavior
from kivy.uix.boxlayout import BoxLayout

from kivy.lang.builder import Builder
from kivy.event import EventDispatcher
from kivy.animation import Animation, AnimationTransition
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    StringProperty,
    NumericProperty,
    ListProperty,
    ObjectProperty
)
from kivy.graphics.context_instructions import PushMatrix, Scale, PopMatrix

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor 
        
    FDualIconButton:
        pos_hint: {'center_x': .5, 'center_y': .5}
        id: button
        FDualIconButtonChild:
            icon: 'menu'
            on_release:
                button.current = 'check'
                print("start selecting")
        FDualIconButtonChild:
            icon: 'check'
            theme_icon_color: 'Custom'
            icon_color: 'red'
            on_release:
                button.current = 'menu'
                print("finish selecting")

<FDualIconButtonChild>
    ripple_scale: 2
    ripple_duration_in_fast: .5


<FDualIconButton>
    size_hint: None, None
    size: dp(40), dp(40)
'''

class FDualIconButtonException(Exception):
    pass


class ButtonTransitionBase(EventDispatcher):
    '''TransitionBase is used to animate 2 FIconButton(s) within the
    :class:`FDualIconButton`. This class acts as a base for other
    implementations like the :class:`SlideTransition` and
    :class:`SwapTransition`.
    '''

    button_out = ObjectProperty()
    '''Property that contains the button to hide.
    Automatically set by the :class:`FDualIconButton`.

    :class:`button_out` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    button_in = ObjectProperty()
    '''Property that contains the button to show.
    Automatically set by the :class:`FDualIconButton`.

    :class:`button_in` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    duration = NumericProperty(.4)
    '''Duration in seconds of the transition.

    :class:`duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to .4 (= 400ms).
    '''

    container = ObjectProperty()
    ''':class:`FDualIconButton` object, set when the button is added to a
    container.

    :attr:`container` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None, read-only.

    '''

    is_active = BooleanProperty(False)
    '''Indicate whether the transition is currently active or not.

    :attr:`is_active` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False, read-only.
    '''

    # privates

    _anim = ObjectProperty(allownone=True)

    __events__ = ('on_progress', 'on_complete')

    def start(self, container):
        '''(internal) Starts the transition. This is automatically
        called by the :class:`FDualIconButton`.
        '''
        if self.is_active:
            raise FDualIconButtonException('start() is called twice!')
        self.container = container
        print("duration", self.duration)
        self.duration = 2
        self._anim = Animation(d=self.duration, s=0)
        # self.add_button(self.button_in)
        self._anim.bind(on_progress=self._on_progress,
                        on_complete=self._on_complete)
        print("self button in?", self.button_in)
        # self.button_in.opacity = 0  # Ensure the incoming button starts as invisible
        # self.button_out.opacity = 1  # Ensure the outgoing button is visible
        self.is_active = True
        self._anim.start(self)
        self.dispatch('on_progress', 0)

    def stop(self):
        '''(internal) Stops the transition. This is automatically called by the
        :class:`FDualIconButton`.
        '''
        if self._anim:
            self._anim.cancel(self)
            self.dispatch('on_complete')
            self._anim = None
        self.is_active = False

    def add_button(self, button):
        '''(internal) Used to add a screen to the :class:`FDualIconButton`.
        '''
        self.container.real_add_widget(button)

    def remove_button(self, button):
        '''(internal) Used to remove a screen from the :class:`FDualIconButton`.
        '''
        self.container.real_remove_widget(button)

    def on_complete(self):
        self.remove_button(self.button_out)

    def on_progress(self, progression):
        pass

    def _on_progress(self, *l):
        progress = l[-1]
        self.dispatch('on_progress', progress)

    def _on_complete(self, *l):
        self.is_active = False
        self.dispatch('on_complete')
        self._anim = None


from kivy.graphics.context_instructions import PushMatrix, Scale, PopMatrix

class ButtonPopupTransition(ButtonTransitionBase):

    def on_progress(self, progression):
        # pass
        a = self.button_in
        b = self.button_out
        al = AnimationTransition.out_quad
        progression = al(progression)

        if progression == 0:
            self.button_in.pos = self.container.pos
            self.button_out.pos = self.container.pos

        # print("wtfff", a, dir(a), b, dir(b))
        # print("================================")

        print("max?", max(1 - progression,0.6))

        # with b.canvas.before:
        #     PushMatrix()
        #     Scale(
        #         # x=1 - progression,
        #         # x=max(1 - progression,0.6),
        #         # x=0.9,
        #         # y=max(1 - progression,0.6),
        #         # x=progression,
        #         # y=progression,
        #         x=1-progression,
        #         y=1-progression,
        #         z=1,
        #         origin=b.center
        #     )
        # with b.canvas.after:
        #     PopMatrix()
            
        # with a.canvas.before:
        #     PushMatrix()
        #     Scale(
        #         # x=1-progression,
        #         # y=1-progression,
        #         x=1,
        #         y=1,
        #         # x=progression,
        #         # y=progression,
        #         z=1,
        #         origin=a.center
        #     )
        # with a.canvas.after:
        #     PopMatrix()

        print("??", progression, 1-progression)

        
        # Animation(
        #     scale_value_x=0.5,
        #     scale_value_y=0.5,
        #     scale_value_z=0.5,
        #     d=0.3,
        # ).start(a)

        # a.scale_value_x = a.scale_value_y = progression
        # b.scale_value_x = b.scale_value_y = 1 - progression

        if progression > .6:
            if a.opacity == 0:
                a.opacity = 1
            if b.opacity == 1:
                b.opacity = 0
        else:
            a.opacity = progression  # Smooth fade-in effect
            b.opacity = 1 - progression  # Smooth fade-out effect

    def on_complete(self):
        # self.real_add_widget(self.button_in)
        super().on_complete()


# class FDualIconButtonChild(ScaleBehavior, MDIconButton):
class FDualIconButtonChild(MDIconButton):
    # scale_value_x = NumericProperty(1)
    # scale_value_y = NumericProperty(1)
    # scale_value_z = NumericProperty(1)
    # scale_value_center = ListProperty()
    container = ObjectProperty(None, allownone=True)


class FDualIconButton(DeclarativeBehavior, BoxLayout):
    buttons = ListProperty()
    current = StringProperty(None, allownone=True)
    current_button = ObjectProperty(None)

    def _get_button_icons(self):
        return [b.icon for b in self.buttons]
    
    button_icons = AliasProperty(_get_button_icons, bind=('buttons',))

    def __init__(self, *args, **kwargs):
        if 'transition' not in kwargs:
            self.transition = ButtonPopupTransition()
        super().__init__(*args, **kwargs)
        self.fbind('pos', self._update_pos)

    def _button_icon_changed(self, button, icon):
        self.property('button_icons').dispatch(self)
        if button == self.current_button:
            self.current = icon
    
    def add_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, FDualIconButtonChild):
            raise FDualIconButtonException(
                "FDualIconButton accepts only FDualIconButtonChild widget."
            )

        if len(self.buttons) <= 2:
            widget.container = self
            widget.bind(icon=self._button_icon_changed)
            self.buttons.append(widget)
            if self.current is None:
                self.current = widget.icon
        else:
            raise FDualIconButtonException(
                "You can't add more than 2 icon buttons."
            )
        
            
    def remove_widget(self, widget, *args, **kwargs):
        if not isinstance(widget, FDualIconButtonChild):
            raise FDualIconButtonException(
                "FDualIconButton can only remove FIconButton."
            )
        
        if widget not in self.buttons:
            return
        
        if self.current_button == widget:
            other = next(self)
            if widget.icon == other:
                self.current = None
                widget.parent.real_remove_widget(widget)
            else:
                self.current = other

        widget.container = None
        widget.unbind(icon=self._button_icon_changed)
        self.buttons.remove(widget)

    def clear_widgets(self, children=None, *args, **kwargs):
        if children is None:
            # iterate over a copy of buttons, as self.remove_widget
            # modifies self.buttons in place
            children = self.buttons[:]
        remove_widget = self.remove_widget
        for widget in children:
            remove_widget(widget)

    def real_add_widget(self, button, *args):
        # ensure button is removed from its previous parent
        parent = button.parent
        if parent:
            parent.real_remove_widget(button)
        super().add_widget(button)

    def real_remove_widget(self, button, *args):
        super().remove_widget(button)   

    def on_current(self, instance, value):
        if value is None:
            self.transition.stop()
            self.current_button = None
            return

        button = self.get_button(value)
        if button == self.current_button:
            return

        self.transition.stop()

        previous_button = self.current_button
        self.current_button = button
        if previous_button:
            self.transition.button_in = button
            self.transition.button_out = previous_button
            self.transition.start(self)
        else:
            self.real_add_widget(button)

    def get_button(self, icon):
        '''Return the button widget associated with the name or raise a
        :class:`FDualIconButtonException` if not found.
        '''
        matches = [b for b in self.buttons if b.icon == icon]
        num_matches = len(matches)
        if num_matches == 0:
            raise FDualIconButtonException(f"No Button with icon '{icon}'.")
        return matches[0]
    
    def __next__(self):
        '''Py2K backwards compatibility without six or other lib.
        '''
        buttons = self.buttons
        if not buttons:
            return
        try:
            index = buttons.index(self.current_button)
            index = (index + 1) % len(buttons)
            return buttons[index].icon
        except ValueError:
            return

    def next(self):
        '''Return the name of the next button from the screen list.'''
        return self.__next__()

    def previous(self):
        '''Return the name of the previous button from the screen list.
        '''
        buttons = self.buttons
        if not buttons:
            return
        try:
            index = buttons.index(self.current_button)
            index = (index - 1) % len(buttons)
            return buttons[index].icon
        except ValueError:
            return
        
    def _update_pos(self, instance, value):
        for child in self.children:
            if self.transition.is_active and \
                (child == self.transition.button_in or
                 child == self.transition.button_out):
                continue
            child.pos = value

    def on_motion(self, etype, me):
        if self.transition.is_active:
            return False
        return super().on_motion(etype, me)

    def on_touch_down(self, touch):
        if self.transition.is_active:
            return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.transition.is_active:
            return False
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.transition.is_active:
            return False
        return super().on_touch_up(touch)
    

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)
    
from kivy.core.window import Window
Window.always_on_top = True
MyApp().run()