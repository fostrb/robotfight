from engine.vector import Vector
from engine.polygon import Polygon

import random

class Entity(object):
    def __init__(self, polygon=None, heading=None, position=None):
        self.body = Polygon(polygon)
        self.heading = heading
        self.position = position

        self.heading = random.randint(0,360)
        self.position = Vector([0,0])

    def translate(self, vector):
        self.position += vector

    def rotate(self, angle_degrees):
        self.heading += angle_degrees
        self.heading %= 360

    def update(self):
        #self.translate([1,1])
        #self.rotate(1)
        self.body.project(heading=self.heading, position=self.position)

    def intersects(self, other):
        if isinstance(other, Entity):
            if self.position.distance(other.position) < self.body.radius + other.body.radius:
                return True
        else:
            if self.position.distance(other.position) < self.body.radius + other.radius:
                return True
        return False

if __name__ == '__main__':
    e = Entity(polygon=[[0,0],[0,10],[5,5]])
    d = Entity(polygon=[[0,0],[0,10],[5,5]])
    e.translate([1,1])
    e.rotate(90)
    d.update()
    e.update()
    print(e.intersects(d))
