from rbtest import RobController
from rob_components import *
import time


class MasterMind(RobController):
    def __init__(self):
        super(MasterMind, self).__init__()
        self.modules = {}
        self.modules['scanner']=ArcScanner
        self.modules['cannon1']=ATCannon
        self.modules['cannon2']=ATCannon
        self.modules['shield']=EnergyShield
        self.modules['laser']=LaserEmitter
        self.modules['treads']=Treads

    def run(self):
        scan_angle = 0
        while True:
            self.treads.forward()
            self.treads.turn(-2)
            tvals = self.scanner.scan(scan_angle)
            if tvals is not False:
                if len(tvals) > 0:
                    t = self.closest_target(tvals)
                    target_angle = t.angle_between(self.get_position())
                    self.laser.fire(target_angle)
                    self.cannon1.fire(target_angle)
                    scan_angle = target_angle
                    self.scanner.set_length(self.get_position().distance(t)+50)
                else:
                    self.scanner.set_arc_width(30)
                    scan_angle += 30
                #self.cannon2.fire(90)
            time.sleep(0.01)

    def closest_target(self, tvals):
        closest = None
        for target in tvals:
            if closest is None:
                closest = target
            if target.distance(self.get_position()) < self.get_position().distance(closest):
                closest = target
        return closest
