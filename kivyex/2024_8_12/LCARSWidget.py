from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse

class LCARSWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Set the color for the main shape
            Color(1, 0.6, 0, 1)  # LCARS orange
            
            # Define dimensions
            rect_x, rect_y = 100, 100
            rect_width, rect_height = 300, 100
            corner_radius = 50
            arc_width = 150  # Width of the arc
            arc_height = 50  # Height of the arc
            
            # Draw the main rounded rectangle
            # Vertical and Horizontal rectangles
            Rectangle(pos=(rect_x + corner_radius, rect_y), size=(rect_width - corner_radius, rect_height))
            Rectangle(pos=(rect_x, rect_y + corner_radius), size=(rect_width, rect_height - corner_radius))
            
            # Draw corners using ellipses
            Ellipse(pos=(rect_x, rect_y), size=(corner_radius * 2, corner_radius * 2))
            Ellipse(pos=(rect_x + rect_width - corner_radius * 2, rect_y), size=(corner_radius * 2, corner_radius * 2))
            Ellipse(pos=(rect_x, rect_y + rect_height - corner_radius * 2), size=(corner_radius * 2, corner_radius * 2))
            Ellipse(pos=(rect_x + rect_width - corner_radius * 2, rect_y + rect_height - corner_radius * 2), size=(corner_radius * 2, corner_radius * 2))
            
            # Subtract the arc by drawing an ellipse with the background color
            Color(0, 0, 0, 1)  # Assuming the background is black
            Ellipse(pos=(rect_x + rect_width - arc_width * 1.5, rect_y + rect_height - arc_height), size=(arc_width * 2, arc_height * 2))

class LCARSApp(App):
    def build(self):
        return LCARSWidget()

if __name__ == '__main__':
    LCARSApp().run()
