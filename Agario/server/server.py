import pygame
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM

server = socket(AF_INET, SOCK_STREAM)
server.bind(("localhost", 2707))

server.listen(5)
server.setblocking(False)
print("Сервер працює")

players = {}
id = 0

def receive_msg():
    while True:
        # print(1)
        for conn in list(players):
            try:
                msg = conn.recv(1024).decode()
                msg = msg.split(",")
                player_id = int(msg[0])
                player_x = int(msg[1])
                player_y = int(msg[2])
                player_radius = int(msg[3])
            except:
                pass
            packet = ''
            try:
                for c, p in players.items():
                    if c!=conn:
                        line = f"{p['id']},{p['x']},{p['y']},{p['radius']}"
                        packet += line + "|"
                conn.send(packet.encode())
            except:
                pass

Thread(target=receive_msg).start()

while True:
    try:
        connect, ip = server.accept()
        connect.setblocking(False)
        print(f"Підключився клієнт: {ip}")
        id += 1
        players[connect] = {
            "id": id,
            "x": 0,
            "y": 0,
            "radius": 30,
            "name": None
        }
        connect.send(f"{id},0,0,30".encode())
    except:
        pass