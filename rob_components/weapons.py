import time
from projectile import Projectile
from rob_components.rmodule import RModule
from random import choice

from laser import Laser


class Weapon(RModule):
    def __init__(self, name='', energy=0, cooldown=None):
        super(Weapon, self).__init__(name=name, energy=energy)
        self.cooldown = cooldown


class ATCannon(Weapon):
    name = 'ATCannon'
    energy = 10
    cooldown = 15
    def __init__(self, source=None, projectile_cb=None):
        super(ATCannon, self).__init__(name=self.name, energy=self.energy, cooldown=self.cooldown)
        self.source = source
        self.projectile_cb = projectile_cb
        self.cooldown_timer = 0

        self.exposed = [self.fire]

    def fire(self, angle_degrees):
        if self.cooldown_timer <= 0:
            p = Projectile(angle_degrees, self.source)
            self.projectile_cb(p)
            self.cooldown_timer = self.cooldown

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1


# separate cooldowns for fire and modulate
class LaserEmitter(Weapon):
    name = 'LaserEmitter'
    energy = 20
    cooldown = 150
    modulate_cooldown = 30
    def __init__(self, sourcebot=None, laser_cb=None):
        self.source = sourcebot
        self.laser_cb = laser_cb
        self.colors = [[1,0,0], [0,1,0], [0,0,1]]
        self.color = choice(self.colors)
        self.cooldown_timer = 0

        self.exposed = [self.modulate, self.fire, self.get_color]

    def modulate(self, index):
        if self.cooldown_timer <= 0:
            self.color = self.colors[index]
            self.cooldown_timer = self.modulate_cooldown

    def fire(self, angle_degrees):
        if self.cooldown_timer == 0:
            l = Laser(heading=angle_degrees, sourcebot=self.source, color=self.color)
            self.laser_cb(l)
            self.cooldown_timer = self.cooldown

    def get_color(self):
        return self.color

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1


