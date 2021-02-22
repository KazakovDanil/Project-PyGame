import pygame
from time import sleep
from random import randint


def start():
    running = True

    class Game:
        def __init__(self, width, height, screen):
            self.screen = screen
            pygame.display.set_caption('Крестики-нолики')
            self.width = width
            self.height = height
            # В board будет содержаться двумерный массив, по которому
            # мы будем определять победу
            self.board = [[0] * width for _ in range(height)]
            # указываем отступ слева и сверху и размер клеток
            self.left = 2
            self.top = 2
            self.cell_size = 100
            self.count = 0
            self.o, self.x, self.f = 0, 0, 0

        def render(self, screen):  # идет создание поля 3x3
            size = self.cell_size
            for y in range(self.height):
                for x in range(self.width):
                    pygame.draw.rect(screen, 'white',
                                     (self.left + size * x, self.top + size * y,
                                      size, size), not self.board[y][x])

        def get_cell(self, mouse_pos):
            size = self.cell_size
            for i in range(self.width):
                for j in range(self.height):
                    a = self.left + size * j
                    a1 = self.left + size * (j + 1)
                    b = self.top + size * i
                    b1 = self.top + size * (i + 1)
                    if mouse_pos[0] in range(b, b1) and mouse_pos[1] in range(a, a1):
                        return i, j
            return None

        def on_click(self, cell_coords):
            # реагирование на мышь(ставится крестик или нолик)
            if cell_coords:
                x_click = cell_coords[0]
                y_click = cell_coords[1]
                for y in range(self.height):
                    for x in range(self.width):
                        if x == x_click and y == y_click:
                            if not self.board[y][x]:
                                self.count += 1
                                rect = pygame.Rect(x * self.cell_size + 6,
                                                   y * self.cell_size + 6,
                                                   94, 94)
                                if self.count % 2 == 0:
                                    pygame.draw.ellipse(screen,
                                                        pygame.Color('red'),
                                                        rect, 2)
                                    self.board[y][x] = 2
                                else:
                                    pygame.draw.line(screen,
                                                     pygame.Color('blue'),
                                                     [rect[0], rect[1]],
                                                     [rect[0] + 94,
                                                      rect[1] + 94], 3)
                                    pygame.draw.line(screen,
                                                     pygame.Color('blue'),
                                                     [rect[0], rect[1] + 94],
                                                     [rect[0] + 94, rect[1]], 3)
                                    self.board[y][x] = 1

        def get_click(self, mouse_pos):  # проверяем поле на победу
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)
            if self.board[0][0] == self.board[0][1] == self.board[0][2] and\
               self.board[0][0] != 0:
                if self.board[0][0] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[1][0] == self.board[1][1] == self.board[1][2] and\
                    self.board[1][1] != 0:
                if self.board[1][0] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[2][0] == self.board[2][1] == self.board[2][2] and\
                    self.board[2][2] != 0:
                if self.board[2][0] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[1][0] == self.board[0][0] == self.board[2][0] and\
                    self.board[1][0] != 0:
                if self.board[1][0] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[1][1] == self.board[0][1] == self.board[2][1] and\
                    self.board[2][1] != 0:
                if self.board[1][1] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[0][2] == self.board[1][2] == self.board[2][2] and\
                    self.board[2][2] != 0:
                if self.board[0][2] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[2][2] != 0:
                if self.board[0][0] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[2][0] != 0:
                if self.board[0][2] == 2:
                    self.o = 1
                else:
                    self.x = 1
            elif self.count == 9:
                self.f = 1
            self.win(self.x, self.o, self.f)

        def win(self, x, o, f):  # функция, которая определяет победу и ничью
            nonlocal running
            if x or o:
                win = 'крестики' if x else 'нолики'
                font = pygame.font.SysFont(None, 20)
                text = font.render("Победили " + win + '!', True, (100, 255, 100))
                rect = text.get_rect()
                rect.midtop = (75, 304)
                self.screen.blit(text, rect)
                rect = text.get_rect()
                running = False
            if f:
                font = pygame.font.SysFont(None, 20)
                text = font.render('Победила дружба!', True, (100, 255, 100))
                rect = text.get_rect()
                rect.midtop = (75, 304)
                self.screen.blit(text, rect)
                rect = text.get_rect()
                running = False

    pygame.init()
    size = width, height = 304, 404
    screen = pygame.display.set_mode(size)
    game = Game(3, 3, screen)
    screen.fill((0, 0, 0))
    game.render(screen)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load(f'data/track_{randint(1,6)}.mid')
    pygame.mixer.music.play(1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.flip()
    sleep(2)
    pygame.quit()
