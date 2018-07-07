import pygame
from robot import Robot
from entity import Polygon

pygame.init()
pygame.font.init()

# TODO: Metric to pixel scaling. Conversion should happen during initialization, not constantly during runtime.
# TODO: dump pygame for something more fun to work with.


class MainDisplay(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([self.width, self.height], 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("robots")
        self.robots = []

        self.load_bots()
        self.bout_loop()

    def bout_loop(self):
        while True:
            self.screen.fill([0, 0, 0])
            self.update_bots()
            self.draw_bots()
            #self.draw_data()
            pygame.display.update()
            self.clock.tick(30)

    def load_bots(self):
        points = [[0,0], [0,10], [10,5]]
        pos = [0,0]
        pos2 = [100, 140]
        p = Polygon(points)
        p1 = Polygon(points)
        self.robots.append(Robot(name="r1", polygon=p, position=pos))
        self.robots.append(Robot(name="r2", polygon=p1, position=pos2))

        for bot in self.robots:
            #print(bot.body.points)
            #bot.initialize(self.width, self.height)
            pass

    def update_bots(self):
        for bot in self.robots:
            bot.update()
            print(bot.position, bot.body.points)
        self.collision_test()
        
    def collision_test(self):
        for bot in self.robots:
            for other in self.robots:
                if other is not bot:
                    if other.intersects(bot):
                        # when objects collide forces are exerted on them
                        # compute the difference of velocity*mass vectors
                        #   angle of force is opposite the angle of impact for each object
                        pass

    def draw_bots(self):
        for bot in self.robots:
            pygame.draw.polygon(self.screen, [0,255,0], bot.get_points(), 1)
            #bot.translate([1,1])
            #bot.thrust()
            #bot.rotate(random.randint(-1, 1))
            bot.rotate(5)


    def draw_data(self):
        for bot in self.robots:
            pygame.draw.circle(self.screen, [0, 255, 0], [int(bot.position[0]), int(bot.position[1])], int(bot.body.radius), 1)
            myfont = pygame.font.SysFont(None, 20)
            textsurface = myfont.render(bot.name, True, [0, 255, 0])
            pos = [bot.position[0]-20, bot.position[1] - bot.body.radius-15]
            self.screen.blit(textsurface, pos)
            textsurface = myfont.render(str(str(int(bot.position[0])) + ' : ' + str(int(bot.position[1]))), True, [0, 255, 0])
            pos = [bot.position[0]-20, bot.position[1] - bot.body.radius+40]
            self.screen.blit(textsurface, pos)




if __name__ == '__main__':
    import random
    MainDisplay(720, 480)
