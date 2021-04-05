import pygame
import random
from pygame.locals import *
from creatures.creature import Creature
from creatures.pellet import Pellet

SCREENRECT = Rect(0, 0, 640, 640)

pygame.init()
winstyle = 0
bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pygame.display.set_mode((640, 640), winstyle, bestdepth)
clock = pygame.time.Clock()


def main():
    boy = Creature([100, 100])
    pellet = Pellet([200, 200])
    objects = [boy, pellet]
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill((250, 250, 250))
        objects = [thing for thing in objects if not thing.eaten]
        if random.randint(0, 100) >= 99:
            objects.append(
                Pellet(
                    [
                        random.randint(5, screen.get_width() - 5),
                        random.randint(5, screen.get_height() - 5),
                    ]
                )
            )
        for thing in objects:
            thing.update(screen, objects)
        pygame.display.flip()
        clock.tick_busy_loop(40)


if __name__ == "__main__":
    main(screen)