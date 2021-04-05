import pygame
import numpy as np


class Pellet(pygame.sprite.Sprite):
    def __init__(self, coords, radius=5):
        self.coords = coords
        self.colour = (20, 200, 20)
        self.rect = pygame.Rect(*((0, 0) + (2 * radius, 2 * radius)))
        self.rect.centerx = int(coords[0])
        self.rect.centery = int(coords[1])
        self.eaten = False

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.colour, self.rect)

    def update(self, screen, objects):
        objects = [o for o in objects if o != self]
        rects = [o.rect for o in objects if o != self]
        idx = self.rect.collidelist(rects)
        if idx >= 0:
            collider = objects[idx]
            collider.interact(self)
        self.draw(screen)