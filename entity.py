import math

#    -90
#
# 0   .   180
#
#     90


# TODO: compute proper rotational center (circumcenter for triangle)
#   add __mul__ operator to Point
#   Separate point(vector) polygon and entity classes into Engine module

class Point(object):
    __slots__ = ['x','y']
    def __init__(self, x_or_pair, y=None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __repr__(self):
        return("Point: " + str(self.x) + ', ' + str(self.y))

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y

    def __add__(self, other):
        #print(self)
        x = self.x + other[0]
        y = self.y + other[1]
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other[0]
        y = self.y - other[1]
        return Point(x, y)

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        d = math.sqrt(dx**2+dy**2)
        return d

    def angle_between(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        a = math.atan2(dy, dx)
        return math.degrees(a)

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Point(x, y)


class Polygon(object):
    def __init__(self, points=None):
        self.points = []
        for point in points:
            self.points.append(Point(point))
        #self.position = Point(position)

        self.reference_points = self.points
        self.center = None
        self.initialize_offsets()
        self.calc_radius()

    def initialize_offsets(self):
        # calculates rotational center / offsets points, sets reference points

        # avg method
        xavg= 0
        yavg = 0
        for point in self.reference_points:
            xavg += point.x
            yavg += point.y
        xavg = xavg/len(self.reference_points)
        yavg = yavg/len(self.reference_points)
        for point in self.reference_points:
            point.x -= xavg
            point.y -= yavg
        self.points = self.reference_points

    def rotate(self, angle_degrees):
        new_points = []
        for point in self.reference_points:
            new_points.append(Point(point.rotated(angle_degrees)))
        self.points = new_points

    def translate(self, vector):
        new_points = []
        for point in self.reference_points:
            #point.x = point.x + vector[0]
            #point.y = point.y + vector[1]
            #new_points.append(Point(point.x + vector[0], point.y + vector[1]))
            new_points.append(point + vector)
        self.points = new_points

    def calc_radius(self):
        d = 0
        for point in self.reference_points:
            if point.distance(Point(0,0)) > d:
                d = point.distance(Point(0,0))
        self.radius = d


# takes up physical space (polygon)
# does / doesn't block
class Entity(object):
    def __init__(self, blocking=True, polygon=None, position=None, heading=None):
        self.blocking = blocking
        self.body = polygon
        self.position = Point(position)
        self.heading = 0

        self.velocity = [0,0]

    def get_points(self):
        points = []
        for point in self.body.points:
            points.append([point.x, point.y])
        return points

    def rotate(self, angle_degrees):
        self.heading += angle_degrees

    def translate(self, vector):
        self.position += vector

    def update(self):
        self.translate(self.velocity)
        self.body.rotate(self.heading)
        self.body.translate(self.position)

    def intersects(self, other):
        if isinstance(other, Entity):
            if other.position.distance(self.position) <= self.body.radius + other.body.radius:
                return True
        return False


if __name__ == '__main__':
    points = [[0,0],[10,0],[5,10]]
    position = [20,20]
    p = Polygon(points=points, position=position)
    Entity(blocking=True, polygon=p)

