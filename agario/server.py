import socket
from _thread import *
import pickle
import time
from objects import Players, Foods
import pygame
import os

server = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

nb_player = 5
s.listen(nb_player)
print("Waiting for a connection, Serveur Started")

size = (10_000, 10_000)

objects = {'foods': Foods(1000, size), 'players': Players(nb_player, size)}


def threaded_client(conn, player):
    conn.send(pickle.dumps(objects['players'].get_player(player)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                objects['players'].refresh(player, data)
                objects['players'].eat(player, objects['foods'])

                player = objects['players'].get_number(data)

                response = objects.copy()
                response['players'].to_send(player)
                reply = (response, objects['players'].get_player(player))

            print('Received: ', data)
            print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))


        except Exception as e:
            print(e)
            break
    print("Lost connection")
    conn.close()


def threaded_foods():
    while True:
        try:
            objects['foods'].create(100)
            time.sleep(3)


        except Exception as e:
            print(e)
            break
    print("Lost connection")
    conn.close()


def drawWindow(win, objects):
    win.fill('black')
    for obj in objects.values():
        obj.draw(win)


def saving_map():
    pygame.init()
    surface = pygame.Surface((10_000, 10_000))
    src = "D:\python\site_django\src\mon_jeu\static\media\map.jpeg"
    while True:
        drawWindow(surface, objects)
        pygame.image.save(surface, src)
        time.sleep(0.5)
        os.remove(src)



currentPlayer = 0
#start_new_thread(saving_map, ())
while True:
    conn, addr = s.accept()
    print("Connected to :", addr)

    if currentPlayer > 2:
        start_new_thread(threaded_foods, ())
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
