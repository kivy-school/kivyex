# https://discord.com/channels/423249981340778496/423250272316293120/1274799111840862341

from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger, LOG_LEVELS
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

Logger.setLevel(LOG_LEVELS["debug"])


def DEBUG(*a):
    Logger.debug(*a)


class LoggingWidget:
    def add_widget(self, widget, *a, **kw):
        Logger.debug(f"class {self.__class__.__name__}: adding widget: {widget.__class__.__name__}")
        super().add_widget(widget, *a, **kw)


Builder.load_string('''

<MenuTitleBar>:
    id: titlebar
    title_label: title_label
    orientation: 'horizontal'
    Button:
        text: "X"
        size_hint_x: .1
        on_release: titlebar.open_menu(self)
    Label:
        id: title_label
        # text: titlebar.title
        text: "titlebar.title"
        halign: "left"

<Main>:
    orientation: 'vertical'
    MenuTitleBar:
        id: topbar
        size_hint_y: .1
        title: "menutitlebar title"

    TabbedPanel:
        id: tabpanel
        tab_pos: 'top_left'
        do_default_tab: False
        TabbedPanelItem:
            text: "Channels"
            MyRecycleView:
                id: channel_tab

        TabbedPanelItem:
            text: "Feeds"
            MyRecycleView:
                id: feed_tab

        TabbedPanelItem:
            text: "Episodes"
            MyRecycleView:
                id: episode_tab

    # bottom menu
    BoxLayout:
        id: buttonbar
        orientation: 'horizontal'
        size_hint_y: .05
        Button:
            text: "Add" or "➕" or "＋"
            on_release: 
                # print("added")
                root.add_one()
        Button:
            text: "Edit" or "✎"
        Button:
            text: "Del" or "➖" or "－"
        Button:
            text: "Reload"

<SelectableItem>:
    id: item
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        halign: 'left'
        text: ' | '.join(filter(None, (item.icon, item.name, item.description)))

<MyRecycleView>:
    viewclass: 'SelectableItem'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False

''')


class MenuTitleBar(LoggingWidget, BoxLayout):
    # def __init__(self, *args, **kwargs):
    #     self.title = "custom title"
    #     self._disabled_count = 20
    pass


class SelectableItem(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    icon = StringProperty()
    name = StringProperty()
    description = StringProperty()
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, *a, **kw):
        self.app = App.get_running_app()
        super().__init__(*a, **kw)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            DEBUG(f'SelectableItem passing touch to {self.parent!r}')
            return self.parent.select_with_touch(self.index, touch)
        return False

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

        # rv.selected = rv.data[index]['_model'] if is_selected else None
        model = None
        if is_selected:
            data = rv.data[index]
            # model = data['_model']
            print("rv?", dir(rv))
            # DEBUG(f"{rv.tab_name} tab selection changed to model for {data['name']!r} : {data['description']}")
        else:
            # DEBUG(f"{rv.tab_name} tab selection changed to None")
            pass

        rv.selected = model


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        item = None
        if is_selected:
            Logger.debug("apply_selection: selection changed to {0}".format(rv.data[index]))
            item = rv.data[index]
        else:
            Logger.debug("apply_selection: selection removed for {0}".format(rv.data[index]))
        rv.selected = item


class MyRecycleView(LoggingWidget, RecycleView):
    #selected = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n = 0

    def add_one(self):
        self.n += 1
        self.data.append({'text': str(self.n)})
        Logger.debug(f"add_one: Data is now {self.data!r}")

    def add_widget(self, widget, *a, **kw):
        Logger.debug(f"adding widget: {widget.__class__.__name__}")
        super().add_widget(widget, *a, **kw)


class MyTabbedPanel(LoggingWidget, TabbedPanel):
    pass


class MyTabbedPanelItem(LoggingWidget, TabbedPanelItem):
    pass


# class Main(LoggingWidget, BoxLayout):
class Main( BoxLayout):
    def add_one(self):
        print("self iods", self.ids["channel_tab"])
        self.ids["channel_tab"].add_one()


class MyApp(App):
    def build(self):
        self.main = Main()
        return self.main


if __name__ == '__main__':
    try:
        from kivy.core.window import Window
        Window.always_on_top = True
        MyApp().run()
    except Exception as e:
        import traceback, sys 
        print("full exception", "".join(traceback.format_exception(*sys.exc_info())))
