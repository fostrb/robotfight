import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
from cairo_display import CairoDisplay
import signal


from nbot import Robot
import random

from engine import Vector

import threading
import time

#from rbtest import 
from ROBOTS.mastermind import MasterMind
from ROBOTS.telepath import Telepath
from ROBOTS.mosquito import Mosquito


DESIRED_UPDATES_PER_SECOND = 30


class Bout(object):
    def __init__(self, robs=[]):
        self.arena = 900, 600
        #self.arena = 400, 400
        self.robs = []
        self.projectiles = []
        self.lasers = []
        self.scanner_events = []

        self.sleep_val = 1 / DESIRED_UPDATES_PER_SECOND

        for rob in robs:
            #self.robs.append(Robot(rob, projectile_cb=self.projectile_spawn_cb, scanner_cb=self.scanner_cb, laser_cb=self.laser_cb))
            r = rob().build_robot(self)
            self.robs.append(r)

        self.initialize_bots()
        self.update_bots()
        self.run_bots()

    def start(self):
        self.run_bots()

    def initialize_bots(self):
        for rob in self.robs:
            r = int(rob.body.radius)
            while self.bot_overlap(rob):
                rob.position = Vector(random.randint(r+100, self.arena[0]-r-100), random.randint(r+100, self.arena[1]-r-100))
            rob.heading = random.randint(0, 360)
            while rob.color is None or sum(rob.color) < 1:
                rob.color = random.random(), random.random(),random.random()

    def bot_overlap(self, rob):
        r = int(rob.body.radius)
        rob.position = Vector(random.randint(r+100, self.arena[0]-r-100), random.randint(r+100, self.arena[1]-r-100))
        for b in self.robs:
            if b is not rob:
                if b.intersects(rob):
                    return True
        return False

    def run_bots(self):
        for rob in self.robs:
            t = threading.Thread(target=rob.execute)
            t.daemon = True
            t.start()

    def update(self):
        self.update_bots()
        self.update_projectiles()
        self.modules_update()
        self.scanners_tick()
        self.update_lasers()

    def update_lasers(self):
        for l in self.lasers:
            l.update()
            if l.fade_val <= 0:
                self.lasers.remove(l)

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
        self.laser_collisions()

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
                            self.kill_rob(rob, p.sourcebot.name + " killed")
                        self.projectiles.remove(p)

    def laser_collisions(self):
        for l in self.lasers:
            for rob in self.robs:
                if rob is not l.sourcebot:
                    if l.intersects(rob):
                        rob.hull -= l.damage
                        if rob.hull <=0:
                            self.kill_rob(rob, l.sourcebot.name + " killed")

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
        print(reason + ' ' + rob.name)
        #print(rob.name+ ':' +reason)
        self.robs.remove(rob)

    def projectile_spawn_cb(self, projectile=None):
        self.projectiles.append(projectile)

    def laser_cb(self, laser=None):
        self.lasers.append(laser)

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
        self.scanner_events.append([pos, angle, arc_width, arc_len, color, DESIRED_UPDATES_PER_SECOND])

    def scanners_tick(self):
        for s in self.scanner_events:
            s[5] -= 1
            if s[5] <= 0:
                self.scanner_events.remove(s)

    def modules_update(self):
        for rob in self.robs:
            for m in rob.modules:
                m.update()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    #robs = ['rob1', 'rob2', 'rob3', 'rob4', 'rob5','rob6']
    #robs = ['rob1', 'rob2']
    robs = [MasterMind, Telepath, Mosquito]
    b = Bout(robs)
    c = CairoDisplay(bout=b)
    Gtk.main()
    exit()

