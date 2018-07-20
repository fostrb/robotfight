from rbtest import RobController
from rob_components import *
import random
import time


class Telepath(RobController):
    def __init__(self):
        super(Telepath, self).__init__()
        self.modules = {}
        self.modules['scanner']=ArcScanner
        self.modules['cannon1']=ATCannon
        #self.modules['cannon2']=ATCannon
        #self.modules['shield']=EnergyShield
        self.modules['laser']=LaserEmitter
        self.modules['laser2']=LaserEmitter
        self.modules['treads']=Treads

    def run(self):
        scan_angle = random.randint(0,360)
        s_len = self.scanner.get_length()
        while True:
            self.scanner.set_length(s_len)
            #self.treads.forward()
            #self.treads.turn(-2)
            tvals = self.scanner.scan(scan_angle)
            if tvals is not False:
                if len(tvals) > 0:
                    t = self.closest_target(tvals)
                    t_angle = t.angle_between(self.get_position())
                    self.laser.fire(t_angle)
                    self.laser2.fire(t_angle)
                    self.cannon1.fire(t_angle)
                    s_len = self.get_position().distance(t) + 50
                    #self.scanner.set_length(self.get_position().distance(t) + 50)
                    scan_angle = t_angle
                else:
                    if s_len < 700:
                        s_len += 10
                    scan_angle += self.scanner.get_arc_width()
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
