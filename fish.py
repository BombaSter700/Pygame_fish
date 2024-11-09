import pygame
import random

pygame.init()

# Параметры окна
s_width = 1000  # ширина игрового окна
s_high = 600  # высота игрового окна

screen = pygame.display.set_mode((s_width, s_high))
pygame.display.set_caption("Аквариум")

# Начало игры
player_pic = pygame.image.load("Fish05_A.png")  # картинка игрока
player_x = 15  # начальная координата x
player_y = 30  # начальная координата y
player_size = 30  # начальный размер игрока
player_left = False  # направление движения игрока

enemy_n = 10  # количество врагов
enemy_pic = pygame.image.load("Fish04_A.png")  # картинка врагов
enemy_pic2 = pygame.image.load("Fish04_B.png")  # альтернативная картинка врагов

# Массивы врагов
enemy_x = [0] * enemy_n
enemy_y = [0] * enemy_n
enemy_size = [50] * enemy_n
enemy_speed = [2] * enemy_n
enemy_main = [True] * enemy_n
enemy_tick = [0] * enemy_n

# Инициализация врагов
for i in range(enemy_n):
    enemy_x[i] = random.randint(0, s_width)
    enemy_y[i] = random.randint(0, s_high)
    enemy_tick[i] = random.randint(0, 10)

# Фон
background_pic = pygame.image.load("Scene_A.png")
background_pic2 = pygame.image.load("Scene_B.png")
b_main = True  # переключатель фона
b_tick = 50  # счетчик тиков для смены фона

clock = pygame.time.Clock()
running = True

# Основной цикл игры
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Управление движением игрока
    if keys[pygame.K_UP]:
        player_y -= 4
    if keys[pygame.K_DOWN]:
        player_y += 4 
    if keys[pygame.K_RIGHT]:
        player_x += 4
        player_left = False
    if keys[pygame.K_LEFT]:
        player_x -= 4
        player_left = True
    if keys[pygame.K_SPACE]:
        player_size += 1

    # Смена фона
    b_tick -= 1
    if b_tick == 0:
        b_tick = 50
        b_main = not b_main

    # Отрисовка фона
    if b_main:
        screen.blit(background_pic, (0, 0))
    else:
        screen.blit(background_pic2, (0, 0))

    # Вывод игрока
    player_pic_small = pygame.transform.scale(player_pic, (int(player_size * 1.25), player_size))
    if player_left:
        player_pic_small = pygame.transform.flip(player_pic_small, True, False)
    screen.blit(player_pic_small, (player_x, player_y))

    # Вывод врагов
    for i in range(enemy_n):
        # Обновление счетчика тиков врагов
        enemy_tick[i] -= 1
        if enemy_tick[i] == 0:
            enemy_tick[i] = 10
            enemy_main[i] = not enemy_main[i]

        # Выбор картинки врага
        if enemy_main[i]:
            enemy_pic_small = pygame.transform.scale(enemy_pic, (int(enemy_size[i] * 1.25), enemy_size[i]))
        else:
            enemy_pic_small = pygame.transform.scale(enemy_pic2, (int(enemy_size[i] * 1.25), enemy_size[i]))

        # Разворот врага
        if enemy_speed[i] < 0:
            enemy_pic_small = pygame.transform.flip(enemy_pic_small, True, False)

        # Движение врага
        enemy_x[i] += enemy_speed[i]
        if enemy_x[i] > s_width or enemy_x[i] < 0:
            enemy_speed[i] = -enemy_speed[i]

        # Отрисовка врага
        screen.blit(enemy_pic_small, (enemy_x[i], enemy_y[i]))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
