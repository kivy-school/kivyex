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
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label

#emoji rendering
# https://www.reddit.com/r/kivy/comments/12l0x8n/any_fix_for_emoji_rendering/

Builder.load_string('''

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
        size_hint: (0.1,1)
        
        # Spinner: 
        #     values: 'Home', 'Work', 'Other', 'Custom'

        DropdownButton: 
            id: ddbuttonID
            text: "..."
            on_parent: self.individual_dropdown.dismiss()
            on_release: 
                self.open_dd(self)
                # self.individual_dropdown.open(self)
                # import pdb
                # pdb.set_trace()
            # https://stackoverflow.com/questions/54606119/why-kivy-dropdown-does-not-show
            # TL:DR; buttons heights need to be set
        
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
    
class DropdownButton(Button):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.individual_dropdown = DropDown()
        textlist = [
            # "Check Add to queue",
            # "Save to Watch Later",
            # "Save to playlist",
            # "Download",
            # "Share",
            # "Not interested",
            # "Don't recommend channel",
            # "Report"
            "\U000F0411",  #playlist play
            "\U000F0954", #clock
            "\U000F0412", #playlist plus
            "\U000F0B8F", #download outline
            "\U000F0932", #share outline
            "\U000F073A", #cancel
            "\U000F0377", #"minus-circle-outline"
            "\U000F023B", #flag
        ]
        for i in range(8):
            bLayout = BoxLayout()
            btn = Button(
                    text=f' {textlist[i]}', 
                    # text= u"\U000F05C7 " + "test", 
                    size_hint_y=None, 
                    font_name='materialdesignicons-webfont.ttf',
                    font_size= dp(30),
                    # size= (300, 40), 
                    height=36,
                    # width=3000,
                    # text_size= (150, 30),
                    # text_size= (170, 44),
                    # text_size= (253, 36), #the acutal size
                    text_size= (240, 30), #resized to fit text properly
                    halign= 'left',
                    )
            btn.id= "ddID" + str(i) #https://stackoverflow.com/questions/52151553/how-to-set-kivy-widget-id-from-python-code-file
            btn.on_release = lambda: print(btn.text + "your console shows a square because it does not have materialdesignicons-webfont.ttf as a font")
            btn.width = 300
            # btn.bind(on_release=lambda btn: self.select(btn.text))
            self.individual_dropdown.add_widget(btn)
            # bLayout.add_widget(btn)
            # lbl = Label(
            #     text= "heya",
            #     font_name="Roboto"
            # )
            # bLayout.add_widget(lbl)

            # self.individual_dropdown.add_widget(bLayout)
    
    def open_dd(self, args):
        #https://stackoverflow.com/questions/67295056/how-do-i-increase-the-width-of-the-dropdown-list-within-a-spinner
        self.option_width = 253
        self.invisible_attacher = Widget(opacity=0, size_hint=(None, None))
        self.add_widget(self.invisible_attacher)
        self.invisible_attacher.pos = (self.center_x - self.option_width/2, self.y)
        self.invisible_attacher.size = (self.option_width, self.height)
        attacher = self.invisible_attacher
        self.bind(pos= self.update_invisible_attacher_pos)
        
        # open th DropDown
        self.individual_dropdown.open(attacher)
        # self.individual_dropdown.open(self)

    def update_invisible_attacher_pos(self, *args):
        self.invisible_attacher.pos= (self.center_x - self.option_width/2, self.y)
        print(self.y)
        # import pdb
        # pdb.set_trace()
        
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