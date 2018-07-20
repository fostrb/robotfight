#from robot_builder.rbuilder import RobotBuilder
from rob_components import *
from nbot import Robot
import time


class RobController(object):
    def build_robot(self, bout=None):
        robot = Robot()
        robot.name = type(self).__name__
        print("Building " + robot.name)
        self.load_modules(robot, bout)

        setattr(self, 'get_position', robot.get_position)
        setattr(self, 'get_heading', robot.get_heading)
        setattr(self, 'get_hull', robot.get_hull)
        setattr(self, 'get_velocity', robot.get_velocity)

        robot.execute = self.run
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
            if hasattr(m_instance, "laser_cb"):
                m_instance.laser_cb = bout.laser_cb
            setattr(robot, mname, m_instance)
            setattr(self, mname, m_instance.gen_interface())
            robot.modules.append(m_instance)

