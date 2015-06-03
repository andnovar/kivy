from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty
from random import random
from kivy.graphics import Color, Rectangle, Point, GraphicException, Ellipse, Line, SmoothLine

from math import sqrt
from colorsys import hsv_to_rgb
from gi.overrides.GLib import Source
from stroke import Stroke

from enum import Enum, unique

from stroke import Stroke
from point import Point
from kivy.event import EventDispatcher

class InkCanvasBehavior(EventDispatcher):
    
    '''InkCanvas behavior.
    
    :Events:
        `on_touch_down`
            Fired when the element is touched.
        `on_touch_move`
            Fired when the element keeps being touched while the finger moves.
        `on_touch_up`
            Fired when a touch is lifted up.
    
    .. versionadded:: 1.9.0
    
    '''
    
    @unique
    class Mode(Enum):
        '''Diferent Modes for the InkCanvas, Allows for drawing, erase and touch.        
        '''
        draw = 1
        erase = 2
        touch = 3
    
    strokes = ListProperty([])
    mode = ObjectProperty(Mode.draw)
    
    def __init__(self, **kwargs):
        self.register_event_type('on_stroke_added')
        self.register_event_type('on_stroke_removed')
        super(InkCanvasBehavior, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        #capture touch and add group_id to stroke to associate it
        if super(InkCanvasBehavior, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            touch.grab(self)
            ud = touch.ud
            ud['group'] = g = str(touch.uid)
            pt = Point(touch.x, touch.y)
            if self.mode == self.Mode.draw:
                strk = Stroke(group_id=g)
                strk.isHighlighter(0.5)
                strk.points.append(pt)
                touch.ud['stroke'] = strk
                '''Calculate point size according to pressure'''
                #if 'pressure' in touch.profile:
                with self.canvas:
                    Color(*strk.color)
                    touch.ud['line'] = Line(points = (pt.X, pt.Y), width = 2.0, group=g)
            elif self.mode == self.Mode.erase:
                self.remove_stroke(pt)
    
    def on_touch_move(self, touch):
        '''If pressure changed recalculate the point size'''
        if super(InkCanvasBehavior, self).on_touch_move(touch):
            return True
        if touch.grab_current is self:
            pt = Point(touch.x, touch.y)
            if self.mode == self.Mode.draw:
                touch.ud['stroke'].points.append(pt)
                touch.ud['line'].points += [pt.X, pt.Y]
            elif self.mode == self.Mode.erase:
                self.remove_stroke(pt) 

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            if self.mode == self.Mode.draw:
                self.add_stroke(touch.ud['stroke'])
            elif self.mode == self.Mode.erase:
                pass
            touch.ungrab(self)
            #Fire event when created a new Stroke
        else:
            return super(InkCanvasBehavior, self).on_touch_up(touch)

    def add_stroke(self, strk):
        self.strokes.append(strk)
        self.dispatch('on_stroke_added', strk)

    def remove_stroke(self, pt):
        for strk in self.strokes:
            if strk.hit_test(pt):
                self.canvas.remove_group(strk.group_id)
                self.dispatch('on_stroke_removed', strk)
                if strk in self.strokes:
                    self.strokes.remove(strk)

    def on_stroke_added(self, strk):
        pass

    def on_stroke_removed(self, strk):
        pass