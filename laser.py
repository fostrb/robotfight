import math
import cairo


class Laser(object):
    def __init__(self, heading, sourcebot, color):
        self.heading = heading
        self.sourcebot = sourcebot
        self.color = color

        self.origin = sourcebot.position

        self.length = 2000
        self.end = []
        self.init_endpoints()
        self.damage = 1

        self.fade_val = 1

    def init_endpoints(self):
        radians = math.radians(self.heading)
        dx = math.cos(radians) * self.length
        dy = math.sin(radians) * self.length
        #self.end = self.origin[0]+dx, self.origin[1]+dy
        self.end = self.origin + [dx, dy]

    def update(self):
        self.fade_val -= .05

    def intersects(self, other):
        # line segment with circle intersect
        return False

    def draw(self, ctx):
        ctx.set_operator(cairo.OPERATOR_ADD)
        i = .1
        while i < 1:
            col = self.color + [i]
            ctx.set_source_rgba(*col)
            ctx.set_line_width(i * 5 * self.fade_val)
            ctx.move_to(self.origin[0], self.origin[1])
            ctx.line_to(self.end[0], self.end[1])
            ctx.stroke()

            i += .1

