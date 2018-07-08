import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
from cairo_display import CairoDisplay
import signal

from cairobot import Robot
import random

from engine import Vector

import threading
import time


class Bout(object):
    def __init__(self, robs):
        self.arena = 1366, 750
        self.robs = []
        for rob in robs:
            self.robs.append(Robot(rob))
        self.initialize_bots()
        self.update_bots()

    def initialize_bots(self):
        for rob in self.robs:
            r = int(rob.body.radius)
            rob.position = Vector(random.randint(r, self.arena[0]-r), random.randint(r, self.arena[1]-r))
            rob.heading = random.randint(0, 360)
            while rob.color is None or sum(rob.color)<1:
                rob.color = random.random(), random.random(),random.random()

    def update_bots(self):
        for rob in self.robs:
            rob.execute()
            rob.update()
            #check out of bounds
            #check collisions
        self.bounds_check()

    def bounds_check(self):
        for rob in self.robs:
            if rob.position[0] <= rob.body.radius or rob.position[0]+rob.body.radius >= self.arena[0]:
                print('oob')
                self.robs.remove(rob)
            elif rob.position[1] <= rob.body.radius or rob.position[1]+rob.body.radius >= self.arena[1]:
                print('oob')
                self.robs.remove(rob)


    def main_loop(self):
        while True:
            time.sleep(.1)
            self.update_bots()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    robs = ['rob1', 'rob2']
    b = Bout(robs)
    c = CairoDisplay(bout=b)
    #threading.Thread(target=lambda: None).start()
    #GObject.threads_init()
    #Gdk.threads.enter()
    Gtk.main()
    exit()

