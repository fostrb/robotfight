import time
from projectile import Projectile
from rob_components.rmodule import RModule


class Weapon(RModule):
    def __init__(self, name='', energy=0, cooldown=None):
        super(Weapon, self).__init__(name=name, energy=energy, cooldown=cooldown)
        self.cooldown = cooldown


class ATCannon(Weapon):
    name = 'ATCannon'
    energy = 10
    cooldown = 15
    def __init__(self, source, projectile_cb=None):
        super(ATCannon, self).__init__(name=self.name, energy=self.energy, cooldown=self.cooldown)
        self.source = source
        self.projectile_cb = projectile_cb
        self.cooldown_timer = 0

    def fire(self, angle_degrees):
        if self.cooldown_timer <= 0:
            p = Projectile(angle_degrees, self.source)
            self.projectile_cb(p)
            self.cooldown_timer = self.cooldown
