from kivy.app import App
from stroke_canvas import StrokeCanvasBehavior, CanvasMode
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from stroke import Stroke

from functools import partial
from stroke_rect import StrokeRect
  
class InkCanvasFloat(StrokeCanvasBehavior, FloatLayout):
    def __init__(self, **kwargs):
        super(InkCanvasFloat, self).__init__(**kwargs)
  
class InkCanvasTest(App):
    title = 'InkCanvas'

    def callback(self, button, result, *args):
        if self.inkc.mode == CanvasMode.draw:
            self.inkc.mode = CanvasMode.erase
            button.text = 'Erase Mode'
        elif self.inkc.mode == CanvasMode.erase:
            self.inkc.mode = CanvasMode.draw
            button.text = 'Draw Mode'

    def stroke_collected(self, layout, stroke):
        print "Stroke collected called", stroke
        # Just to visualize the bounding box
        rect = stroke.get_bounds()
        with self.inkc.canvas:
            Color(*stroke.Color.Yellow + (0.5,))
            Rectangle(pos = (rect.left, rect.bottom), size = (rect.right-rect.left, rect.top - rect.bottom))

    def stroke_removed(self, layout, strk):
        print "Stroke removed called", strk
    
    def mode_changed(self, instance, value):
        print "InkCanvas mode changed", value

    def build(self):
        self.inkc = inkc = InkCanvasFloat()
        inkc.bind(size=self._update_rect, pos = self._update_rect)
        inkc.bind(on_stroke_added = self.stroke_collected)
        inkc.bind(on_stroke_removed = self.stroke_removed)
        inkc.bind(mode = self.mode_changed)
        btn = Button(text='Change Mode', size_hint = (1,.15))
        btn.bind(on_press=partial(self.callback, btn))
        inkc.add_widget(btn)
        with inkc.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(size = inkc.size, pos = inkc.pos)
        return inkc
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
      
    def on_pause(self):
        return True
  
if __name__ == '__main__':
    InkCanvasTest().run()