from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics.tesselator import Tesselator
from kivy.graphics import Mesh

import numpy as np

# https://discord.com/channels/423249981340778496/614483622409535489/1274478812591161356

KV = """
MeshTest:
"""

class MeshTest(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tess = Tesselator()
        tess.add_contour([0, 0,
                          100, 0,
                          *Bspline().generate([100,0],[200,0],[200,100])[2:],
                          200,100,
                          200,200,
                          100,200,
                          *Bspline().generate([100,200],[0,200],[0,100])[2:]])
        if not tess.tesselate():
            print("Tesselator didn't work :(")
            return
        for vertices, indices in tess.meshes:
            self.canvas.add(Mesh(
                vertices=vertices,
                indices=indices,
                mode="triangle_fan"
            ))

class Bspline:

    def generate(self, p1, p2, p3):
        control_points = np.array([p1, p2, p3])
        points = self.bspline(control_points).flatten()
        return points

    def de_boor(self, t, x, c):
        d = np.copy(c)
        for r in range(1, 3):
            for j in range(2, r - 1, -1):
                alpha = (x - t[j]) / (t[j + 3 - r] - t[j])
                d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]
        return d[2]

    def bspline(self, c, n=10):
        t = [0, 0, 0, 1, 1, 1]
        u_range = np.linspace(0, 1, n)
        curve = np.array([self.de_boor(t, u, c) for u in u_range])
        return curve


class TestApp(App):

    def build(self):
        return Builder.load_string(KV)

TestApp().run()