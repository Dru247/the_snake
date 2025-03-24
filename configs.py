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

COLOR_BLACK = (0, 0, 0)
COLOR_LIME = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_TURQUOISE = (93, 216, 228)

# Цвет фона:
BOARD_BACKGROUND_COLOR = COLOR_BLACK

# Цвет границы ячейки
BORDER_COLOR = COLOR_TURQUOISE

# Цвет яблока
APPLE_COLOR = COLOR_RED

# Цвет змейки
SNAKE_COLOR = COLOR_LIME

# Скорость движения змейки:
SPEED = 20

# Начальная позиция игровых объектов
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
