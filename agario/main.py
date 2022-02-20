import pickle
import pygame
import time
from objects import Player
from network import Network
from _thread import *

width = 1080
height = 720

pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def sub(win, surface, player):
    x = player.x - win.get_width() // 2
    y = player.y - win.get_height() // 2

    if player.x - win.get_width() // 2 < 0:
        x = 0
    if player.x + win.get_width() // 2 > surface.get_width():
        x = surface.get_width() - win.get_width()
    if player.y - win.get_height() // 2 < 0:
        y = 0
    if player.y + win.get_height() // 2 > surface.get_height():
        y = surface.get_height() - win.get_height()

    rect = pygame.Rect(x, y, win.get_width(), win.get_height())
    s = surface.subsurface(rect)
    return s


def redrawWindow(win, objects, player):
    surface = pygame.Surface((10_000, 10_000))
    win.fill('black')
    for obj in objects.values():
            obj.draw(surface)

    player.draw(surface)

    win.blit(sub(win, surface, player), (0, 0))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network('192.168.1.83')
    player = n.getP()

    while run:
        clock.tick(60)

        objects, player = n.send(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or player is None:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.bool_up = True
                if event.key == pygame.K_DOWN:
                    player.bool_down = True
                if event.key == pygame.K_LEFT:
                    player.bool_left = True
                if event.key == pygame.K_RIGHT:
                    player.bool_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.bool_up = False
                if event.key == pygame.K_DOWN:
                    player.bool_down = False
                if event.key == pygame.K_LEFT:
                    player.bool_left = False
                if event.key == pygame.K_RIGHT:
                    player.bool_right = False

        redrawWindow(win, objects, player)
    pygame.display.quit()


main()
