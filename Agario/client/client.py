import pygame # імпортуємо бібліотеку pygame
import random # імпортуємо модулб рандом
from socket import* # імпортуємо socket
from threading import Thread # імпортуємо необхідну функцію із модуля Threading 

# створюємо клієнта
client = socket(AF_INET, SOCK_STREAM)
client.connect(("localhost", 2707)) # з'єднуємо клієнта з  хостом та портом

# отримаємо дані про себе від клієнта
msg = client.recv(1024).decode()
msg = msg.split(",")
my_id = int(msg[0])
my_x = int(msg[1])
my_y = int(msg[2])
my_radius = int(msg[3])
print(my_id, my_x, my_y, my_radius)

# активуємо pygame
pygame.init()

w, h = 1000, 600 # ширина та висота єкрана
username = " "

# створюємо клас Ball
class Ball():
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed_x = 4
        self.speed_y = 4
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        
    def draw_1(self):
        pygame.draw.circle(window, self.color, (self.rect.x+self.radius, self.rect.y+self.radius), self.radius)

    # def draw_2(self):
    #     pygame.draw.circle(window, self.color, (self.rect.x+self.radius, self.rect.y+self.radius), self.radius)
    #     font1 = pygame.font.Font("minecraft_0.ttf", 18)
    #     text = font1.render(nickname, True, (0, 0, 0))
    #     window.blit(text, (460, 280))

run2 = True
foods = list()
for _ in range(1000):
    food = Ball(random.randint(-1000, 1000), 
                random.randint(-1000, 1000), (random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)), 
                random.randint(5, 15))
    foods.append(food)
enemies = [] # список інших гравців
# прийом повдомлень від сервера
def receive_msg():
    global enemies, run2 # робимо список глобальним

    while run2:
        try:
            msg = client.recv(1024).decode()
            a = msg.strip("|").split("|")
            enemies = []
            for enemy in a:
                data_enemy_txt = enemy.split(',')
                enemy_id = int(data_enemy_txt[0])
                enemy_x = int(data_enemy_txt[1])
                enemy_y = int(data_enemy_txt[2])
                enemy_radius = int(data_enemy_txt[3])
                enemies.append([enemy_id, enemy_x, enemy_y, enemy_radius])
        except:
            pass
# створюємо поток
Thread(target=receive_msg).start()

# створюємо ігрове вікно
window = pygame.display.set_mode((w, h))
ball = Ball(w // 2, h // 2, (255, 0, 0), my_radius) # наш гравець

clock = pygame.time.Clock()
run = True
# ігровий цикл
while run:
    window.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    for f in foods:
        if ball.rect.colliderect(f):
            foods.remove(f)
            ball.radius += 1
        else:
            f.draw_1()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
            run2 = False
            pygame.quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                username = username[0 : -1]
            else: 
                username += e.unicode

    if keys[pygame.K_LEFT]:
        for food in foods:
            food.rect.x += 5
        my_x -= 5
    if keys[pygame.K_RIGHT]:
        for food in foods:
            food.rect.x -= 5
        my_x += 5
    if keys[pygame.K_UP]:
        for food in foods:
            food.rect.y += 5
        my_y -= 5
    if keys[pygame.K_DOWN]:
        for food in foods:
            food.rect.y -= 5
        my_y += 5
    ball.draw_1()

    try:
        msg_for_server = f"{my_id}, {my_x}, {my_y}, {ball.radius}"
        client.send(msg_for_server.encode())
    except:
        pass
    
    font1 = pygame.font.Font("minecraft_0.ttf", 16)
    user_text = font1.render(username, True, (255,255,255))
    window.blit(user_text, ((w / 2) - 40, (h / 2)-20 ))

    for element in enemies:
        sx = int((element[1] - my_x) + w // 2)
        sy = int((element[2] - my_y) + h // 2)
        enemy1 = Ball(sx, sy, (0, 0, 0), element[3])
        if ball.rect.colliderect(enemy1):
            if ball.radius < enemy1.radius:
                enemy1.draw_1()
                run = False
                run2 = False
                pygame.quit()
        else:
            enemy1.draw_1()

    pygame.display.update()
    clock.tick(60)