from random import randint
from sys import exit

import pygame as pg

from configs import (APPLE_COLOR, BOARD_BACKGROUND_COLOR, BORDER_COLOR, DOWN,
                     GRID_HEIGHT, GRID_SIZE, GRID_WIDTH, LEFT, RIGHT,
                     SCREEN_HEIGHT, SCREEN_WIDTH, SNAKE_COLOR, SPEED,
                     START_POSITION, UP)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=None, position=None):
        self.position = START_POSITION if position is None else position
        self.body_color = body_color

    def draw_position(self, position, color=None, border=True):
        """Отрисовывает позицию на игровом поле."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для отрисовки объекта на игровом поле."""
        raise NotImplementedError(
            f'This method must be implemented in a {type(self).__name__} class'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, busy_positions, body_color=None):
        if body_color is None:
            body_color = APPLE_COLOR
        super().__init__(body_color=body_color)
        self.randomize_position(busy_positions)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_position(self.position)

    def randomize_position(self, busy_positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in busy_positions:
                self.position = new_position
                break


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, body_color=None):
        if body_color is None:
            body_color = SNAKE_COLOR
        super().__init__(body_color=body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент.
        """
        if self.last:
            self.positions.pop()

        now_width, now_height = self.get_head_position()
        direction_width, direction_height = self.direction
        next_position = (
            (now_width + (direction_width * GRID_SIZE)) % SCREEN_WIDTH,
            (now_height + (direction_height * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, next_position)
        self.last = self.positions[-1]

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        self.draw_position(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            self.draw_position(
                self.last,
                color=BOARD_BACKGROUND_COLOR,
                border=False
            )

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()

    def update_direction(self, direction):
        """обновляет направления после нажатия на кнопку."""
        self.direction = direction


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                game_quit()


def game_quit():
    """Функция завершения игры."""
    pg.quit()
    exit()


def main():
    """Основной фнкционал."""
    # Инициализация pygame:
    pg.init()
    snake = Snake()
    apple = Apple(busy_positions=snake.positions)
    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            apple.randomize_position(busy_positions=snake.positions)
            apple.draw()
            snake.last = None

        if snake.get_head_position() in snake.positions[1:]:
            for position in snake.positions:
                snake.draw_position(position, color=BOARD_BACKGROUND_COLOR)
            snake.reset()

        snake.draw()
        snake.move()

        pg.display.update()


if __name__ == '__main__':
    main()
