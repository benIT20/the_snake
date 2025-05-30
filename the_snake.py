from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс для объектов игры."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод для инициализации объектов в дочерних классах"""
        pass


class Apple(GameObject):
    """Дочерний класс для объекта яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None

    def randomize_position(self, snake_positions):
        """Метод, по простоновке объекта яблоко"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in snake_positions:
                break

    def draw(self):
        """Метод, по инициализации объекта яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс для объекта змея"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод, по смене направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, для отрисовки змеи в каждом цикле"""
        # Обновляем направление движения
        self.update_direction()

        # Получеаем текущую позицию головы
        current_head_position = self.get_head_position()

        # Вычисляем новую позицию головы
        new_head = (
            (current_head_position[0] + self.direction[0] * GRID_SIZE) %
            SCREEN_WIDTH,
            (current_head_position[1] + self.direction[1] * GRID_SIZE) %
            SCREEN_HEIGHT
        )

        # Добавляем новую позицию в начало списка позиций змейки
        self.positions.insert(0, new_head)

        # Удаляем последнюю позицию, если длина змейки не увеличилась
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def draw(self):
        """Метод, по инициализации объекта змея"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, для передачи посиции головы"""
        return self.positions[0]

    def reset(self):
        """Метод, по начальной инициализации змея"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((DOWN, UP, RIGHT, LEFT))
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция по запуску программы и ее дальнейшей работе"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    # Добавляем эту строку для инициализации позиции яблока
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка на столкновение с самим собой
        for position in snake.positions[1:]:
            if snake.positions[0] == position:
                snake.reset()
                apple.randomize_position(snake.positions)
                pygame.time.delay(500)
                break

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
