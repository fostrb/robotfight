from rbtest import RobController
from rob_components import *
import random
import time


class Mosquito(RobController):
    def __init__(self):
        super(Mosquito, self).__init__()
        self.modules = {}
        self.modules['scanner']=ArcScanner
        self.modules['cannon']=ATCannon
        #self.modules['cannon2']=ATCannon
        #self.modules['shield']=EnergyShield
        self.modules['laser']=LaserEmitter
        self.modules['treads']=Treads

    def run(self):
        scan_angle = self.get_heading()+90
        self.scanner.set_arc_width(180)
        while True:
            self.treads.forward()
            self.treads.turn(2)
            tvals = self.scanner.scan(scan_angle)
            if tvals is not False:
                if len(tvals) > 0:
                    for target in tvals:
                        self.pursuit(target)
                else:
                    self.scanner.set_arc_width(180)
                    scan_angle += 180
            time.sleep(0.01)

    def pursuit(self, target):
        self.scanner.set_length(self.get_position().distance(target)+50)
        t_angle = target.angle_between(self.get_position())
        self.cannon.fire(t_angle)
        self.treads.turn(0)
        while True:
            tvals = self.scanner.scan(t_angle)
            if tvals is not False:
                if len(tvals) > 0:
                    p = self.get_position()
                    closest = None
                    for target in tvals:
                        if closest is None:
                            closest = target
                        if p.distance(target) < p.distance(closest):
                            closest = target
                    t_angle = target.angle_between(p)
                    self.scanner.set_length(p.distance(closest)+50)
                    self.cannon.fire(t_angle)
                    self.laser.fire(t_angle)
                else:
                    self.scanner.set_arc_width(180)
                    return
            time.sleep(0.01)

            
