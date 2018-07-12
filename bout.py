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
        self.arena = 900, 600
        #self.arena = 400, 400
        self.robs = []
        self.projectiles = []
        
        self.scanner_events = []
        
        for rob in robs:
            self.robs.append(Robot(rob, projectile_cb=self.projectile_spawn_cb, scanner_cb=self.scanner_cb))
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

    def update(self):
        self.update_bots()
        self.update_projectiles()

    def update_projectiles(self):
        for p in self.projectiles:
            p.update()

    def update_bots(self):
        for rob in self.robs:
            if rob.alive:
                rob.update()
                if rob.hull <= 0:
                    self.kill_rob(rob, "dead")
        self.bounds_check()
        self.rob_collisions()
        self.proj_collisions()

    def rob_collisions(self):
        for i in range(len(self.robs)):
            rob = self.robs[i]
            for j in range(i+1, len(self.robs)):
                if self.robs[j].intersects(rob):
                    #print("collision " + rob.name + ', ' + self.robs[j].name)
                    pass

    def proj_collisions(self):
        for p in self.projectiles:
            for rob in self.robs:
                if rob is not p.sourcebot:
                    if rob.intersects(p):
                        rob.hull -= p.damage
                        if rob.hull <= 0 :
                            self.kill_rob(rob, "killed by "+ p.sourcebot.name)
                        self.projectiles.remove(p)

    def bounds_check(self):
        for rob in self.robs:
            if rob.position[0] <= rob.body.radius or rob.position[0]+rob.body.radius >= self.arena[0]:
                self.kill_rob(rob, "OOB")

            elif rob.position[1] <= rob.body.radius or rob.position[1]+rob.body.radius >= self.arena[1]:
                self.kill_rob(rob, "OOB")

        for p in self.projectiles:
            if p.position[0] <= p.radius or p.position[0] + p.radius >= self.arena[0]:
                self.projectiles.remove(p)
            elif p.position[1] <= p.radius or p.position[1] + p.radius >= self.arena[1]:
                self.projectiles.remove(p)

    def kill_rob(self, rob, reason):
        rob.alive = False
        print(rob.name+ ':' +reason)
        self.robs.remove(rob)
        #print(len(self.robs))

    def projectile_spawn_cb(self, projectile=None):
        self.projectiles.append(projectile)

    def scanner_cb(self, source, angle_degrees, position, arc_degrees, arc_length, color):
        start_angle = (angle_degrees - arc_degrees / 2) % 360
        end_angle = (start_angle + arc_degrees) % 360
        rvals = []
        p = Vector(position)
        for rob in self.robs:
            if rob is not source:
                if p.distance(rob.position) < arc_length:
                    angle = rob.position.angle_between(p) % 360
                    if start_angle + arc_degrees > 360:
                        if angle > start_angle or angle < end_angle:
                            
                            rvals.append(rob.position)
                    else:
                        if start_angle < angle < end_angle:
                            rvals.append(rob.position)
        if len(rvals) > 0:
            color = [1,0,0]
        self.scanner_draw(p, angle_degrees, arc_degrees, arc_length, color)
        return rvals

    def scanner_draw(self, pos, angle, arc_width, arc_len, color):
        self.scanner_events.append([pos, angle, arc_width, arc_len, color, time.time()])


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    robs = ['rob1', 'rob2', 'rob3', 'r3', 'asdf','deded']
    #robs = ['rob1', 'rob2']
    b = Bout(robs)
    c = CairoDisplay(bout=b)
    #b.scanner_draw = c.scanner_draw
    #threading.Thread(target=lambda: None).start()
    #GObject.threads_init()
    #Gdk.threads.enter()
    Gtk.main()
    exit()

