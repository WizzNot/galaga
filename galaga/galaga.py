import pygame
import os
import sys
import math
import random
pygame.init()
pygame.display.set_caption('GALAGA')
screen_size = (800, 1000)
screen = pygame.display.set_mode(screen_size)
width = 800
height = 1000


def terminate():
    pygame.quit()
    sys.exit()



def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


sounds = {'start': pygame.mixer.Sound(os.path.join('data', 'theme.mp3')), \
          'level': pygame.mixer.Sound(os.path.join('data', 'levelstart.mp3')), \
          'anykey': pygame.mixer.Sound(os.path.join('data', 'anykey.mp3')), \
          'fire': pygame.mixer.Sound(os.path.join('data', 'fire.mp3')), \
          'gameover': pygame.mixer.Sound(os.path.join('data', 'gameover.mp3'))}


def startscreen():
    run = True
    # TEXT
    font = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 36)
    text = font.render("GALAGA", True, (0, 0, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - 100
    text_w = text.get_width()
    text_h = text.get_height()
    # GALAGA
    font2 = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 10)
    author = font2.render("Made by WizzNot / YandexLyceum Project", True, (255, 255, 255))
    author_x = width // 2 - text.get_width() // 2 - 70
    author_y = height // 2 - text.get_height() // 2 + 300
    author_w = text.get_width()
    author_h = text.get_height()
    # AUTHOR
    font3 = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 20)
    anykey = font3.render("PRESS ANY KEY", True, (255, 0, 0))
    anykey_x = width // 2 - text.get_width() // 2 - 25
    anykey_y = height // 2 - text.get_height() // 2 + 100
    anykey_w = text.get_width()
    anykey_h = text.get_height()
    # ANYKEY
    anykeydraw = True
    timeconst = pygame.USEREVENT + 1
    pygame.time.set_timer(timeconst, 1000)
    sounds['start'].play()
    screen.blit(text, (text_x, text_y))
    screen.blit(author, (author_x, author_y))
    pygame.display.flip()
    pygame.time.delay(6200)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                run = False
            if event.type == timeconst:
                anykeydraw = abs(anykeydraw - 1)
        screen.fill((0, 0, 0))
        if anykeydraw:
            sounds['anykey'].play()
            screen.blit(anykey, (anykey_x, anykey_y))
        screen.blit(text, (text_x, text_y))
        screen.blit(author, (author_x, author_y))
        pygame.display.flip()


sprites = {1: [load_image('enemy1.png'), load_image('enemy11.png')], 2: [load_image('enemy2.png'), load_image('enemy22.png')], 3: [load_image('enemy33.png'), load_image('enemy3.png')]}
screen.fill((0, 0, 0))

all_sprites = pygame.sprite.Group()
player = pygame.sprite.Sprite(all_sprites)
player.image = load_image('player.png')
player.rect = player.image.get_rect()
kx = width // 2
ky = height - 70
player.rect.topleft = (kx, ky)


class Enemy:
    def __init__(self, typee, startcoords, trajectoryfunc):
        self.type = typee
        self.animated = 0
        self.func = trajectoryfunc
        self.coords = startcoords
        self.plusx = startcoords[0]
        self.plusy = startcoords[1]
        self.countfunc = 0
        self.sprite = pygame.sprite.Sprite(all_sprites)
        self.sprites = sprites[typee]
        self.sprite.image = self.sprites[self.animated]
        self.sprite.rect = self.coords
    
    def move(self):
        i, j = self.func[self.countfunc]([self.coords[0] - self.plusx, self.coords[1] - self.plusy])
        self.coords = [i + self.plusx, j + self.plusy]
        self.sprite.rect = self.coords
    
    def newsprite(self):
        self.animated = abs(self.animated - 1)
        self.sprite.image = self.sprites[self.animated]
    
    def newfunc(self):
        if self.countfunc == len(self.func) - 1:
            self.countfunc = 0
        else:
            self.countfunc += 1
        self.plusx = self.coords[0]
        self.plusy = self.coords[1]


class Bullet:
    def __init__(self, xcoord):
        self.coords = [xcoord + 23, height - 70]
        self.sprite = pygame.sprite.Sprite(all_sprites)
        self.sprite.image = load_image('missle.png')
        self.sprite.rect = self.coords
    
    def move(self):
        self.coords[1] -= 20
        self.sprite.rect = self.coords


functions = {1: [lambda x: [x[0] + 15, x[1]], lambda x: [x[0] - 15, x[1]]], \
             2: [lambda x: [x[0] + 10, math.sin(x[0] / 100) * 100], lambda x: [x[0] - 10, -1 * math.sin(x[0] / 100) * 100], lambda x: [x[0] + 15, x[1]], lambda x: [x[0] - 15, x[1]]], \
             3: [lambda x: [x[0] + 10, x[1] + 10], lambda x: [x[0] - 10, x[1] + 10], lambda x: [x[0] + 10, x[1] - 10]]}


def generate_level():
    enemies = []
    for i in range(random.randint(10, 20)):
        typee = random.randint(1, 3)
        enemies.append(Enemy(typee, [50 + i * 30, 200], functions[typee]))
    return enemies


def end_screen(score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 15)
    text = font.render("YOUR SCORE: {}".format(score), True, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 + 100
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    font2 = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 36)
    text2 = font2.render("GAME OVER", True, (0, 255, 0))
    text2_x = width // 2 - text2.get_width() // 2
    text2_y = height // 2 - text2.get_height() // 2
    text2_w = text2.get_width()
    text2_h = text2.get_height()
    font3 = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 20)
    anykey = font3.render("PRESS ANY KEY", True, (255, 0, 0))
    anykey_x = width // 2 - text.get_width() // 2 - 25
    anykey_y = height // 2 - text.get_height() // 2 + 150
    anykey_w = text.get_width()
    anykey_h = text.get_height()
    sounds['gameover'].play()
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text2_x, text2_y))
    pygame.display.flip()
    end = True
    pygame.time.delay(3000)
    anykeydraw = 1
    timeconst = pygame.USEREVENT + 1
    pygame.time.set_timer(timeconst, 1000)
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                return
            if event.type == timeconst:
                anykeydraw = abs(anykeydraw - 1)
        screen.fill((0, 0, 0))
        if anykeydraw:
            sounds['anykey'].play()
            screen.blit(anykey, (anykey_x, anykey_y))
        screen.blit(text, (text_x, text_y))
        screen.blit(text2, (text2_x, text2_y))
        pygame.display.flip()


startscreen()
sounds['level'].play()
# highscore
file = open(os.path.join('data', 'highscore.txt'))
highscore = file.readline()
file.close()
font = pygame.font.Font(os.path.join('data', 'galaga_font.ttf'), 10)
text = font.render("HIGHSCORE: {}".format(highscore), True, (255, 255, 255))
text_x = 0
text_y = 0
text_w = text.get_width()
text_h = text.get_height()
screen.blit(text, (text_x, text_y))
# score
boomsprites = {1: load_image('boom1.png'), \
               2: load_image('boom2.png'), \
               3: load_image('boom3.png'), \
               4: load_image('boom4.png'), \
               5: load_image('boom5.png')}
# endtexts
missle = []


class Boom:
    def __init__(self, coords):
        self.coords = coords
        self.count = 1
        self.sprite = pygame.sprite.Sprite(all_sprites)
        self.sprite.image = boomsprites[self.count]
        self.sprite.rect = self.coords
    
    def nextboom(self):
        self.sprite.image = boomsprites[self.count]
        self.count += 1


enemies = generate_level()
# for i in range(30):
#     enemies.append(Enemy(1, [100 + i * 10, 200], [lambda x: [x[0] + 15, x[1]], lambda x: [x[0] - 15, x[1]]]))
all_sprites.draw(screen)
pygame.display.flip()
booms = []
running = True
right = False
left = False
end = False
clock = pygame.time.Clock()
animated = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            elif event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_z or event.key == pygame.K_x:
                missle.append(Bullet(kx))
                sounds['fire'].play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
    if end:
        end_screen(50)
        end = False
    if left and kx > 10:
        kx -= 10
    if right and kx + 70 < width:
        kx += 10
    k = 0
    missledel = []
    enemiesdel = []
    for i in range(len(missle)):
        for j in range(len(enemies)):
            if missle[i].coords[0] - enemies[j].coords[0] >= -10 and \
               missle[i].coords[0] - enemies[j].coords[0] <= 45 and \
               missle[i].coords[1] <= enemies[j].coords[1] + 50 and \
               missle[i].coords[1] >= enemies[j].coords[1]:
                if i not in missledel:
                    missledel.append(i)
                if j not in enemiesdel:
                    enemiesdel.append(j)
                break
    boomdel = []
    for i in range(len(booms)):
        if booms[i].count == 6:
            boomdel.append(i)
            continue
        booms[i].nextboom()
    for i in range(len(boomdel)):
        booms[boomdel[i] - i].sprite.kill()
        del booms[boomdel[i] - i]
    for i in range(len(missledel)):
        missle[missledel[i] - i].sprite.kill()
        del missle[missledel[i] - i]
    for i in range(len(enemiesdel)):
        booms.append(Boom(enemies[enemiesdel[i] - i].coords))
        enemies[enemiesdel[i] - i].sprite.kill()
        del enemies[enemiesdel[i] - i]
    for i in range(len(missle)):
        missle[i - k].move()
        if missle[i - k].coords[1] <= 0:
            missle[i - k].sprite.kill()
            del missle[i - k]
            k += 1
    for i in enemies:
        i.move()
        if i.coords[1] >= height - 50:
            i.coords[1] = height - 60
            i.newfunc()
        if i.coords[1] <= 0:
            i.coords[1] = 10
            i.newfunc()
        if i.coords[0] <= 0:
            i.coords[0] = 10
            i.newfunc()
        if i.coords[0] >= width - 50:
            i.coords[0] = width - 60
            i.newfunc()
    animated += 1
    if animated == 10:
        animated = 0
        for i in enemies:
            i.newsprite()
    player.rect.topleft = (kx, ky)
    screen.fill(pygame.Color('black'))
    all_sprites.draw(screen)
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    clock.tick(30)
pygame.quit()    