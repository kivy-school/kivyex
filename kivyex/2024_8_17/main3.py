# https://discord.com/channels/423249981340778496/670954354932449290/1274802148756029541

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, RenderContext
from kivy.clock import Clock

class ShaderWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Utilisation de RenderContext pour injecter un shader personnalisé
        self.canvas = RenderContext(use_parent_projection=True,
                                    use_parent_modelview=True,
                                    use_parent_frag_modelview=True)
        Clock.schedule_once(self.draw, 0) #draw on the 1st available frame
        
    def draw(self, *args):
        print("???")
        # Chargement du shader personnalisé
        self.canvas.shader.fs = '''
        #ifdef GL_ES
        precision mediump float;
        #endif

        void main(void) {
            gl_FragColor = vec4(1.0, 0.0, 0.0, 1);  // Rouge
        }
        '''
        with self.canvas.after:
            self.rect = Rectangle(pos=self.pos, size=self.size)

class ShaderApp(App):
    def build(self):
        floatlayout = FloatLayout(size=(600,600))
        s = ShaderWidget(size_hint=(None, None), size=(200,400))
        print("what is s pos at beginning?", s.pos)
        
        floatlayout.add_widget(s)
        s.pos=(100,100)
        return floatlayout

if __name__ == '__main__':
    from kivy.core.window import Window
    Window.always_on_top = True
    ShaderApp().run()