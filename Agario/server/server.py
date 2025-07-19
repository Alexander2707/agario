import pygame # імпортуємо бібліотеку pygame
from threading import Thread # імпортуємо необхідну функцію із модуля Threading
from socket import socket, AF_INET, SOCK_STREAM # імпортуємо необхідні функції із модуля socket

# створюємо сервер
server = socket(AF_INET, SOCK_STREAM)
server.bind(("localhost", 2707)) # прив'язуємо сервер до хосту

server.listen(5) # сервер одночасно може приймати 5 гравців
server.setblocking(False) # вимикаємо блокування
print("Сервер працює") # перевіряємо чи працює сервер

players = {} # словник для данних про гравців
id = 0 # айди гравця

# Функція для отримання повідомлень від клієнтів
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

Thread(target=receive_msg).start() # створюємо поток


# ігровий цикл
while True:
    try:
        connect, ip = server.accept() # приймаємо до себе клієнта
        connect.setblocking(False) # знімаємо блокування
        print(f"Підключився клієнт: {ip}")
        id += 1 # айді слідуючаго гравця
        players[connect] = {
            "id": id,
            "x": 0,
            "y": 0,
            "radius": 30,
            "name": None
        } # оновлюємо словник додаючи в нього словник з даними при гравця
        connect.send(f"{id},0,0,30".encode()) # відправляємо данні клієнту
    except:
        pass