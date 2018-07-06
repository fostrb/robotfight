#
#
#


class Bout(object):
    def __init__(self, robs):
        self.robs = robs
        print(self.robs)


if __name__ == '__main__':
    robs = ['rob1', 'rob2']
    Bout(robs)
