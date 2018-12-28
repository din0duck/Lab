import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        #сетка поля
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self) -> None:
        #Запуск
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_cell_list(clist)
            self.draw_grid()
            clist = self.update_cell_list(clist)
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:#здесь начинаются изменения
        """
            Создание списка клеток.

            Клетка считается живой, если ее значение равно 1.
            В противном случае клетка считается мертвой, то
            есть ее значение равно 0.
            Если параметр randomize = True, то создается список, где
            каждая клетка может быть равновероятно живой или мертвой.
            """
        if randomize == True:
            self.clist = [[random.randint(0, 1) for col in range(self.cell_width)] for row in range(self.cell_height)]
        else:
            self.clist = [[0 for col in range(self.cell_width)] for row in range(self.cell_height)]
        return self.clist

    def draw_cell_list(self, rects: list) -> None:
        """
           Отображение списка клеток 'rects' с закрашиванием их в
           соответствующе цвета
           """
        clist = rects
        for rown, row in enumerate(self.clist):
            for coln, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple) -> list:
        """
           Вернуть список соседних клеток для клетки cell.

           Соседними считаются клетки по горизонтали,
           вертикали и диагоналям, то есть во всех
           направлениях.
           """
        neigh = []
        row, col = cell
        neigh_posits = [(row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row - 1, col - 1), (row, col - 1), (row + 1, col - 1), (row - 1, col), (row + 1, col)]

        for neigh_pos in neigh_posits:
            row, col = neigh_pos
            if -1 < row < self.cell_height and -1 < col < self.cell_width:
                neigh.append(self.clist[row][col])
            else:
                neigh = [None]
        return neigh

    def update_cell_list(self, cell_list: list) -> list:
        """
         Отображение списка клеток 'rects' с закрашиванием их в
    соответствующе цвета
        """
        rects = [[0 for col in range(self.cell_width)] for row in range(self.cell_height)]
        for rown, row in enumerate(cell_list):
            for coln, col in enumerate(row):
                neighbours = self.get_neighbours((rown, coln))
                neighbours_num = neighbours.count(1)
                if neighbours_num == 3 or (neighbours_num == 2 and col == 1):
                    rects[rown][coln] = 1
        self.clist = rects
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()