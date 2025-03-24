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

    def draw(self):
        """Абстрактный метод для отрисовки объекта на игровом поле."""
        raise NotImplementedError(
            f'This method must be implemented in a {type(self).__name__} class'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, body_color=None):
        if body_color is None:
            body_color = APPLE_COLOR
        super().__init__(body_color=body_color)
        self.randomize_position()

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, body_color=None):
        if body_color is None:
            body_color = SNAKE_COLOR
        super().__init__(body_color=body_color)
        self.positions = [self.position]
        self.__next_position = None
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def is_food(self, *args):
        """Метод, проверяющий следующую позицию на самого себя или еду."""
        if self.__next_position in self.positions:
            self.reset()
            return None

        for food in args:
            if (isinstance(food, Apple)
                    and food.position == self.__next_position):
                food.randomize_position()
                food.draw()
                self.last = None
                return True
        return False

    def move(self, *args):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент.
        """
        self.update_direction()
        now_width, now_height = self.get_head_position()
        direction_width, direction_height = self.direction
        self.__next_position = (
            (now_width + (direction_width * GRID_SIZE)) % SCREEN_WIDTH,
            (now_height + (direction_height * GRID_SIZE)) % SCREEN_HEIGHT
        )
        check_next_position = self.is_food(*args)
        if check_next_position is not None:
            if check_next_position:
                self.positions.insert(0, self.__next_position)
            else:
                self.positions.insert(0, self.__next_position)
                self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        head_rect = pg.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.__init__()

    def update_direction(self):
        """обновляет направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
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
    apple = Apple()
    apple.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move(apple)
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
