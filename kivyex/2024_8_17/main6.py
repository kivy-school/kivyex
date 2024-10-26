# https://github.com/kivy/kivy/issues/8802

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager

from data_routines import DataRtns

# https://discord.com/channels/423249981340778496/741935529838379028/1148697678004363284
import sys, os
if not sys.stderr:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

from kivy.resources import resource_add_path

if getattr(sys, 'frozen', False):
    resource_add_path(sys._MEIPASS)


class StatLabel(Label):
    def on_text(self, instance, value):
        self.parent.parent.parent.parent.status = value


class Interface(ScreenManager):

    status = "Data Routines"
    err_flg = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clock = Clock.schedule_once(self.process_data, 5)

    def process_data(self, dt):

        if self.status == "Data Routines":
            DataRtns.validate_database(self)
        elif self.status == "Validated Database":
            DataRtns.check_tables(self)
        elif self.status == "Checked Tables":
            DataRtns.check_defaults(self)
        elif self.status == "Checked Defaults":
            self.ids.status_indicator.text = "Finished"

        if self.status != "Finished":

            self.clock.cancel()

            if self.err_flg:
                print(self.ids.status_indicator.text)
                App.get_running_app().stop()
            else:
                self.clock = Clock.schedule_once(self.process_data, 5)


class CandoitApp(App):
    def build(self):
        self.title = "Can Do IT Application"
        # self.icon = "cando.png"


if __name__ == "__main__":
    try:
        CandoitApp().run()
    except Exception as e:
        import traceback
        print("full exception", "".join(traceback.format_exception(*sys.exc_info())))
        import time
        time.sleep(10)

from pygame import mixer