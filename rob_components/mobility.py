import math
import time
from engine import Vector
from rob_components.rmodule import RModule


class Mobility(RModule):
    def __init__(self, name='', energy=0):
        super(Mobility, self).__init__(name=name, energy=energy)

class Treads(Mobility):
    name = "Treads"
    energy = 10
    speed = 2
    turn_speed = 2

    def __init__(self, sourcebot=None):
        super(Treads, self).__init__(name=self.name, energy=self.energy)
        self.source = sourcebot
        self.exposed = [self.forward, self.turn]

    def forward(self, v=2):
        if v > self.speed:
            v = self.speed
        if v < 0:
            v = 0
        vx = math.cos(math.radians(self.source.heading)) * v
        vy = math.sin(math.radians(self.source.heading)) * v
        self.source.velocity = Vector(vx, vy)

    def turn(self, val):
        if abs(val) > abs(self.turn_speed):
            if val < 0:
                val = self.turn_speed * -1
        self.source.rotation = val

