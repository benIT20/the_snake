from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь противоположных направлений:
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

# Цветовая палитра игры:
BOARD_BACKGROUND_COLOR = (211, 211, 211)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject():
    """Базовый класс для объектов игры."""

    def __init__(self, color=None) -> None:
        self.position = INITIAL_POSITION
        self.body_color = color

    def draw_cell(self, position, color=None):
        """Отрисовка одной ячейки объекта"""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw_earse_cell(self, position):
        """Новый метод для затирания ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def draw(self):
        """Метод для инициализации объектов в дочерних классах"""


class Apple(GameObject):
    """Дочерний класс для объекта яблоко"""

    def __init__(self, occupied_positions=[], apple_color=APPLE_COLOR):
        super().__init__(apple_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, positions):
        """Метод, по простоновке объекта яблоко"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in positions:
                break

    def draw(self):
        """Метод, по инициализации объекта яблоко"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Дочерний класс для объекта змея"""

    def __init__(self, snake_color=SNAKE_COLOR):
        super().__init__(snake_color)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self, new_direction=None):
        """Обновляет направление движения змейки"""
        if new_direction:
            if new_direction != OPPOSITE_DIRECTIONS[self.direction]:
                self.direction = new_direction

    def move(self):
        """Перемещает змейку"""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку"""
        self.draw_cell(self.get_head_position())

        if self.last:
            self.draw_earse_cell(self.last)

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.position = INITIAL_POSITION
        self.length = 1
        self.positions = [INITIAL_POSITION]
        self.direction = choice((DOWN, UP, RIGHT, LEFT))
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Функция по запуску программы и ее дальнейшей работе"""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка на столкновение с самим собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            pg.time.delay(500)
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
