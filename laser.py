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
		dx = self.origin[0] - other.position[0]
		dy = self.origin[1] - other.position[1]

		if math.sqrt(dx**2 + dy**2) <= other.body.radius:
			# if either end point exists within other's circle...
			return True
		dot = (((other.position[0] - self.origin[0]) * (self.end[0] - self.origin[0])) + other.position[1] - self.origin[1] * (self.end[1] - self.origin[1])) / self.length**2

		closest_x = self.origin[0] + (dot * (self.end[0] - self.origin[0]))
		closest_y = self.origin[1] + (dot * (self.end[1] - self.origin[1]))

		if not self.line_point(self.origin[0], self.origin[1], self.end[0], self.end[1], closest_x, closest_y):
			return False
		dx = closest_x - other.position[0]
		dy = closest_y - other.position[1]

		distance = math.sqrt(dx**2 + dy**2)

		if distance <= other.body.radius*2:
			return True
		return False

	def line_point(self, x1, y1, x2, y2, px, py):
		dx = px - x1
		dy = py - y1
		d1 = math.sqrt(dx**2 + dy**2)

		dx = px - x2
		dy = py - y2
		d2 = math.sqrt(dx**2 + dy**2)

		buff = 1

		if d1+d2 >= self.length - buff and d1+d2 <= self.length+buff:
			return True


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

