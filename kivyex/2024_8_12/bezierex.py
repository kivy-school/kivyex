from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color

class BezierCurveWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Set the color of the line
            Color(1, 0, 0, 1)  # Red color
            
            # Draw a Bézier curve
            Line(bezier=(100, 100, 150, 200, 300, 200, 400, 100), width=2)

class BezierCurveApp(App):
    def build(self):
        return BezierCurveWidget()

if __name__ == '__main__':
    BezierCurveApp().run()
