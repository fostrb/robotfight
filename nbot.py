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

    def draw(self, ctx):
        #body
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_line_width(1)

        col = [*self.color] + [0.7]

        ctx.set_source_rgba(*col)
        ctx.move_to(self.body.points[0].x, self.body.points[0].y)
        for point in self.body.points:
            ctx.line_to(point[0], point[1])
        ctx.line_to(self.body.points[0].x, self.body.points[0].y)
        ctx.fill()

        ctx.set_source_rgb(*self.color)
        ctx.move_to(self.body.points[0].x, self.body.points[0].y)
        for point in self.body.points:
            ctx.line_to(point[0], point[1])
        ctx.line_to(self.body.points[0].x, self.body.points[0].y)
        ctx.stroke()

        # energy shield
        '''
        shield_color = self.shield.color + [.3]
        ctx.set_source_rgba(*shield_color)
        ctx.arc(self.position[0], self.position[1], self.body.radius+1, 0, math.pi*2)
        ctx.fill()
        '''
        self.draw_data(ctx)

    def draw_data(self, ctx):
        #circle
        ctx.set_line_width(1)
        ctx.set_source_rgb(0, 1, 0)
        ctx.arc(self.position[0], self.position[1], self.body.radius+1, 0, math.pi*2)
        ctx.stroke()

        #data
        self.draw_text(ctx)

    def draw_text(self, ctx):
        ctx.set_source_rgb(*self.color)
        ctx.select_font_face("Courier", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(12)
        (x, y, width, height, dx, dy) = ctx.text_extents(self.name)

        ctx.move_to(self.position[0]-width/2, self.position[1]+self.body.radius + height + 2)
        ctx.show_text(self.name)

        hull_str = str(self.hull)
        r = 1-.01*self.hull
        g = .01*self.hull
        ctx.set_source_rgb(r, g, 0)
        (x, y, width, height, dx, dy) = ctx.text_extents(hull_str)
        ctx.move_to(self.position[0] - width/2, self.position[1]- self.body.radius - height + 2)
        ctx.show_text(hull_str)


if __name__ == '__main__':
    Robot()

