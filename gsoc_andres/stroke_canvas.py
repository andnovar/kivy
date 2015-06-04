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
from stroke_point import StrokePoint
from kivy.event import EventDispatcher

class StrokeCanvasBehavior(object):
    
    '''InkCanvas behavior.
    
    :Events:
        `on_stroke_added`
            Fired when a stroke is drawn in the canvas.
        `on_stroke_removed`
            Fired when a stroke is removed from the canvas.
    
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
        super(StrokeCanvasBehavior, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        #capture touch and add group_id to stroke to associate it
        if super(StrokeCanvasBehavior, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            touch.grab(self)
            ud = touch.ud
            ud['group'] = g = str(touch.uid)
            pt = StrokePoint(touch.x, touch.y)
            if self.mode == self.Mode.draw:
                stroke = Stroke(group_id=g)
                stroke.is_highlighter(0.5)
                stroke.points.append(pt)
                touch.ud['stroke'] = stroke
                '''Calculate stroke_point size according to pressure'''
                #if 'pressure' in touch.profile:
                with self.canvas:
                    Color(*stroke.color)
                    touch.ud['line'] = Line(points=(pt.X, pt.Y),width=2.0,group=g)
            elif self.mode == self.Mode.erase:
                self.remove_stroke(pt)
    
    def on_touch_move(self, touch):
        '''If pressure changed recalculate the stroke_point size'''
        if super(StrokeCanvasBehavior, self).on_touch_move(touch):
            return True
        if touch.grab_current is self:
            pt = StrokePoint(touch.x, touch.y)
            if self.mode == self.Mode.draw:
                touch.ud['stroke'].points.append(pt)
                touch.ud['line'].points += [pt.X, pt.Y]
            elif self.mode == self.Mode.erase:
                self.remove_stroke(pt) 

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            pt = StrokePoint(touch.x, touch.y)
            if self.mode == self.Mode.draw:
                touch.ud['stroke'].points.append(pt)
                self.add_stroke(touch.ud['stroke'])
                touch.ud['stroke'].sampling2()
                print touch.ud['stroke'].sampled_points
                for i in range(1, len(touch.ud['stroke'].sampled_points) - 1):
                    print str(touch.ud['stroke'].sampled_points[i-1].distance_to(touch.ud['stroke'].sampled_points[i])) + ", "
                with self.canvas:
                    Color(0, 0, 1)
                    Line(points = touch.ud['stroke'].get_line_points(), width = 1.0)
            elif self.mode == self.Mode.erase:
                pass
            touch.ungrab(self)
            #Fire event when created a new Stroke
        else:
            return super(StrokeCanvasBehavior, self).on_touch_up(touch)

    def add_stroke(self, stroke):
        self.strokes.append(stroke)
        self.dispatch('on_stroke_added', stroke)

    def remove_stroke(self, pt):
        for stroke in self.strokes:
            if stroke.hit_test(pt):
                self.canvas.remove_group(stroke.group_id)
                self.dispatch('on_stroke_removed', stroke)
                if stroke in self.strokes:
                    self.strokes.remove(stroke)

    def on_stroke_added(self, stroke):
        pass

    def on_stroke_removed(self, stroke):
        pass