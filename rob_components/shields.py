from rob_components.rmodule import RModule
from random import choice


class Shield(RModule):
    def __init__(self, name='', energy=0):
        super(Shield, self).__init__(name=name, energy=energy)


class EnergyShield(Shield):
    name = "EnergyShield"
    energy = 10
    cooldown = 60
    def __init__(self):
        super(EnergyShield, self).__init__(name=self.name, energy=self.energy)
        self.colors = [[1,0,0], [0,1,0], [0,0,1]]
        self.color = choice(self.colors)
        self.cooldown_timer = 0
        self.exposed = [self.modulate, self.get_color]

    def modulate(self, index):
        if self.cooldown_timer <= 0:
            self.color = self.colors[index]
            self.cooldown_timer = self.cooldown

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def get_color(self):
        return self.color

