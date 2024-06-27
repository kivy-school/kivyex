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

#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

Builder.load_string('''

<CustomDD@DropDown>:
    Button: 
        id: ddID1
        text: "Add to queue"
        on_release: print(self.text)
    Button: 
        id: ddID2
        text: "Save to Watch Later"
        on_release: print(self.text)
    Button: 
        id: ddID3
        text: "Save to Playlist"
        on_release: print(self.text)
    Button: 
        id: ddID4
        text: "Download"
        on_release: print(self.text)
    Button: 
        id: ddID5
        text: "Share"
        on_release: print(self.text)
    Button: 
        id: ddID6
        text: "Not interested"
        on_release: print(self.text)
    Button: 
        id: ddID7
        text: "Don't recommend channel"
        on_release: print(self.text)
    Button: 
        id: ddID8
        text: "Report"
        on_release: print(self.text)
                    
<SelectableBoxLayout>:
    orientation: 'horizontal'
                    
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
            
    AsyncImage: 
        id: thumbID
        # size_x: dp(50)
        # size_hint: (1,0.6)
    
    BoxLayout:
        id: "textBoxID"
        orientation: 'vertical'
        size_hint: (1.3,1)

        Label:
            id: videoTitleID
            text: "default name"
            font_name: 'Roboto'
            size_hint: (1,1)
            # https://stackoverflow.com/questions/52222205/python-how-to-make-label-bold-in-kivy
            bold: True

            
            text_size: self.size
            halign: 'left'
            
        Label:
            id: videoAuthorID
            font_name: 'Roboto'
            text: "default number"
            
            text_size: self.size
            halign: 'left'
        
        Label:
            id: videoViewsID
            text: "default number"
            font_name: 'Roboto'
                    
            text_size: self.size
            halign: 'left'
                    
        Label:
            # text: 'blah blah ' * 1000
            text: 'blah blah ' * 1000
            text_size: self.width, None
            size_hint: 1, None
            height: self.texture_size[1]
            max_lines: 2
            # shorten: True
            # shorten_from: right
            # split_str: " "
                        
    BoxLayout:
        id: buttonBoxID
        orientation: 'vertical'
        # size_hint: (0.1,1)
        
        Button: 
            id: ddbuttonID
            text: "..."
            # on_release: ddID.open(self)

        # CustomDD:
        # DropDown:
        #     id: ddID
        #     # on_release: self.open
        #     Button: 
        #         id: ddID1
        #         text: "Add to queue"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID2
        #         text: "Save to Watch Later"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID3
        #         text: "Save to Playlist"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID4
        #         text: "Download"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID5
        #         text: "Share"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID6
        #         text: "Not interested"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID7
        #         text: "Don't recommend channel"
        #         on_release: print(self.text)
        #     Button: 
        #         id: ddID8
        #         text: "Report"
        #         on_release: print(self.text)
    # Button:
    #     id: testButtonID

<RV>:
    viewclass: 'SelectableBoxLayout'
    id: RV_ID
    data: self.rvdata
    SelectableRecycleBoxLayout:
        default_size: None, dp(90)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
''')
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
class SelectableBoxLayout(RecycleKVIDsDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)        
        # self.parent.parent.refresh_from_data()
        # import pdb
        # pdb.set_trace()
        
    def on_touch_up(self, touch): #touch is laggy because touch up takes a while
        # self.parent.parent.refresh_from_data()
        pass
        
    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.rvdata[index]))
        else:
            print("selection removed for {0}".format(rv.rvdata[index]))
        
class RV(RecycleView):
    rvdata = ListProperty() 
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.rvdata = [{"videoTitleID.text": "id: "+ str(x*2) + " VERY LONG COOL YOUTUBE TITLE!", 'videoAuthorID.text': 'Employee:' + '\N{pensive face}'} for x in range(10)]
        # self.rvdata = [{"testButtonID.text": "id: "+ str(x*2) + " VERY LONG COOL YOUTUBE TITLE!"} for x in range(10)]
        
class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    from kivy.core.window import Window
    #this is to make the Kivy window always on top
    Window.always_on_top = True
    #https://stackoverflow.com/questions/14014955/kivy-how-to-change-window-size
    Window.size = (dp(400), 700)
    TestApp().run()