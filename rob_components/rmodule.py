

class RModule(object):
    def __init__(self, name='', energy=0, cooldown=0):
        self.name = name
        self.energy = energy
        self.cooldown = cooldown
        #print(self.name, self.cooldown)

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

