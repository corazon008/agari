import pygame
import pygame.freetype
import random
import math


class Player:
    def __init__(self, coor, name, radius = 100):
        self.name = name
        x, y, size = coor
        self.x = x
        self.y = y
        self.size = size
        self.speed = 20
        self.radius = radius
        self.color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
        self.bool_up = False
        self.bool_down = False
        self.bool_left = False
        self.bool_right = False
        self.start = False

    def eat(self, other):
        if self.x - self.radius < other.x - other.radius and self.y - self.radius < self.y - other.radius and other.start and self.start:
            if self.radius > other.radius:
                self.radius += other.radius
                return True
        return False

    def draw(self, win):
        self.move()
        myfont = pygame.freetype.SysFont('Comic Sans MS', 30)
        text, rect = myfont.render(f'{self.radius}', 'white')
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        win.blit(text, (self.x - rect[1]//2, self.y - rect[1]//2))

    def move(self):
        if self.bool_up and self.y - self.speed > 0:
            self.y -= self.speed
        if self.bool_down and self.y + self.speed < self.size[1]:
            self.y += self.speed
        if self.bool_left and self.x - self.speed > 0:
            self.x -= self.speed
        if self.bool_right and self.x + self.speed < self.size[0]:
            self.x += self.speed

    def get_coor(self):
        return int(self.x), int(self.y)


class Food:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
