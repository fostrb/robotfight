import math


class Vector(object):
    __slots__ = ['x','y']
    def __init__(self, x_or_pair, y=None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __repr__(self):
        return("["+str(self.x) + ', ' + str(self.y)+"]")

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y

    def __add__(self, other):
        if hasattr(other, "__getitem__"):
            x = self.x + other[0]
            y = self.y + other[1]
        else:
            x = self.x + other
            y = self.y + other
        return Vector(x, y)

    def __sub__(self, other):
        if hasattr(other, "__getitem__"):
            x = self.x - other[0]
            y = self.y - other[1]
        else:
            x = self.x - other
            y = self.y - other
        return Vector(x, y)

    def distance(self, other):
        dx = self.x - other[0]
        dy = self.y - other[1]
        d = math.sqrt(dx**2+dy**2)
        return d

    def angle_between(self, other):
        dx = self.x - other[0]
        dy = self.y - other[1]
        a = math.atan2(dy, dx)
        return math.degrees(a)

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vector(x, y)

