import pygame
import random
import sys
import os

game_pictures = os.path.join(os.path.dirname(__file__), "images")

def overlap(x,y,w,h,vx,vy,vw,vh):
    x2=x+w
    y2=y+h
    vx2=vx+vw 
    vy2=vy+vh
    r = (vx<=x<=vx2 or x<=vx<=x2) and (vy<=y<=vy2 or y<=vy<=y2)
    return r
def space_wait():
    wait=True
    while wait:
        for event in pygame.event.get(): # проверяем все системные события игры 
            if event.type == pygame.QUIT:  # если окно закрылось, то...
                wait = False # сбрасываем флажок в значение ЛОЖЬ для выхода из цикла
                pygame.quit()   # останавливаем игровой движок
                sys.exit()  # закрываем окно с экраном игры
        keys = pygame.key.get_pressed() # запрашиваем состояние клавиатуры
        if keys[pygame.K_SPACE]: # если в keys зафиксировано нажатие стрелки вправо
            wait = False # брасываем переменную-флажок в значение ЛОЖЬ для выхода


pygame.init() #инизиализация игры

# Параметры окна
s_width = 1000  # ширина игрового окна
s_high = 600  # высота игрового окна

screen = pygame.display.set_mode((s_width, s_high))
pygame.display.set_caption("Аквариум")

#функция обьявления всех значений
def game_begin():
    global player_pic
    player_pic =pygame.image.load(os.path.join(game_pictures,'Fish01_A.png'))
    global player_x
    player_x = 15 
    global player_y
    player_y = 30 
    global player_size
    player_size=30     
    global player_left
    player_left=False 
    for i in range(enemy_n):
        enemy_x[i]=random.randint(0,s_width) # задаем случайную координату x для врага
        enemy_y[i]=random.randint(0,s_high)  # задаем случайную координату y для врага
        enemy_tick[i]=random.randint(0,10)   # задаем случайное начальное значение тиков 
        enemy_speed[i]=random.randint(-3,3)  # задаем случайную скорость врага
        enemy_size[i]=random.randint(15,60)  # задачем случайный размер врага

restart_pic = pygame.image.load(os.path.join(game_pictures,"BtnRestart.png")) # подгружаем картинку перезапуска
start_pic = pygame.image.load(os.path.join(game_pictures,"BtnPlay.png")) # подгружаем картинку начала


enemy_n = 20  # количество врагов
enemy_pic = pygame.image.load(os.path.join(game_pictures,"Fish04_A.png"))  # картинка врагов
enemy_pic2 = pygame.image.load(os.path.join(game_pictures,"Fish04_B.png"))  # альтернативная картинка врагов

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
    enemy_speed[i]=random.randint(-3,3)  # задачем случайную скорость врагов
    enemy_size[i]=random.randint(15,60)  # задачем случайный размер врагов

# Фон
background_pic = pygame.image.load(os.path.join(game_pictures,"Scene_A.png"))
background_pic2 = pygame.image.load(os.path.join(game_pictures,"Scene_B.png"))
b_main = True  # переключатель фона
b_tick = 50  # счетчик тиков для смены фона

clock = pygame.time.Clock()
running = True

#инициализция переменные пузырей
bubble_n = 10 # задаем количество пузырей
bubble_pic = pygame.image.load(os.path.join(game_pictures,"Bubble.png"))
bubble_x=[0]*bubble_n
bubble_y=[0]*bubble_n
bubble_size=[0]*bubble_n
#заполняем координаты пузырей и размеры случайными числами
for i in range(bubble_n):
    bubble_x[i]= random.randint(0, s_width)
    bubble_y[i]= random.randint(s_high, s_high*2)
    bubble_size[i]= random.randint(10,32)

screen.blit(background_pic,(0,0))   # выводим аквариум
screen.blit(start_pic,(420,250))    # выводим картинку play
pygame.display.flip()               # обновляем экран
space_wait()                        # ждем пробел
life=3                              # задаем количество жизней
game_begin()                        # инициализируем игрока и врагов


'''******************** ОСНОВНОЙ ЦИКЛ ИГРЫ **********************'''
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Огранические на передвижение только в рамках экрана
    if player_x <= 0: player_x = 0 # self.x, self.y - Координаты чекпоинта перса
    if player_y <= 0: player_y = 0 # В первых 2 условиях говориться, что перс не может выходить за пределы экрана.  
    if player_x >= s_width - 60: player_x =  - 60 # SCREEN_WIDTH и SCREEN_HEIGHT это константы с размерами окна.
    if player_y >= s_high - 64:player_y = s_high - 64 # self.x = SCREEN_WIDTH, self.y = SCREEN_HEIGHT

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
        # проверяем нет ли столкновениия рыбки врага с рыбкой героем
        if overlap(player_x, player_y, int(player_size * 1.25), player_size, enemy_x[i], enemy_y[i], 
                   int(enemy_size[i]*1.25), enemy_size[i]):
            if player_size>enemy_size[i]:
                player_size += 2   # увеличиваем размер героя
                enemy_x[i] = -200  # прячем врага за левую границу экрана
                enemy_speed[i]=2   # задаем положительную скорость движения
                
            else:
                enemy_size[i] +=10 # увеличиваем размер врага
                player_x = 15      # задаем начальную х-координату героя
                player_y = 30      # задаем начальную y-координату героя
                player_size=30     # задаем начальный размер героя
                player_left=False  # указываем, что герой смотрит направо


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
