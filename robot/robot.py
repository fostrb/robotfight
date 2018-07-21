from engine import Entity
from engine import Vector
import math
import cairo
from rob_components import *

import time
import random

robody = [[0,0], [0,10], [15,5]]

class Robot(Entity):
    def __init__(self, name='', polygon=robody):
        super(Robot, self).__init__(polygon=polygon)
        self.name = name
        self.color = None
        self.position = Vector(0, 0)
        self.velocity = Vector(0, 0)

        self.modules = []
        self.alive = True

        self.hull = 100
        self.kills = []

    def get_position(self):
        return self.position

    def get_heading(self):
        return self.heading

    def get_hull(self):
        return self.hull

    def get_velocity(self):
        return self.velocity

    def execute(self):
        print(self.name + ' running default execute method.')


# power generation
# module slots
class AlphaClass(Robot):
    polygon = [[0,0], [0,10], [15,5]]
    def __init__(self, name=''):
        self.name = name
        super(AlphaClass, self).__init__(self, name=self.name, polygon=self.polygon)


if __name__ == '__main__':
    AlphaClass()

