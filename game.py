import pygame as pg
from random import randrange
from time import sleep

# инициализируем модуль pygame
pg.init()

# определяем размер экрана в константах
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 600
CELL_SIZE = 40

# задаем цвета кортежами RGB
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# инициализируем шрифт из pygame
FONT = pg.font.SysFont(name=None, size=32)

# создаем и инициализируем дисплей
display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

#задаем заголовок
pg.display.set_caption("Snake Game")

# чтобы окошко не закрывалось. Делается с помощью флага (Игра сейчас заказчивается? Нет.)На его основе пишется цикл while. 
game_exit = False

# images
background = pg.image.load("bg.jpg")
body = pg.image.load("body.png")
head = pg.image.load("head.png")
apple = pg.image.load("apple.png")
wall = pg.image.load("wall.png")

# snake position. задаем координаты головы змейки. Мы хотим, чтобы змейка начинала с середины экрана. Pygame хранит координат относительно верхнего левого угла
head_x = (DISPLAY_WIDTH - CELL_SIZE) / 2
head_y = (DISPLAY_HEIGHT - CELL_SIZE) / 2

# изменения направления движения змейки
head_x_change = 0
head_y_change = 0

# game variable. сколько яблок съела змейка, длина змейки
score = 0
snake_lenth = 1
snake_list = []

def check_events():
    global game_exit
    global head_x_change
    global head_y_change

    for event in pg.event.get():
        if event.type == pg.QUIT: # событие "выход"
            game_exit = True
        if event.type == pg.KEYDOWN: # событие "нажатие клавиши"
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                head_x_change = -1 * CELL_SIZE
                head_y_change = 0
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                head_x_change = CELL_SIZE
                head_y_change = 0
            elif event.key == pg.K_UP or event.key == pg.K_w:
                head_x_change = 0
                head_y_change = -1 * CELL_SIZE
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                head_x_change = 0
                head_y_change = CELL_SIZE

def snake_movement() -> tuple:
    """
    Вычисляет смещение головы и добавляет элемент в список
    Calculate head offset and append object to snake_list.
    \n Return head position tuple
    """
    global head_x
    global head_y

    head_x += head_x_change
    head_y += head_y_change
    head_pos = (int(head_x), int(head_y))
    snake_list.append(head_pos)
    if len(snake_list) > snake_lenth:
        del snake_list[0]
    return head_pos

def check_collide():
    global apple_x
    global apple_y
    global score
    global snake_lenth
    global wall_x
    global wall_y

    # snake collide apple. столкновение с яблоком - змейка подбирает яблоко
    if apple_x == head_x and apple_y == head_y:
        apple_x = randomze_apple_pos(DISPLAY_WIDTH)
        apple_y = randomze_apple_pos(DISPLAY_HEIGHT)
        wall_x = randomize_wall_pos(DISPLAY_WIDTH)
        wall_y = randomize_wall_pos(DISPLAY_HEIGHT)
        score += 1
        snake_lenth += 1

    # collide self столкновение змейки с собой (из snake_list берем всё, кроме последнего элемента)
    for item in snake_list[:-1]:
        if item == head_pos:
            show_game_over()

    # collide border столкновение змейки с границей
    if head_x > DISPLAY_WIDTH or head_x < 0 or head_y < 0 or head_y > DISPLAY_HEIGHT:
        show_game_over()

    # столкновение змейки со стеной
    if wall_x == head_x and wall_y == head_y:
        show_game_over()


def redraw_screen():
    # рисуем фон
    display.blit(background, [0, 0])

    # рисуем яблоко
    display.blit(apple, [apple_x, apple_y])

    # рисуем стену
    display.blit(wall, [wall_x, wall_y])

    # рисуем змейку
    draw_snake()
    draw_text_to_screen(text=f"Score: {score}", color=RED, x=0, y=0)

# метод только для квадратного поля, используется для клеточных игр
def randomze_apple_pos(size:int) -> int:
    """
    Generate apple pos on size axis
    """

    return randrange(0, size-CELL_SIZE) // CELL_SIZE * CELL_SIZE


def randomize_wall_pos(size:int) -> int:
    """
    Generate wall pos on size axis
    """

    return randrange(0, size-CELL_SIZE) // CELL_SIZE * CELL_SIZE

# метод отрисовки змейки
def draw_snake() -> None:  
    for item in snake_list:
        display.blit(body, [item[0], item[1]])
    head_obj = snake_list[-1]
    display.blit(head, [head_obj[0], head_obj[1]])

# рисование текста на экране
def draw_text_to_screen(text:str, color:tuple, x:int=0, y:int=0, center:bool=False) -> None:
    """
    Draw text to display
    """
    score_text = FONT.render(text, True, color)
    if center:
        x = DISPLAY_WIDTH // 2 - score_text.get_size()[0] //2
        y = DISPLAY_HEIGHT // 2 + score_text.get_size()[1] //2
    display.blit(score_text, [x, y])

# показать надпись GAME OVER
def show_game_over():
    global game_exit
    display.blit(background, [0, 0]) # перерисовываем фон экрана
    draw_text_to_screen(text=f"Game over! Score: {score}", color=RED, center=True)
    pg.display.update() #делаем обновление экрана
    sleep(4)
    game_exit = True

# apple position
apple_x = randomze_apple_pos(DISPLAY_WIDTH)
apple_y = randomze_apple_pos(DISPLAY_HEIGHT)

# wall position
wall_x = randomize_wall_pos(DISPLAY_WIDTH)
wall_y = randomize_wall_pos(DISPLAY_HEIGHT)

while not game_exit:
    check_events()
    head_pos = snake_movement()
    check_collide()
    redraw_screen() 
    pg.display.update() #чтобы обновить на экране всё, что произошло
    pg.time.delay(150) #для плавности движений, можно использовать для изменения скорости змейки

# освобождаем модуль из памяти (операция, обратная инициализации)
pg.quit()
