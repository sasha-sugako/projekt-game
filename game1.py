import os
import pygame
import sys
FPS = 50
size = WIDTH, HEIGHT = 1000, 500
tile_width = tile_height = 50
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Невозможно загрузить изображение из файла: ', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image = image.convert()
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["", "",
                  "Правила игры",
                  "Для ходьбы в разные стороны используйте", "стрелки вправо и влево или кнопки a, d",
                  "Для залезания по лестницам используйте стрелки вверх и вниз или кнопки w, s",
                  "Для стрельбы используйте кнопку b",
                  'Чтобы поставить игру на паузу используйте кнопку esc']

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 215
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 70
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():
    intro_text = ["Чтобы продолжить игру нажмите любую кнопку"]
    fon = pygame.transform.scale(load_image('pause.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def new_level():
    intro_text = ["Уровень 2", "Чтобы начать нажмите любую кнопку"]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 275
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 70
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def v_screen():
    intro_text = ["Вы выиграли", "Чтобы завершить игру нажмите любую кнопку"]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 275
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 70
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def die_screen():
    intro_text = ["Вы проиграли", "Чтобы завершить игру нажмите любую кнопку"]
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 275
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 70
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('wall.png'), 'empty': load_image('grass.png'), 'stairs': load_image('stair.png')}
player_image = load_image('pers.png')
player_image_dv_p = [load_image('pers.png'), load_image('run2.png'), load_image('run1.png')]
player_image_dv_l = [load_image('pers.png'),  load_image('run3.png'), load_image('run4.png')]
player_image_dv_vv = [load_image('climb1.png'), load_image('climb2.png'), load_image('pers.png')]
mobe_image = load_image('1.png')
bullet = [load_image('bullet_1.png'), load_image('bullet_2.png')]
dead_mob = load_image('12.png')
image_flag = [load_image('box.png'), load_image('grass.png')]
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'pew.wav'))
bax_sound = pygame.mixer.Sound(os.path.join('sound', 'bax.wav'))
pygame.mixer.music.load(os.path.join('sound', 'osn.wav'))
flag_sound = pygame.mixer.Sound(os.path.join('sound', 'flag.wav'))
win_sound = pygame.mixer.Sound(os.path.join('sound', 'win.wav'))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y
        self.coun = 0
        self.k_zizh = 3
        self.font = pygame.font.Font(None, 20)
        self.surf = self.font.render('Количество жизней: ' + str(self.k_zizh), True, [0, 0, 0])

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def moves(self, stor):
        x, y = self.pos
        if stor == 'up':
            if y > 0 and level1[y][x] == '#' and level1[y - 1][x] != '*':
                self.draw_animation(3)
                self.move(x, y - 1)
        if stor == 'down':
            if y < level_y and level1[y][x] == '#' and level1[y + 1][x] != '*':
                self.draw_animation(3)
                self.move(x, y + 1)
        if stor == 'left':
            if x > 0 and level1[y][x - 1] != '*':
                self.draw_animation(2)
                self.move(x - 1, y)
        if stor == 'right':
            if x < level_x and level1[y][x + 1] != '*':
                self.draw_animation(1)
                self.move(x + 1, y)

    def draw_animation(self, posi):
        if self.coun == 3:
            self.coun = 0
        if posi == 1:
            self.image = player_image_dv_p[self.coun]
            self.coun += 1
        if posi == 2:
            self.image = player_image_dv_l[self.coun]
            self.coun += 1
        if posi == 3:
            self.image = player_image_dv_vv[self.coun]
            self.coun += 1

    def zizh(self):
        self.k_zizh -= 1
        self.surf = self.font.render('Количество жизней: ' + str(self.k_zizh), True, [0, 0, 0])


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mobs, all_sprites)
        self.image = mobe_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.pos = pos_x, pos_y
        self.mob_update = True
        self.k = 0
        self.f = 0
        self.z = 1

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def dead(self):
        bax_sound.play()
        self.image = dead_mob
        self.mob_update = False
        self.z = -1

    def update(self):
        if self.mob_update:
            if player.pos[1] == self.pos[1]:
                if player.pos[0] - self.pos[0] < 0:
                    if self.f % 10 == 5:
                        self.move(self.pos[0] - 1, self.pos[1])
                else:
                    if self.f % 10 == 5:
                        self.move(self.pos[0] + 1, self.pos[1])
                self.f += 1
            else:
                if (self.k % 20 == 0 or self.k % 20 == 15) and level1[self.pos[1]][self.pos[0] - 1] != '*':
                    self.move(self.pos[0] - 1, self.pos[1])
                if (self.k % 20 == 5 or self.k % 20 == 10) and level1[self.pos[1]][self.pos[0] + 1] != '*':
                    self.move(self.pos[0] + 1, self.pos[1])
                self.k += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, facing):
        super().__init__(bullets)
        self.image = bullet[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 15)
        self.pos = pos_x, pos_y
        self.facing = facing

    def moves(self, x, y):
        self.pos = (x, y)
        if self.facing == -1:
            self.image = bullet[1]
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 15)


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(flag)
        self.image = image_flag[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def podn(self):
        flag_sound.play()
        self.image = image_flag[1]


class Oflag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(oflag)
        self.image = image_flag[0]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def podn(self):
        pygame.mixer.music.stop()
        win_sound.play()
        self.image = image_flag[1]


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
flag = pygame.sprite.Group()
oflag = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('stairs', x, y)
            elif level[y][x] == '*':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '/':
                Mob(x, y)
                Tile('empty', x, y)
            elif level[y][x] == '+':
                Flag(x, y)
                Tile('empty', x, y)
            elif level[y][x] == '%':
                Oflag(x, y)
                Tile('empty', x, y)
    return new_player, x, y


level1 = load_level('1.txt')
level2 = load_level('2.txt')
player, level_x, level_y = generate_level(level1)
start_screen()
pygame.mixer.music.play(loops=-1)
lastmove = 'right'
bul = []
x_b = []
running = True
while running:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            player.moves('down')
        if key[pygame.K_UP] or key[pygame.K_w]:
            player.moves('up')
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.moves('left')
            lastmove = 'left'
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.moves('right')
            lastmove = 'right'
        if key[pygame.K_ESCAPE]:
            pygame.mixer.music.pause()
            pause_screen()
            pygame.mixer.music.unpause()
        if key[pygame.K_b]:
            if lastmove == 'right':
                face = 1
            else:
                face = -1
            if len(bul) == 0:
                shoot_sound.play()
                bul.append(Bullet(player.pos[0], player.pos[1], face))
                y = player.pos[1]
                x_b.append(player.pos[0])
    for i in range(len(bul)):
        if (level1[y][x_b[i] + bul[i].facing] == '.' or level1[y][x_b[i] + bul[i].facing] == '#'
        or level1[y][x_b[i] + bul[i].facing] == '/' or level1[y][x_b[i] + bul[i].facing] == '%'):
            x_b[i] += 1 * bul[i].facing
        else:
            bul[i].kill()
            bul = []
            x_b = []
        if i < len(bul):
            bul[i].moves(x_b[i], player.pos[1])
    for i in mobs:
        for j in bullets:
            if j.rect.colliderect(i):
                i.dead()
                j.kill()
                bul = []
    if level1[player.pos[1]][player.pos[0]] == '+':
        for i in flag:
            i.podn()
        for i in mobs:
            i.kill()
        level1 = level2
        new_level()
        player, level_x, level_y = generate_level(level1)
    if level1[player.pos[1]][player.pos[0]] == '%':
        for i in oflag:
            i.podn()
        for i in mobs:
            i.kill()
        running = False
        v_screen()
    for i in mobs:
        if i.pos == player.pos and i.z == 1:
            player.zizh()
            screen.blit(player.surf, [125, 470])
    if player.k_zizh == 0:
        die_screen()
        running = False
    mobs.update()
    all_sprites.update()
    tiles_group.draw(screen)
    player_group.draw(screen)
    mobs.draw(screen)
    bullets.draw(screen)
    flag.draw(screen)
    oflag.draw(screen)
    screen.blit(player.surf, [125, 470])
    pygame.display.flip()
pygame.quit()