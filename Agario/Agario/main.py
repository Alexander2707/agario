nickname = input('Введіть нікнейм: ')

import pygame
import random

pygame.init()

w, h = 1000, 600

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

    def draw_2(self):
        pygame.draw.circle(window, self.color, (self.rect.x+self.radius, self.rect.y+self.radius), self.radius)
        font1 = pygame.font.Font("minecraft_0.ttf", 18)
        text = font1.render(nickname, True, (0, 0, 0))
        window.blit(text, (460, 280))


def load_level_map ():
    global enemies
    enemies = list() 
    for _ in range(1000):
        food = Ball(random.randint(-1000, 1000), 
                    random.randint(-1000, 1000), (random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)), 
                    random.randint(5, 15))
        enemies.append(food)
    return enemies

window = pygame.display.set_mode((w, h))

ball = Ball(450, 250, (255, 0, 0), 40)
lvl = load_level_map()

clock = pygame.time.Clock()
run = True
while run:
    window.fill((255, 255, 255))
    for food in lvl:
        food.draw_1()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for food in enemies:
            food.rect.x += 5
    if keys[pygame.K_RIGHT]:
        for food in enemies:
            food.rect.x -= 5
    if keys[pygame.K_UP]:
        for food in enemies:
            food.rect.y += 5
    if keys[pygame.K_DOWN]:
        for food in enemies:
            food.rect.y -= 5
    ball.draw_2()

    pygame.display.update()
    clock.tick(60)