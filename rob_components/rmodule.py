
class RMInterface(object):
    def __init__(self, em=[]):
        for m in em:
            setattr(self, m.__name__, m)



class RModule(object):
    def __init__(self, name='', energy=0, cooldown=0):
        self.name = name
        self.energy = energy
        self.cooldown = cooldown

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def gen_interface(self):
        return RMInterface(self.exposed)
