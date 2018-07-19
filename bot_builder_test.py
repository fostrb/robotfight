from cairobot import Robot
from rob_components import *

e=EnergyShield().gen_interface()

for k, v in e.__dict__.items():
    print(k)

print(e.get_color())
e.modulate(1)
c = e.get_color()
c = 1
print(e.get_color())
