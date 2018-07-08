from engine.vector import Vector


class Polygon(object):
    def __init__(self, points=None):
        self.points = []
        for point in points:
            self.points.append(Vector(point))

        self.reference_points = self.points
        self.initialize_offsets()
        self.calc_radius()

    def initialize_offsets(self):
        x_sum = 0
        y_sum = 0

        for point in self.reference_points:
            x_sum += point.x
            y_sum += point.y
        xavg = x_sum / len(self.reference_points)
        yavg = y_sum / len(self.reference_points)
        
        for point in self.reference_points:
            point.x -= xavg
            point.y -= yavg
        self.points = self.reference_points

    def calc_radius(self):
        d = None
        for point in self.points:
            if not d:
                d = point.distance([0,0])
            else:
                if point.distance([0,0]) > d:
                    d = point.distance([0,0])
        self.radius = d

    def rotate(self, angle_degrees):
        new_points = []
        for point in self.reference_points:
            new_points.append(point.rotated(angle_degrees))
        self.points = new_points

    def translate(self, vector):
        new_points = []
        for point in self.points:
            new_points.append(point+vector)
        self.points = new_points

    def project(self, heading, position):
        self.rotate(heading)
        self.translate(position)

if __name__ == "__main__":
    p = Polygon([[0,0],[0,10], [5,5]])
    
