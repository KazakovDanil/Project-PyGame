import pygame
from random import randint, random, choice
import os
import sys


def start():
    '''Функция, вызывающая клон игры "Арканоид".'''
    # Создадим флаг начала игры, кол-во очков и установим кол-во кадров
    # в секунду.
    running = True
    begin = False
    score = 0
    FPS = 30
    # Чтобы в дальнейшем было удобнее проверять столкновения, укажем collides.
    collides = pygame.sprite.spritecollideany
    # Задаём размеры окна и "кирпичиков" (здесь они, как и бита игрока,
    # названы платформами). Размеры окна не будут равны именно 800х600 потому,
    # что по бокам экрана установлены границы толщиной в 5 пикселей. Похожим
    # образом дело обстоит и с платформами: чтобы быть визуально отличимыми,
    # размеры будут на пиксель урезаны снизу и справа.
    SIZE = WIDTH, HEIGHT = 810, 600
    PLATFORM_SIZE = (99, 29)

    # --------------------------------------------------------------------------
    # Объявляем необходимые для игры классы.
    # --------------------------------------------------------------------------

    # Сначала создадим классы подвижных объектов - шара и бонусов.

    # Стоит объяснить значение некоторых использованных в комментариях терминов:
    # О. = объект;
    # Тело О. - Фигура, по которой проходят взаимодействия с другими объектами.
    # Физика О. - параметры, отвечающие за перемещение О. по экрану.

    class Ball(pygame.sprite.Sprite):
        '''Шар, с помощью которого игрок будет выбивать платформы.'''

        def __init__(self, x, y, radius=15):
            super().__init__(all_sprites)
            # Добавим шар в соответствующее множество спрайтов.
            self.add(balls)
            # Любопытный момент: геометрически объект будет действиьно шаром
            # (вернее, кругом)...
            self.radius = radius
            self.image = pygame.Surface((2 * radius, 2 * radius),
                                        pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color("gray"),
                               (radius, radius), radius)
            # ... но столкновения расчитываются по квадрату!
            self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
            # Инициализуем физику объекта: скорость и направления по осям Х и У.
            self.speed = 3
            self.dx = choice((-1, 1))
            self.dy = -1

        def update(self):
            key = pygame.key.get_pressed()
            sprites = platforms.sprites()
            self.rect = self.rect.move(self.dx * self.speed,
                                       self.dy * self.speed)
            if collides(self, horizontal_borders):
                self.dy = -self.dy
            if collides(self, vertical_borders):
                self.dx = -self.dx
            if collides(self, platforms):
                hit = self.rect.collidelist(list(map(
                    lambda a: a.rect, platforms)))
                self.dx, self.dy = detect_collision(self.dx, self.dy, self.rect,
                                                    sprites[hit].rect)
                obj = platforms.sprites()[hit]
                if isinstance(obj, Platform):
                    obj.kill(self.dx, self.dy)
            if collides(self, player_platforms):
                self.dx, self.dy = detect_collision(self.dx, self.dy, self.rect,
                                                    PP.rect)
            if self.rect.top > HEIGHT:
                self.kill()

    class Bonus(pygame.sprite.Sprite):
        '''Бонус, с некоторым шансом выпадающий из платформ.'''

        def __init__(self, x, y, dx, dy):
            super().__init__(all_sprites)
            # Бонусы будут разделяться на два вида: монету и коробку с шариком.
            # Зададим появляющемуся бонусу случайный тип.
            bonus_types = ('coin', 'add_ball')
            self.b_type = randint(0, 1)
            # Изображением этого бонуса будет зависящая от его типа картинка
            self.image = load_image(f"{bonus_types[self.b_type]}.jpg")
            # Инициализуем физику объекта: скорость и направления по осям Х и У.
            self.speed = 5
            self.dx = dx
            self.dy = dy
            # Тело объекта - прямоугольник, по которому
            # будут проходить столкновения.
            self.rect = pygame.Rect(x, y, 50, 50)

        def update(self):
            nonlocal score
            # Тело бонуса будет смещаться по оси Х с постоянной скоростью,
            # которая задаётся при инициализации, но по оси У направление
            # бонуса будет увеличиваться, имитируя падение в реальности.
            self.rect = self.rect.move(self.dx * self.speed, self.dy)
            # dy увеличивается - стоит напомнить: начало координат в pygame -
            #  левый верхний угол, ось ОУ направлена вниз.
            self.dy += 0.2
            if collides(self, player_platforms):
                if self.b_type:
                    # Если бонус попадает на биту и его тип - бонусный мяч,
                    # на её середине появляется мяч.
                    Ball(PP.rect.x + PP.w // 2, PP.rect.top - 30)

                else:
                    # Если тип бонуса - монета, то игрок получает 5 очков.
                    score += 5
                # После встречи с битой бонус уничтожается.
                self.kill()

            # При встрече со стеной бонус упруго отскакивает.
            if collides(self, vertical_borders):
                self.dx = -self.dx

    class PlayerPlatform(pygame.sprite.Sprite):
        '''Бита, управляемая игроком.'''

        def __init__(self, x, y):
            super().__init__(all_sprites)
            # Располагаем и задаём размеры биты.
            self.x, self.y, self.w, self.h = x, y, 100, 20
            # Добавим биту в соответствующее множество. Она будет одна,
            # но так проще отследить столкновения.
            self.add(player_platforms)
            # Изображением и телом биты будет прямоугольник 100х20 пикселей.
            self.image = pygame.Surface([self.w, self.h])
            self.image.fill(pygame.Color('gray'))
            self.rect = pygame.Rect(x, y, self.w, self.h)
            # Единственый параметр физики объекта - скорость, поначалу нулевая.
            self.speed = 0

        def update(self):
            # Получаем доступ к клавиатуре.
            key = pygame.key.get_pressed()

            if key[pygame.K_LEFT]:
                # Если кажата клавиша "влево", бита смещается налево.
                self.speed = -8
                if self.rect.left + self.speed < 0:
                    # Если далее идёт граница, бита останавливается.
                    self.speed = 0

            elif key[pygame.K_RIGHT]:
                # Если кажата клавиша "вправо", бита смещается направо.
                self.speed = 8
                if self.rect.right + self.speed > WIDTH:
                    # Если справа граница, бита останавливается.
                    self.speed = 0

            else:
                # Если ничего из вышеприведённого не нажато, скорость обнуляется.
                self.speed = 0
            # Чтобы бита сместилась, смещаем её тело.
            self.rect = self.rect.move(self.speed, 0)

    # Далее идут неподвижные классы.

    class Platform(pygame.sprite.Sprite):
        '''Платформы - это "кирпичики", которые надо выбить в оригинальной игре.
        Цвет означает, по сути, прочность: градация цвета такая же, как 
        у радуги; красный кирпич - самый хрупкий, фиолетовый - самый твёрдый.'''

        def __init__(self, x, y, c):
            super().__init__(all_sprites)
            # Цвет и координаты левого верхнего угла зададим.
            self.c = c
            self.x, self.y = x, y
            # Добавим платформу в соответствующее множество.
            self.add(platforms)
            # Цвет платформы задаётся через нижеприведённый кортеж (голубой цвет
            # пришлось добавлять кортежем, т.к. нет подходящего цвета в pygame).
            colors = ('Red',
                      'orange',
                      'yellow',
                      'green',
                      (70, 170, 250),
                      'blue',
                      'purple',)
            self.image = pygame.Surface(PLATFORM_SIZE)
            self.image.fill(pygame.Color(colors[c]))
            # Тело - прямоугольник соответствующего изображению размера.
            self.rect = pygame.Rect(x, y, *PLATFORM_SIZE)

        def kill(self, dx, dy):
            nonlocal score
            # Eсли цвет платформы старше красного, появляется более хрупкий
            # "потомок". Красные платформы просто уничтожаются.
            # В любом случае счёт увеличится на 1.
            if self.c:
                Platform(self.x, self.y, self.c - 1)
            score += 1
            # Со случайным шансом (не) появляется бонус.
            if random() > 0.92:
                Bonus(self.x + PLATFORM_SIZE[0] // 2, self.y, dx, dy)
            # "Родитель" уничтожается.
            super().kill()

    class Border(pygame.sprite.Sprite):
        '''Границы игрового экрана.'''
        # Границей будет строго вертикальный или строго горизонтальный отрезок.

        def __init__(self, x1, y1, x2, y2):
            super().__init__(all_sprites)
            # Шаблон создания границ прост:
            # 1. Добавление в соответствующее множество;
            # 2. Создание вида объекта;
            # 3. Создание тела объекта.
            # Различие лишь в расположении стенки в пространстве.
            if x1 == x2:
                # Вертикальная стенка
                self.add(vertical_borders)
                self.image = pygame.Surface([10, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 10, y2 - y1)
            else:
                # Горизонтальная стенка
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 10])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 10)

    # --------------------------------------------------------------------------
    # Далее идут функции, необходимые для взаимодействия между объектами.
    # --------------------------------------------------------------------------

    def terminate():
        '''Окончание игры.'''
        # Закрываем PyGame.
        pygame.quit()
        # sys.exit()

    def load_image(name):
        '''Функция, позволяющая загрузить изображение.'''
        # Складываем полное имя файла.
        fullname = os.path.join('data', name)
        # Eсли файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        # При наличии изображения загружаем его.
        image = pygame.image.load(fullname)
        return image

    def show_screen(win=None):
        '''Функция показывает один из трёх экранов: начальный, экран поражения
        или экран победы.'''
        # Введём строку для отображения счёта.
        # Выводится начальный экран - счёт не нужно показывать.
        score_text = f'Ваш счёт: {score}.'
        # Добавим подсказки для пользователя, какие клавиши что выполняют.
        keys = ('', 'R - начать заново.', 'Esc - выйти из игры.')
        # В зависимости от значения win, фон и текст будут отличаться.
        text_and_image = {None: ("Арканоид",
                                 "",
                                 "Двигайте серую платформу",
                                 'С помощью кнопок "влево" и "вправо",',
                                 "чтобы выбить все кирпичики сверху",
                                 "и не дать шарику упасть.",
                                 'background_arkanoid_begin.jpg'),

                          0: ('Вы проиграли.',
                              score_text,
                              *keys,
                              'background_arkanoid_lose.jpg'),

                          1: ('Поздравляем, вы победили!',
                              score_text,
                              *keys,
                              'background_arkanoid_win.jpg')}
        # Задаём фон.
        fon = pygame.transform.scale(load_image(text_and_image[win][-1]), (
            WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # Шрифт для выводимого текста.
        font = pygame.font.Font(None, 30)
        # Зададим начальную координату текста по оси OУ.
        text_coord = 180
        # Выведим текст построчно.
        for line in text_and_image[win][:-1]:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        # Технически, эта функция - "под-игра": пока пользователь
        # не нажмёт любую клавишу, будет отображаться данный экран.
        while True:
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                # Если пользователь захочет просто выйти из игры,
                # он может нажать Escape или закрыть окно через "крестик".
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    key = pygame.key.get_pressed()
                    # В случае проигрыша пользователь может нажать R
                    # и тем самым перезапустить игру.
                    if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                        terminate()
                    if key[pygame.K_r] and win is not None:
                        start()
                    if win is None:
                        # Начинаем игру, если нажата любая клавиша
                        # и отображается не экран поражения.
                        # Иначе - игра просто закрывается.
                        return  # Одно слово, а как неоднозначно!
            pygame.display.flip()
            clock.tick(FPS)

    def detect_collision(dx, dy, ball, rect):
        '''Функция, определяющая поведение сталкивающихся объектов.'''
        # Если шар летел направо, то delta_x высчитывается как разность
        # между правой стороной шара и левой - платформы. Иначе - наоборот.
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        # Если шар падал на блок, то delta_y высчитывается как разность
        # между низом шара и верхом платформы. И наоборот.
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_y - delta_x) < 10:
            # Разность "дельт" невелика, т.е. шар попал в угол платформы.
            # В таком случае шар отскакивает
            # в противоположном изначальному направлении.
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            # Если шар попадает скорее в "фасад" платформы,
            # отражается направление по ветикали.
            dy = -dy
        elif delta_y > delta_x:
            # Если шар попадает скорее в торец платформы,
            # отражается направление по горизонтали.
            dx = -dx
        return dx, dy

    # --------------------------------------------------------------------------
    # Далее идут инициализации необходимых переменных и основная часть игры.
    # --------------------------------------------------------------------------

    # Иициализируем окно игры.
    pygame.init()
    pygame.display.set_caption('Arkanoid')
    screen = pygame.display.set_mode(SIZE)
    # Создадим группы спрайтов для всех спрайтов, вертикальных и горизонтальной
    # границ, платформ, шаров и биты игрока.
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    player_platforms = pygame.sprite.Group()
    # Создадим таймер для игры.
    clock = pygame.time.Clock()
    # Также нам понадобятся музыкальное событие и трёхминутный таймер.
    # Их необходимость будет показана ниже.
    MUSICEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MUSICEVENTTYPE, 180000)
    # Задаём поле из случайных платформ.
    for i in range(8):
        for j in range(6):
            Platform(5 + 100 * i, 5 + 30 * j, randint(0, 6))
    # Создаём границы, чтобы шары не вылетали за пределы экрана.
    Border(-5, -5, WIDTH, 0)
    Border(-5, 5, -5, HEIGHT)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT)
    # Отображаем пользователю экран с инструкциями насчёт игры.
    show_screen()
    # Если пользователь не вышел из игры в show_screen(), создаётся бита.
    PP = PlayerPlatform((WIDTH - 100) // 2, HEIGHT - 20)
    # Да будет музыка! Инициализуем mixer и поставим случайную композицию.
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load(f'data/track_{randint(1,6)}.mid')
    pygame.mixer.music.play(1)

    while running:
        for event in pygame.event.get():
            # Пользователь выходит - закрываем программу.
            if event.type == pygame.QUIT:
                terminate()

            # Подключаем события с клавиатуры.
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                # Пользователь нажал Escape - закрываем программу.
                terminate()

            if key[pygame.K_SPACE] and begin == 0:
                # Нажат пробел - выпускаем мяч и начинаем игру.
                begin = 1
                Ball(PP.rect.left + 50, PP.rect.top - 30)

            if event.type == MUSICEVENTTYPE:
                # Вот зачем нужно "музыкальное" событие: каждые 3 минуты
                # в очередь будет ставиться новый саундтрек.
                pygame.mixer.music.queue(f'data/track_{randint(1,6)}.mid')
        screen.fill((255, 255, 255))
        if not begin:
            # Пока пользователь не нажал пробел, будет выводиться надпись.
            font = pygame.font.Font(None, 30)
            text = font.render(
                "Нажмите пробел, чтобы выпустить шар", True, (100, 100, 100))
            screen.blit(text, (WIDTH // 4, HEIGHT - 60))
        # Отображаем все спрайты и поддерживаем стабильное количество FPS.
        all_sprites.draw(screen)
        balls.update()
        all_sprites.update()
        clock.tick(FPS)
        # Если игра началась, а шаров/платформ на экране нет,
        # игра останавливается (при этом музыка плавно стихает).
        if (not len(balls.sprites()) or not len(platforms.sprites())) and begin:
            running = False
            pygame.mixer.music.fadeout(2000)
        # Отображаем счёт игрока.
        font = pygame.font.Font(None, 40)
        text = font.render(f"{score}", True, (120, 155, 220))
        screen.blit(text, (5, 570))
        pygame.display.flip()
    # Игра окончена - выводим экран о победе/поражении.
    show_screen(win=not len(platforms.sprites()))
    terminate()

