from engine import Entity
from engine import Vector
import math
import cairo


robody = [[0,0], [0,10], [15,5]]



class Robot(Entity):
    def __init__(self, name='', polygon=robody):
        super(Robot, self).__init__(polygon=polygon)
        self.name = name
        self.color = None

    def forward(self, val):
        # translate in direction of heading
        vx = math.cos(math.radians(self.heading)) * val
        vy = math.sin(math.radians(self.heading)) * val
        self.translate(Vector(vx, vy))


    def strafe(self, val):
        # translate perpendicular to heading
        pass

    def execute(self):
        # to be initialized as a thread
        #self.rotate(3)
        self.forward(1)

    def draw(self, ctx):
        #body
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_line_width(2)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(self.body.points[0].x, self.body.points[0].y)
        for point in self.body.points:
            ctx.line_to(point[0], point[1])
        ctx.line_to(self.body.points[0].x, self.body.points[0].y)
        ctx.stroke()
        ctx.new_path()

        #circle
        ctx.set_line_width(1)
        ctx.set_source_rgb(0, 1, 0)
        ctx.arc(self.position[0], self.position[1], self.body.radius+1, 0, math.pi*2)
        ctx.stroke()

        #data
        self.draw_text(ctx)

    def draw_text(self, ctx):
        ctx.select_font_face("Courier", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(12)
        (x, y, width, height, dx, dy) = ctx.text_extents(self.name)

        ctx.move_to(self.position[0]-width/2, self.position[1]+self.body.radius + height + 2)
        ctx.show_text(self.name)

if __name__ == '__main__':
    Robot()
