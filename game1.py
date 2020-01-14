import os
import pygame
import sys
import random
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
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'), 'stairs': load_image('box.png')}
player_image = load_image('pers.png')
mobe_image = load_image('1.png')

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

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def moves(self, stor):
        x, y = self.pos
        if stor == 'up':
            if y > 0 and level[y][x] == '#' and level[y - 1][x] != '*':
                self.move(x, y - 1)
        if stor == 'down':
            if y < level_y and level[y][x] == '#' and level[y + 1][x] != '*':
                self.move(x, y + 1)
        if stor == 'left':
            if x > 0 and level[y][x - 1] != '*':
                self.move(x - 1, y)
        if stor == 'right':
            if x < level_x and level[y][x + 1] != '*':
                self.move(x + 1, y)


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mobs, all_sprites)
        self.image = mobe_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)

    def update(self):
        x, y = self.pos
        if level[y][x + 1] == '.' or level[y][x - 1] == '.':
            self.rect.x = random.choice(tile_width * (self.pos[0] - 1) + 15, tile_width * (self.pos[0] + 1) + 15)


class Bullet():
    def __init__(self, x, y, r, col,  facing):
        self.y = y
        self.x = x
        self.r = r
        self.col = col
        self.facing = facing
        self.speedy = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.col, (self.x, self.y), self.r)


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()


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
    return new_player, x, y


level = load_level('1.txt')
player, level_x, level_y = generate_level(level)
start_screen()
sna = []
lastmove = 'right'
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
        if key[pygame.K_b]:
            if lastmove == 'right':
                facing = 1
            else:
                facing = -1
            if len(sna) < 5:
                sna.append(Bullet(player.pos[0] * tile_width + 20, player.pos[1] * tile_width + 15,
                                  8, (255, 0, 0), facing))
    for i in sna:
        if i.x < 1000 and i.x > 0:
            i.x += i.speedy
            print(i.x)
            i.draw(screen)
        else:
            sna.pop(sna.index(i))
    all_sprites.update()
    tiles_group.draw(screen)
    player_group.draw(screen)
    mobs.draw(screen)
    pygame.display.flip()
pygame.quit()