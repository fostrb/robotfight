import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
from cairo_display import CairoDisplay
import signal

from cairobot import Robot
import random

from projectile import Projectile

from engine import Vector

import threading
import time


class Bout(object):
    def __init__(self, robs):
        self.arena = 900, 600
        #self.arena = 100, 100
        self.robs = []
        self.projectiles = []
        for rob in robs:
            self.robs.append(Robot(rob, projectile_cb=self.projectile_spawn_cb))
        self.initialize_bots()
        self.update_bots()
        self.run_bots()

    def initialize_bots(self):
        for rob in self.robs:
            r = int(rob.body.radius)
            rob.position = Vector(random.randint(r, self.arena[0]-r), random.randint(r, self.arena[1]-r))
            rob.heading = random.randint(0, 360)
            while rob.color is None or sum(rob.color)<1:
                rob.color = random.random(), random.random(),random.random()

    def run_bots(self):
        for rob in self.robs:
            t = threading.Thread(target=rob.execute)
            t.daemon = True
            t.start()

    def update_bots(self):
        for rob in self.robs:
            rob.update()
            #check out of bounds
            #check collisions
        self.bounds_check()
        self.rob_collisions()
        self.proj_collisions()

    def rob_collisions(self):
        for i in range(len(self.robs)):
            rob = self.robs[i]
            for j in range(i+1, len(self.robs)):
                if self.robs[j].intersects(rob):
                    print("collision " + rob.name + ', ' + self.robs[j].name)

    def proj_collisions(self):
        for p in self.projectiles:
            for rob in self.robs:
                if rob.intersects(p):
                    rob.hull -= p.damage
                    self.projectiles.remove(p)

    def bounds_check(self):
        for rob in self.robs:
            if rob.position[0] <= rob.body.radius or rob.position[0]+rob.body.radius >= self.arena[0]:
                print('oob')
                self.robs.remove(rob)
            elif rob.position[1] <= rob.body.radius or rob.position[1]+rob.body.radius >= self.arena[1]:
                print('oob')
                self.robs.remove(rob)

        for p in self.projectiles:
            if p.position[0] <= p.radius or p.position[0] + p.radius >= self.arena[0]:
                self.projectiles.remove(p)
            elif p.position[1] <= p.radius or p.position[1] + p.radius >= self.arena[1]:
                self.projectiles.remove(p)


    def main_loop(self):
        self.run_bots()
        while True:
            time.sleep(.1)
            self.update_bots()

    def projectile_spawn_cb(self, sourcebot, angle_degrees):
        p = Projectile(angle_degrees, sourcebot)
        self.projectiles.append(p)
        t = threading.Thread(target=p.execute)
        t.daemon = True
        t.start()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    robs = ['rob1', 'rob2', 'rob3']
    b = Bout(robs)
    c = CairoDisplay(bout=b)
    #threading.Thread(target=lambda: None).start()
    #GObject.threads_init()
    #Gdk.threads.enter()
    Gtk.main()
    exit()

