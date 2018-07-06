from entity import Entity
import math


class Robot(Entity):
    def __init__(self, name='', polygon=None, position=None):
        super(Robot, self).__init__(blocking=True, polygon=polygon, position=position)
        self.name = name

        self.thrust_power = .02


    def thrust(self):
        vy = math.sin(math.radians(self.heading)) * self.thrust_power
        vx = math.cos(math.radians(self.heading)) * self.thrust_power
        self.velocity = [self.velocity[0] + vx, self.velocity[1] + vy]

if __name__ == '__main__':
    r = Robot("rob")

