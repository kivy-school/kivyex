# https://github.com/Jean-Jose-Edvach/Kivy_problema_editor/issues/1
# https://discord.com/channels/423249981340778496/670954354932449290/1269454751322476644


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from random import random

class MyPixel(Widget):
    coordenada = []
    pixeis = []
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.label = Label(text='', font_size='20sp', pos=(10, 500))
        self.add_widget(self.label)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.coordenada = self.grade([[int(touch.x),  int(touch.y)]], 20)
            self.pixel(self.coordenada[0])
            

    def pixel(self,coordenadas, *args):
        #self.canvas.before.clear()
        with self.canvas.before:
            Color(
                rgba = [0.4, 0.6, 0.6, 1]
                )
            rec = Rectangle(size=[20, 20], pos=coordenadas)
            
            self.pixeis.append(rec)
            
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
        # Adiciona nova coordenada
            self.coordenada.append([int(touch.x), int(touch.y)])
            
                #self.coordenada.append([int(touch.x), int(touch.y)])
                
            
            # Atualiza as coordenadas usando a função grade
            self.coordenada = self.grade(self.coordenada, 20)
            cont = len(self.coordenada)
                #self.label.text = str(cont)
            # Adiciona um botão se houver exatamente 2 coordenadas e self.dois for True
            if cont == 2 and len(self.pixeis) < 2:
                self.pixel(self.coordenada[1])
                
                    
            
            # Suaviza as coordenadas e adiciona um terceiro botão se houver 3 coordenadas
            elif cont == 3:
                self.coordenada = self.anti_aliasing(self.coordenada)
                cont = len(self.coordenada)
                
                if cont == 3:
                    self.pixel(self.coordenada[2])
                    self.coordenada = self.coordenada[-2:]
                
                    self.pixeis = self.pixeis[-2:]
                    
                        
                    
                elif cont == 2:
                    self.pixeis[0].pos = self.coordenada[0]
                    self.pixeis[1].pos = self.coordenada[1]
                    
                    self.coordenada = self.coordenada[-1:]
                    self.pixeis = self.pixeis[-1:]
                    
                        
            
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

    def on_touch_up(self, touch):
        self.coordenada = []
        self.pixeis = [] 
        self.dois = True 

class MyApp(App):
    def build(self):
        self.title = 'Pixel Editor Proof of Concept'
        return MyPixel()

if __name__ =='__main__':
    #this is to make the Kivy window always on top
    from kivy.core.window import Window
    Window.always_on_top = True
    MyApp().run()