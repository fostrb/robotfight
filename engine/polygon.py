from engine.vector import Vector

# circumcenter locating functions need to be tested---
def distance(A, B):
    n = len(A)
    assert len(B) == n
    return sum((A[i]-B[i])**2 for i in range(n))**0.5

def cosine(A, B, C):
    a, b, c = distance(B, C), distance(A, C), distance(A, B)
    return (a*a+c*c-b*b)/(2*a*c)

def barycentric(A, B, C, p, q, r):
    n = len(A)
    assert len(B) == len(C) == n
    s = p + q + r
    p, q, r = p/s, q/s, r/s
    return tuple([p*A[i]+q*B[i]+r*C[i] for i in range(n)])

def trilinear(A, B, C, alpha, beta, gamma):
    a = distance(B, C)
    b = distance(A, C)
    c = distance(A, B)
    return barycentric(A, B, C, a*alpha, b*beta, c*gamma)

def circumcenter(A, B, C):
    cosA = cosine(C, A, B)
    cosB = cosine(A, B, C)
    cosC = cosine(B, C, A)
    return trilinear(A, B, C, cosA, cosB, cosC)
# ^^^circumcenter locating functions need to be tested^^^

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
    
