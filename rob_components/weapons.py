import time
from projectile import Projectile

class Weapon(object):
    def __init__(self, cooldown=None):
        self.cooldown = cooldown


class ATCannon(Weapon):
    def __init__(self, source, projectile_cb=None):
        super(ATCannon, self).__init__(cooldown=.5)
        self.source = source
        self.projectile_cb = projectile_cb

        self.last_fired = 0

    def fire(self, angle_degrees):
        if time.time() - self.last_fired > self.cooldown:
            p = Projectile(angle_degrees, self.source)
            self.projectile_cb(p)
            self.last_fired = time.time()

