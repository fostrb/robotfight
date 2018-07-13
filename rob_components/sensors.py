import math
import time
# TODO
# scan arc drawings should fade out on a timer and dissapate


class Sensor(object):
    def __init__(self, scanner_cb=None, cooldown=0):
        self.scanner_cb = scanner_cb


class ArcScanner(Sensor):
    def __init__(self, source, scanner_cb=None, cooldown=.05):
        super(ArcScanner, self).__init__(scanner_cb = scanner_cb, cooldown=1)
        self.source = source
        self.arc_width = 30
        self.arc_length = 200
        self.cooldown = cooldown
        self.last_scan = 0

    def scan(self, angle_degrees, position, color):
        if time.time() - self.last_scan > self.cooldown:
            rvals = []
            rvals = self.scanner_cb(self.source, angle_degrees, position, self.arc_width, self.arc_length, color)
            self.last_scan = time.time()
            return rvals
        else:
            return False

