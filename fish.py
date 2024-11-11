import pygame
import random
import sys
import os
from assets import load_images

pygame.init() #инизиализация игры

# Параметры окна
s_width = 1000  # ширина игрового окна
s_high = 600  # высота игрового окна

screen = pygame.display.set_mode((s_width, s_high))
pygame.display.set_caption("Аквариум")

game_pictures = os.path.join(os.path.dirname(__file__), "images")
images = load_images(game_pictures)

#функция обьявления всех значений и загрузки картинок 
def game_begin():
    global player_pic, player_x, player_y, player_size, player_left, fish_count
    global restart_pic, start_pic, count_pic, enemy_pic, enemy_pic2
    global background_pic, background_pic2, bubble_pic

    # Инициализация игровых данных
    player_x, player_y = 15, 30
    player_size = 30
    player_left = False
    fish_count = 0

    # Подгруз всех картинок для игры
    player_pic = images["player"]
    restart_pic = images["restart"]
    start_pic = images["start"]
    count_pic = pygame.transform.scale(images["count"], (40, 40))
    enemy_pic = images["enemy"]
    enemy_pic2 = images["enemy_alt"]
    background_pic = images["background"]
    background_pic2 = images["background_alt"]
    bubble_pic = images["bubble"]

    for i in range(enemy_n):
        enemy_x[i] = random.randint(0, s_width)
        enemy_y[i] = random.randint(0, s_high)
        enemy_tick[i] = random.randint(0, 10)
        enemy_speed[i] = random.randint(-3, 3)
        enemy_size[i] = random.randint(15, 60)

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


# Массивы врагов
enemy_n = 20  # количество врагов
enemy_x = [0] * enemy_n
enemy_y = [0] * enemy_n
enemy_size = [50] * enemy_n
enemy_speed = [2] * enemy_n
enemy_main = [True] * enemy_n
enemy_tick = [0] * enemy_n

# Фон
b_main = True  # переключатель фона
b_tick = 50  # счетчик тиков для смены фона

clock = pygame.time.Clock()
running = True

#инициализция переменные пузырей
bubble_n = 10 # задаем количество пузырей
bubble_x=[0]*bubble_n
bubble_y=[0]*bubble_n
bubble_size=[0]*bubble_n
#заполняем координаты пузырей и размеры случайными числами
for i in range(bubble_n):
    bubble_x[i]= random.randint(0, s_width)
    bubble_y[i]= random.randint(s_high, s_high*2)
    bubble_size[i]= random.randint(10,32)

game_begin() # инициализируем игрока и врагов
pygame.font.init()  # инициализация шрифтов
myfont = pygame.font.SysFont('Comic Sans MS', 30) # настройка шрифта
screen.blit(background_pic,(0,0))   # выводим аквариум
screen.blit(start_pic,(420,250))    # выводим картинку play
pygame.display.flip()               # обновляем экран
space_wait()                        # ждем пробел
life=3                              # задаем количество жизней



'''******************** ОСНОВНОЙ ЦИКЛ ИГРЫ **********************'''
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Огранические на передвижение только в рамках экрана
    if player_x < 0:player_x = 0
    if player_y < 0:player_y = 0
    if player_x > s_width - int(player_size * 1.25):  # Учитываем размер игрока для правой границы
        player_x = s_width - int(player_size * 1.25)
    if player_y > s_high - player_size:  # Учитываем высоту игрока для нижней границы
        player_y = s_high - player_size

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
    textsurface = myfont.render(str(life), False, (0, 0, 0)) # формируем картинку с цифрой жизней
    screen.blit(textsurface,(player_x-15,player_y)) # выводим картинку с цифрой жизней


    # Вывод врагов
    for i in range(enemy_n): 
        # проверяем нет ли столкновениия рыбки врага с рыбкой героем
        if overlap(player_x, player_y, int(player_size * 1.25), player_size, enemy_x[i], enemy_y[i], 
                   int(enemy_size[i]*1.25), enemy_size[i]):
            if player_size>enemy_size[i]:
                player_size += 2   # увеличиваем размер героя
                enemy_x[i] = -200  # прячем врага за левую границу экрана
                enemy_speed[i]=2   # задаем положительную скорость движения
                fish_count += 1
                
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

    screen.blit(count_pic,(s_width-60,10)) # выводим картинку съеденной рыбки
    textsurface = myfont.render(str(fish_count), False, (0, 0, 0)) # формируем картинку с цифрой жизней
    screen.blit(textsurface,(s_width-80,10)) # выводим картинку с цифрой жизней


    # Обновление экрана
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
