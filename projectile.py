import math
from engine import Vector
import cairo
import time


class Projectile(object):
    def __init__(self, heading, sourcebot):
        self.heading = heading % 360
        self.sourcebot = sourcebot

        self.radius = 2
        self.position = [self.sourcebot.position[0], self.sourcebot.position[1]]

        self.speed = 10
        self.velocity = self.calc_velocity()
        self.damage = 10
        self.init_position()

    def init_position(self):
        radians = math.radians(self.heading)
        dx = math.cos(radians) * self.sourcebot.body.radius+self.radius + 1
        dy = math.sin(radians) * self.sourcebot.body.radius+self.radius + 1
        self.position[0] += dx
        self.position[1] += dy


    def calc_velocity(self):
        radians = math.radians(self.heading)
        dx = math.cos(radians) * self.speed
        dy = math.sin(radians) * self.speed
        return Vector(dx, dy)

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, ctx):
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_line_width(1)
        ctx.set_source_rgb(*self.sourcebot.color)
        ctx.arc(self.position[0], self.position[1], self.radius, 0, math.pi*2)
        ctx.fill()

