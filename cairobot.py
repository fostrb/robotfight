from engine import Entity
from engine import Vector
import math
import cairo
from rob_components import *

import time
import random

robody = [[0,0], [0,10], [15,5]]


class Robot(Entity):
    def __init__(self, name='', polygon=robody, projectile_cb=None, scanner_cb=None):
        super(Robot, self).__init__(polygon=polygon)
        self.name = name
        self.color = None
        self.velocity = Vector(0, 0)
        self.projectile_cb = projectile_cb

        self.alive = True

        self.hull = 100
        self.kills = []

        self.scanner = ArcScanner(self, scanner_cb)
        self.cannon = ATCannon(source=self, projectile_cb=projectile_cb)

    def scan(self, angle):
        rvals = self.scanner.scan(angle, self.position, self.color)
        if len(rvals) > 0:
            return rvals
        else:
            return []

    def forward(self, val):
        vx = math.cos(math.radians(self.heading)) * val
        vy = math.sin(math.radians(self.heading)) * val
        self.velocity = Vector(vx, vy)

    def turn(self, val):
        self.rotation = val

    def execute(self):
        # to be initialized as a thread
        rval = random.randint(-3, 3)
        s_angle = random.randint(0, 360)
        while True:
            if self.alive:
                time.sleep(.05)
                self.forward(.5)
                if random.randint(0, 3) == 0:
                    while rval >= 3 and rval <= -3:
                        rval += random.randint(-3,3)
                if random.randint(0, 50) == 0:
                    rval *= -1

                self.turn(rval)
                tvals = self.scan(s_angle)
                s_angle += 1
                s_angle %=360
                if len(tvals) > 0:
                    for t in tvals:
                        d = None
                        if d is None:
                            d = t
                        elif self.position.distance(t) < self.position.distance(d):
                            d = t
                    angle = Vector(d).angle_between(self.position)
                    self.fire(angle)
                    s_angle = angle
            else:
                return

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
    # exposed functions
    def fire(self, angle_degrees):
        self.cannon.fire(angle_degrees)


if __name__ == '__main__':
    Robot()

