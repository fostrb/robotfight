import math
import time
from rob_components.rmodule import RModule


class Sensor(RModule):
    def __init__(self, name='', energy=0, scanner_cb=None, cooldown=None):
        super(Sensor, self).__init__(name=name, energy=energy, cooldown=cooldown)
        self.scanner_cb = scanner_cb


class ArcScanner(Sensor):
    name = "ArcScanner"
    energy = 10
    cooldown = 3
    def __init__(self, source, scanner_cb=None):
        super(ArcScanner, self).__init__(name=self.name, energy=self.energy, scanner_cb = scanner_cb, cooldown=self.cooldown)
        self.source = source
        self.arc_width = 30
        self.arc_length = 200
        self.last_scan = 0
        self.cooldown_timer = 0

    def scan(self, angle_degrees, position, color):
        if self.cooldown_timer <= 0:
            rvals = []
            rvals = self.scanner_cb(self.source, angle_degrees, position, self.arc_width, self.arc_length, color)
            self.cooldown_timer = self.cooldown
            return rvals
        else:
            return False

