from engine import Entity
import math
import cairo


robody = [[0,0], [0,10], [15,5]]



class Robot(Entity):
    def __init__(self, name='', polygon=robody):
        super(Robot, self).__init__(polygon=polygon)
        self.name = name
        self.color = None

    def draw(self, ctx):
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.set_line_width(1)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(self.body.points[0].x, self.body.points[0].y)
        for point in self.body.points:
            ctx.line_to(point[0], point[1])
        ctx.line_to(self.body.points[0].x, self.body.points[0].y)
        ctx.stroke()
        ctx.new_path()

        ctx.set_source_rgb(0, 1, 0)


if __name__ == '__main__':
    Robot()
