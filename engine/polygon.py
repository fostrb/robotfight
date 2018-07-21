from engine.vector import Vector


def distance(A,B):
    n = len(A)
    assert len(B) == n
    return sum((A[i]-B[i])**2 for i in range(n))**0.5

# Cosine of angle ABC
def cosine(A,B,C):
    a,b,c = distance(B,C), distance(A,C), distance(A,B)
    return (a*a+c*c-b*b)/(2*a*c)

# Cartesian coordinates of the point whose barycentric coordinates
# with respect to the triangle ABC are [p,q,r]
def barycentric(A,B,C,p,q,r):
    n = len(A)
    assert len(B) == len(C) == n
    s = p+q+r
    p, q, r = p/s, q/s, r/s
    return tuple([p*A[i]+q*B[i]+r*C[i] for i in range(n)])

# Cartesian coordinates of the point whose trilinear coordinates
# with respect to the triangle ABC are [alpha,beta,gamma]
def trilinear(A,B,C,alpha,beta,gamma):
    a = distance(B,C)
    b = distance(A,C)
    c = distance(A,B)
    return barycentric(A,B,C,a*alpha,b*beta,c*gamma)

# Cartesian coordinates of the circumcenter of triangle ABC
def circumcenter(A,B,C):
    cosA = cosine(C,A,B)
    cosB = cosine(A,B,C)
    cosC = cosine(B,C,A)
    return trilinear(A,B,C,cosA,cosB,cosC)

class Polygon(object):
    def __init__(self, points=None):
        self.points = []
        for point in points:
            self.points.append(Vector(point))

        self.reference_points = self.points
        self.initialize_offsets()
        self.calc_radius()

    def initialize_offsets(self):
        # this is offset initialization for a triangle.
        # calc circumcenter, zero reference points around it, calc radius.
        pts = []
        for p in self.reference_points:
            pts.append([p[0],p[1]])

        ccenter = circumcenter(*pts)
        newpoints = []
        for point in self.reference_points:
            newpoints.append(point - ccenter)
        self.reference_points = newpoints
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

