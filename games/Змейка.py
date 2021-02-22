import pygame
from random import randrange, randint
from time import sleep


def start():
    FPS = 50
    WIDTH, HEIGHT = 720, 460
    running = True

    class Game():
        def __init__(self):
            # необходимые цвета
            self.red = pygame.Color(255, 0, 0)
            self.green = pygame.Color(0, 255, 0)
            self.black = pygame.Color(0, 0, 0)
            self.white = pygame.Color(255, 255, 255)
            self.brown = pygame.Color(165, 42, 42)
            # будет задавать количество кадров в секунду
            self.fps_controller = pygame.time.Clock()
            # количество сьеденной еды
            self.score = 0

        def set_surface_and_title(self):
            """Задаем surface(поверхность поверх которой будет все рисоваться)
            и устанавливаем заголовок окна"""
            self.play_surface = pygame.display.set_mode((
                WIDTH, HEIGHT), )
            pygame.display.set_caption('Змейка')

        def event_loop(self, change_to):
            nonlocal running
            # Функция для отслеживания нажатий клавиш игроком
            for event in pygame.event.get():
                # если нажали клавишу
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        change_to = "RIGHT"
                    elif event.key == pygame.K_LEFT or event.key == ord('a'):
                        change_to = "LEFT"
                    elif event.key == pygame.K_UP or event.key == ord('w'):
                        change_to = "UP"
                    elif event.key == pygame.K_DOWN or event.key == ord('s'):
                        change_to = "DOWN"
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            return change_to

        def refresh_screen(self):  # обновляем экран и задаем фпс
            pygame.display.flip()
            game.fps_controller.tick(20)

        def show_score(self, choice=1):  # Отображение результата
            try:
                s_font = pygame.font.SysFont(None, 24)
            except:
                pass
            s_surf = s_font.render(
                'Score: {}'.format(self.score), True, self.white)
            s_rect = s_surf.get_rect()
            # при choice = 1 результат будет отображаться в левом верхнем углу
            if choice == 1:
                s_rect.midtop = (35, 10)
            else:
                # при game_overe отображаем результат по центру
                # под надписью game over
                s_rect.midtop = (360, 120)
            self.play_surface.blit(s_surf, s_rect)  # рисуем прямоугольник поверх surface

        def game_over(self):
            nonlocal running
            """Функция для вывода надписи Game Over и результатов
            в случае завершения игры и выход из игры"""
            go_font = pygame.font.SysFont(None, 72)
            go_surf = go_font.render('Game over', True, self.red)
            go_rect = go_surf.get_rect()
            go_rect.midtop = (360, 15)
            self.play_surface.blit(go_surf, go_rect)
            self.show_score(0)
            pygame.display.flip()
            sleep(3)
            running = False

    class Snake():
        def __init__(self, snake_color):
            # важные переменные - позиция головы змеи и его тела
            self.snake_head_pos = [100, 50]
            # начальное тело змеи состоит из трех сегментов
            self.snake_body = [[100, 50], [90, 50], [80, 50]]
            self.snake_color = snake_color
            # направление движение змеи, изначально зададимся вправо
            self.direction = "RIGHT"
            # куда будет меняться напраление движения змеи при нажатии соответствующих клавиш
            self.change_to = self.direction

        def validate_direction_and_change(self):
            # Изменяем направление движения змеи только в том случае, если
            # оно не прямо противоположно текущему
            if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                    self.change_to == "LEFT" and not self.direction == "RIGHT",
                    self.change_to == "UP" and not self.direction == "DOWN",
                    self.change_to == "DOWN" and not self.direction == "UP")):
                self.direction = self.change_to

        def change_head_position(self):  # Изменияем положение головы змеи
            if self.direction == "RIGHT":
                self.snake_head_pos[0] += 10
            elif self.direction == "LEFT":
                self.snake_head_pos[0] -= 10
            elif self.direction == "UP":
                self.snake_head_pos[1] -= 10
            elif self.direction == "DOWN":
                self.snake_head_pos[1] += 10

        def snake_body_mechanism(
                self, score, food_pos, screen_width, screen_height):
            # идет управление координат тела
            self.snake_body.insert(0, list(self.snake_head_pos))
            # если съели еду
            if (int(self.snake_head_pos[0]) in range(int(food_pos[0]) - 10,
                                                     int(food_pos[0] + 10)) and
                    int(self.snake_head_pos[1]) in range(int(food_pos[1]) - 10,
                                                             int(food_pos[1]) + 10)):
                # если съели еду, то задаем новое положение еды случайным образом и увеличивем score на один
                food_pos = [randrange(1, screen_width / 10) * 10,
                            randrange(1, screen_height / 10) * 10]
                score += 1
            else:  # если не нашли еду, то убираем последний сегмент
                self.snake_body.pop()
            return score, food_pos

        def draw_snake(self, play_surface, surface_color):
            # Отображаем все сегменты змеи
            play_surface.fill(surface_color)
            for pos in self.snake_body:
                rect = pygame.Rect(pos[0], pos[1], 10, 10)
                pygame.draw.rect(
                    play_surface, self.snake_color, rect)

        def check_for_boundaries(self, game_over, screen_width, screen_height):
            # Проверка, что столкунлись с концами экрана или сами с собой
            if any((
                self.snake_head_pos[0] > screen_width - 10 or
                self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10 or
                self.snake_head_pos[1] < 0
            )):
                game_over()
            for block in self.snake_body[1:]:
                # проверка на то, что первый элемент врезался в любой
                # другой элемент змеи
                if (block[0] == self.snake_head_pos[0] and
                        block[1] == self.snake_head_pos[1]):
                    game_over()

    class Food():
        def __init__(self, food_color, screen_width, screen_height):
            self.food_color = food_color
            self.food_pos = [randrange(1, screen_width / 10) * 10,
                             randrange(1, screen_height / 10) * 10]

        def draw_food(self, play_surface):  # Отображение еды
            pygame.draw.circle(play_surface, self.food_color,
                               (self.food_pos[0], self.food_pos[1]), 10)

    pygame.init()
    game = Game()
    snake = Snake(game.green)
    food = Food(game.red, WIDTH, HEIGHT)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load(f'data/track_{randint(1,6)}.mid')
    pygame.mixer.music.play(1)
    game.set_surface_and_title()
    while running:
        snake.change_to = game.event_loop(snake.change_to)

        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(
            game.score, food.food_pos, WIDTH, HEIGHT)
        snake.draw_snake(game.play_surface, game.black)

        food.draw_food(game.play_surface)

        snake.check_for_boundaries(
            game.game_over, WIDTH, HEIGHT)

        game.show_score()
        game.refresh_screen()
    pygame.quit()