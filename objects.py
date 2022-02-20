import pygame
import random
import math
from circle import Player, Food


class Players:
    def __init__(self, num, size):
        self.size = size
        self.radius = 50
        self.list = []
        for i in range(num):
            x, y = self.spawn()
            self.list.append(Player((x, y, self.size),i , self.radius))

    def spawn(self):
        while True:
            x = random.randint(self.radius + 1, self.size[0] - self.radius - 1)
            y = random.randint(self.radius + 1, self.size[1] - self.radius - 1
                               )
            if not any((e.x, e.y) for e in self.list if euclidean_distance(x, y, e.x, e.y) < self.radius + e.radius):
                return x, y
                break

    def draw(self, win):
        for e in self.list:
            if e is not None:
                e.draw(win)

    def eat(self, numP, foods):
        player = self.get_player(numP)
        self.eatF(player, foods)
        self.eatP(player)

    def eatF(self, player, foods):
        for i, f in enumerate(foods):
            if player.x - player.radius < f.x - f.radius and player.y - player.radius < f.y - f.radius \
                    and player.x + player.radius > f.x + f.radius and player.y + player.radius > f.y + f.radius:
                if player.radius > f.radius:
                    player.radius += f.radius // 5
                    foods.list.pop(i)
                    break

    def eatP(self, player):
        for i, p in enumerate(self):
            if not player == p and p is not None:
                if player.x - player.radius < p.x - p.radius and player.y - player.radius < p.y - p.radius \
                        and player.x + player.radius > p.x + p.radius and player.y + player.radius > p.y + p.radius:
                    if player.radius - 5 > p.radius and p.start:
                        player.radius += p.radius // 5
                        #self.refresh(self.get_number(p), None)
                        self.list.pop(i)
                        break

    def refresh(self, num, obj):
        self.list[num] = obj

    def get_number(self, obj):
        for i, e in enumerate(self):
            if e.name == obj.name:
                return i

    def get_player(self, num):
        self.list[num].start = True
        return self.list[num]

    def to_send(self, num):
        l = self.list.copy()
        l.pop(num)
        return l

    def __iter__(self):
        for e in self.list:
            yield e


class Foods:
    def __init__(self, num: int, size):
        self.size = size
        self.radius = 5
        self.list = []
        for i in range(num):
            x, y = self.spawn()
            self.list.append(Food(x, y, self.radius))

    def spawn(self):
        # while (x, y) in [(e.x, e.y) for e in self.liste]: # enhance with collide_circle
        while True:
            x = random.randint(self.radius, self.size[0] - self.radius)
            y = random.randint(self.radius, self.size[1] - self.radius)
            if not any((e.x, e.y) for e in self.list if euclidean_distance(x, y, e.x, e.y) < self.radius * 2):
                return x, y
                break

    def draw(self, win):
        for e in self.list:
            e.draw(win)

    def create(self, num):
        for i in range(num):
            x, y = self.spawn()
            self.list.append(Food(x, y, self.radius))

    def __iter__(self):
        for e in self.list:
            yield e


def euclidean_distance(x1, y1, x2, y2):
    return math.hypot((int(x1) - int(x2)), (int(y1) - int(y2)))
