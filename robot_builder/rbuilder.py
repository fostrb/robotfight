from rob_components import *


class RobotBuilder(object):
    def __init__(self, modules={}):
        self.modules = modules
        for mname, module in self.modules.items():
            print(mname, module)


if __name__ == '__main__':
    RobotBuilder()
