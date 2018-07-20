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
        self.modules['treads']=Treads

    def run(self):
        scan_angle = random.randint(0,360)
        while True:
            #self.treads.forward()
            #self.treads.turn(-2)
            tvals = self.scanner.scan(scan_angle)
            if tvals is not False:
                if len(tvals) > 0:
                    for target in tvals:
                        #print(target)
                        pass
                    self.laser.fire(scan_angle)
                    #self.cannon1.fire(scan_angle)
                else:
                    scan_angle += 30
                #self.cannon2.fire(90)
            time.sleep(0.01)
