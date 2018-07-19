from robot_builder.rbuilder import RobotBuilder
from rob_components import *
from cairobot import Robot
from bout import Bout


class RobController(object):
    def build_robot(self, bout=None):
        robot = Robot()
        robot.name = type(self).__name__
        print("Building " + robot.name)
        self.load_modules(robot, bout)
        return robot

    def load_modules(self, robot, bout):
        print("Modules:")
        for mname, m in self.modules.items():
            m_instance = m()
            print('\t'+m_instance.name)
            if hasattr(m_instance, "source"):
                m_instance.source = robot
            if hasattr(m_instance, "projectile_cb"):
                m_instance.projectile_cb = bout.projectile_spawn_cb
            if hasattr(m_instance, "scanner_cb"):
                m_instance.scanner_cb = bout.scanner_cb
            for k, v in m_instance.__dict__.items():
                #print(k, v)
                pass
            setattr(robot, mname, m_instance)
            setattr(self, mname, m_instance.gen_interface())
        


class MasterMind(RobController):
    def __init__(self):
        super(MasterMind, self).__init__()
        self.modules = {}
        self.modules['scanner']=ArcScanner
        self.modules['cannon1']=ATCannon
        self.modules['cannon2']=ATCannon
        self.modules['shield']=EnergyShield
        #self.load_modules(self.modules)

        #self.cannon1.fire(4)
        #self.shield.modulate(1)
        #print(self.shield.get_color())

    def run(self):
        self.scanner.scan(2)
        self.cannon1.fire(2)
        self.cannon2.fire(3)


if __name__ == '__main__':
    b = Bout('a')
    m=MasterMind()
    m.build_robot(b)
    m.run()
