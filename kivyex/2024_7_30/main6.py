# https://github.com/Jean-Jose-Edvach/Kivy_problema_editor/issues/1#issue-2446539975
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.lang import Builder
kvString = '''
<PButton@Button>:
    canvas:
        Color:
            rgba: 0, 0, 1, 1
        Rectangle:
            size: self.width, self.height
            pos: self.pos
    background_normal: ''
    background_down: ''
    background_disabled_normal: ''
    background_disabled_down: ''

'''
class PButton(Button):
    pass

class MyPixel(Widget):
    coordenada = []
    dois = True
    pixeis = []
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.label = Label(text='')
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.coordenada = self.grade([[int(touch.x),  int(touch.y)]], 60)
            botao = PButton( size_hint=(None, None), size=(60, 60), pos=self.coordenada[0])
            self.add_widget(botao)
            self.pixeis.append(botao)


    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
        # Adiciona nova coordenada
            self.coordenada.append([int(touch.x), int(touch.y)])
        
        # Atualiza as coordenadas usando a função grade
            self.coordenada = self.grade(self.coordenada, 60)
            cont = len(self.coordenada)
        
        # Adiciona um botão se houver exatamente 2 coordenadas e self.dois for True
            if cont == 2 and self.dois:
                botao = PButton(size_hint=(None, None), size=(60, 60), pos=self.coordenada[1])
                self.add_widget(botao)
                self.pixeis.append(botao)
                self.dois = False
        
        # Suaviza as coordenadas e adiciona um terceiro botão se houver 3 coordenadas
            elif cont == 3:
                self.coordenada = self.anti_aliasing(self.coordenada)
                cont = len(self.coordenada)
                if cont == 3:
                    botao = PButton(size_hint=(None, None), size=(60, 60), pos=self.coordenada[2])
                    self.coordenada = self.coordenada[-2:]
                    self.add_widget(botao)
                    self.pixeis = self.pixeis[-2:]
                    self.dois = True
                elif cont == 2:
                    self.pixeis[0].pos = self.coordenada[0]
                    self.pixeis[1].pos = self.coordenada[1]
                    self.coordenada = self.coordenada[-1:]
                    self.pixeis = self.pixeis[-1:]
                    self.dois = True
        
        # Atualiza a tela
        self.canvas.ask_update()
        
            
    def grade(self, coordenadas, size = 10):
        grad_x = (coordenadas[0][0] // size) * size
        grad_y = (coordenadas[0][1] // size) * size
        
        lista = [[grad_x,  grad_y]]
        
        if len(coordenadas) > 1:
            grad_x2 = (coordenadas[1][0] // size) * size
            grad_y2 = (coordenadas[1][1] // size) * size
            
            if grad_y == grad_y2 and \
            grad_x != grad_x2 or \
            grad_x == grad_x2 and \
            grad_y != grad_y2 or \
            grad_x != grad_x2 and \
            grad_y != grad_y2:
                lista.append([grad_x2, grad_y2])
            
        if len(coordenadas) > 2:
            grad_x3 = (coordenadas[2][0] // size) * size
            grad_y3 = (coordenadas[2][1] // size) * size
            if grad_x2 == grad_x3 and \
            grad_y2 != grad_y3 or \
            grad_y2 == grad_y3 and \
            grad_x2 != grad_x3 or \
            grad_y2 != grad_y3 and \
            grad_x2 != grad_x3:
                lista.append([grad_x3,  grad_y3])
            
        return lista
        
    def anti_aliasing(self, posicao):
        
        
        colocar_x3 = False
        
        if posicao[0][1] == posicao[1][1] and posicao[2][0] == posicao[1][0] and posicao[1][1] != posicao[2][1]:
            posicao[1][1] = posicao[2][1]
        
        elif posicao[0][0] == posicao[1][0] and posicao[2][1] == posicao[1][1] and posicao[1][0] != posicao[2][0]:
            posicao[1][0] = posicao[2][0] 
        
        else:
            colocar_x3 = True
        
        lista = [[posicao[0][0], posicao[0][1]], [posicao[1][0], posicao[1][1]]]
        
        if colocar_x3:
            lista.append([posicao[2][0], posicao[2][1]])
        
        return lista

    def on_touch_up(self, *args):
        self.coordenada = []
        self.pixeis = [] 
        self.dois = True 

class MyApp(App):
    def build(self):
        return MyPixel()

if __name__ == '__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    Builder.load_string(kvString)
    MyApp().run()