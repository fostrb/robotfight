from rob_components.rmodule import RModule
from random import choice


class Shield(RModule):
    def __init__(self, name='', energy=0, cooldown=None):
        super(Shield, self).__init__(name=name, energy=energy, cooldown=cooldown)


class EnergyShield(Shield):
    name = "EnergyShield"
    energy = 10
    cooldown = 60
    def __init__(self):
        super(EnergyShield, self).__init__(name=self.name, energy=self.energy, cooldown=self.cooldown)
        self.colors = [[1,0,0], [0,1,0], [0,0,1]]
        self.color = choice(self.colors)
        self.cooldown_timer = 0
        self.exposed = [self.modulate, self.get_color]

    def modulate(self, index):
        if self.cooldown_timer <= 0:
            self.color = self.colors[index]
            self.cooldown_timer = self.cooldown

    def get_color(self):
        return self.color

