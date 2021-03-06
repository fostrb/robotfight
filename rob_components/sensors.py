import math
import time
from rob_components.rmodule import RModule


class Sensor(RModule):
    def __init__(self, name='', energy=0, scanner_cb=None):
        super(Sensor, self).__init__(name=name, energy=energy)
        self.scanner_cb = scanner_cb


class PulseScanner(Sensor):
    name = "PulseScanner"
    energy = 10
    cooldown = 50
    radius = 5000

    def __init__(self, source=None, scanner_cb=None):
        super(PulseScanner, self).__init__(name=self.name, energy=self.energy, scanner_cb = scanner_cb)
        self.source = source
        self.cooldown_timer = 0
        self.exposed = [self.scan]

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def scan(self, position=None, color=None):
        if self.cooldown_timer <= 0:
            position = self.source.position
            color = self.source.color
            rvals = []
            rvals = self.scanner_cb(self.source, 90, position, 360, self.radius, color)
            self.cooldown_timer = self.cooldown
            return rvals
        else:
            return False



class ArcScanner(Sensor):
    name = "ArcScanner"
    energy = 10
    cooldown = 4
    area = 10000

    def __init__(self, source=None, scanner_cb=None):
        super(ArcScanner, self).__init__(name=self.name, energy=self.energy, scanner_cb = scanner_cb)
        self.source = source
        self.arc_width = 30
        self.arc_length = None
        self.cooldown_timer = 0
        self.exposed = [self.scan, self.set_length, self.set_arc_width, self.get_length, self.get_arc_width]
        self.calc_size()

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def scan(self, angle_degrees, position=None, color=None):
        if self.cooldown_timer <= 0:
            position = self.source.position
            color = self.source.color
            rvals = []
            rvals = self.scanner_cb(self.source, angle_degrees, position, self.arc_width, self.arc_length, color)
            self.cooldown_timer = self.cooldown
            return rvals
        else:
            return False

    def calc_size(self):
        if self.arc_width is not None:
            self.arc_length = math.sqrt(self.area/(math.pi*self.arc_width/360))
        elif self.arc_length is not None:
            self.arc_width = self.area/ (math.pi * self.arc_length**2) * 360

        #print((math.pi * self.arc_length**2) * self.arc_width/360)

    def set_length(self, length):
        self.arc_length = length
        self.arc_width = None
        self.calc_size()

    def set_arc_width(self, angle):
        self.arc_width = angle
        self.arc_length = None
        self.calc_size()

    def get_length(self):
        return self.arc_length

    def get_arc_width(self):
        return self.arc_width

