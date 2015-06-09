from matplotlib.figure import Figure
from numpy import arange, sin, pi
from kivy.app import App

from backend_kivyagg import FigureCanvasKivyAgg as FigureCanvas
from kivy.uix.floatlayout import FloatLayout

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2 * pi * t)
a.plot(t, s)

canvas = FigureCanvas(f)


class MatplotlibTest(App):
    title = 'Matplotlib Test'

    def build(self):
        fl = FloatLayout()
        fl.add_widget(canvas.widget)
        return fl

if __name__ == '__main__':
    MatplotlibTest().run()
