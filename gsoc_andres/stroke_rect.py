from stroke_point import StrokePoint


class StrokeRect(object):
    '''
    Rect
    ===================

    A rectangle implementation for getting bounds of objects::

        # Create a StrokeRect
        pointA = Point(2,3)
        pointB = Point(4,5)
        rect = StrokeRect(pointA, pointB)
    '''

    def __init__(self, p1, p2):
        ''' Initialize a Rectangle by using two points'''
        self.pt1 = p1.to_float()
        self.pt2 = p2.to_float()
        self.left = min(self.pt1.X, self.pt2.X)
        self.top = max(self.pt1.Y, self.pt2.Y)
        self.right = max(self.pt1.X, self.pt2.X)
        self.bottom = min(self.pt1.Y, self.pt2.Y)
        self.width = self.right - self.left
        self.height = self.top - self.bottom

    def contains(self, p):
        ''' Returns whether or not a stroke_point is inside the rectangle '''
        return (self.left <= p.X <= self.right and
                self.top <= p.Y <= self.bottom)

    def overlaps(self, rect):
        ''' Returns whether or not two strokerects overlap '''
        return (self.right > rect.left and self.left < rect.right and
                self.top < rect.bottom and self.bottom > rect.top)

    def top_left(self):
        '''Get the top-left corner stroke_point'''
        return StrokePoint(self.left, self.top)

    def bottom_right(self):
        '''Get the bottom right corner stroke_point'''
        return StrokePoint(self.right, self.bottom)

    def __str__(self):
        return "<Rect (%s,%s) - (%s,%s)>" % (self.left, self.top,
                                             self.right, self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               StrokePoint(self.left, self.top),
                               StrokePoint(self.right, self.bottom))
