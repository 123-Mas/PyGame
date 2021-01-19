import pygame


import sys
import os
import random


pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Game:
    def __init__(self, width, height, labirint, screen):
        self.screen = screen
        self.width = width
        self.height = height
        self.labirint = labirint
        self.lab = [[0] * 10 for _ in range(10)]
        self.left = 350
        self.top = 50
        self.cell_size = 80
        self.player = (0, 9)
        self.value = 5
        self.surprises()

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def render(self, screen):
        x, y, s = self.left, self.top, self.cell_size
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, (70, 70, 70), (x, y, s, s), 1)
                if self.lab[i][j] == 1:
                    pygame.draw.rect(screen, (80, 80, 80), (x, y, s, s))
                if 'T' in self.labirint[i][j]:
                    pygame.draw.line(screen, (70, 160, 170), (x, y),
                                     (x + s, y), 5)
                if 'L' in self.labirint[i][j]:
                    pygame.draw.line(screen, (70, 160, 170), (x, y),
                                     (x, y + s), 5)
                if 'R' in self.labirint[i][j]:
                    pygame.draw.line(screen, (70, 160, 170), (x + s, y),
                                     (x + s, y + s), 5)
                if 'B' in self. labirint[i][j]:
                    pygame.draw.line(screen, (70, 160, 170), (x, y + s),
                                     (x + s, y + s), 5)
                if (i, j) == self.player:
                    self.lab[i][j] = 1
                    pygame.draw.circle(screen, (128, 0, 0), (x + s // 2, y + s // 2),
                                       s // 2 - 3)
                x += s
            x = self.left
            y += s

    def sprites(self, treasure):
        treasure.rect = treasure.image.get_rect()
        x0 = self.left + self.cell_size * 5
        y0 = self.top + self.cell_size * 4 + 3
        treasure.rect.x = x0
        treasure.rect.y = y0
        return treasure

    def surprises(self):
        for i in range(15):
            x = random.choice(range(10))
            y = random.choice(range(10))
            if x != self.player[0] and y != self.player[1]:
                chance = random.choice([4, -2, -1, 2, -3, 3])
                self.lab[x][y] = chance
            self.lab[4][5] = 10000

    def move(self, direction):
        y, x = self.player[0], self.player[1]
        if direction not in self.labirint[y][x]:
            self.ride(y, x, direction)

    def ride(self, y, x, direction):
        if direction == 'L':
            self.ride_left(y, x)
        if direction == 'R':
            self.ride_right(y, x)
        if direction == 'T':
            self.ride_up(y, x)
        if direction == 'B':
            self.ride_down(y, x)

    def ride_left(self, y, x):
        if self.lab[y][x - 1] != 1:
            if self.value > 0:
                self.open(y, x - 1)
                self.value -= 1
                x -= 1
        else:
            x -= 1
        self.player = y, x

    def ride_right(self, y, x):
        if self.lab[y][x + 1] != 1:
            if self.value > 0:
                self.open(y, x + 1)
                self.value -= 1
                x += 1
        else:
            x += 1
        self.player = y, x

    def ride_up(self, y, x):
        if self.lab[y - 1][x] != 1:
            if self.value > 0:
                self.open(y - 1, x)
                self.value -= 1
                y -= 1
        else:
            y -= 1
        self.player = y, x

    def ride_down(self, y, x):
        if self.lab[y + 1][x] != 1:
            if self.value > 0:
                self.open(y + 1, x)
                self.value -= 1
                y += 1
        else:
            y += 1
        self.player = y, x

    def open(self, y, x):
        if self.lab[y][x] != 0:
            chance = self.lab[y][x]
            self.value += chance
            if self.value < 0:
                self.value = 0
            quest = Question()
            quest.rect.x = self.left + self.cell_size * x + 5
            quest.rect.y = self.top + self.cell_size * y
            self.print_chance(chance, self.screen)

    def get_click(self, mouse_pos):
        x, y = mouse_pos
        if (40 > x or x > 200) or (740 > y or y > 820):
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)
            return None
        if self.value == 0:
            return 'earn'
        return None

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or x > self.left + self.width * self.cell_size:
            return None
        if y < self.top or y > self.top + self.height * self.cell_size:
            return None
        x_num = (x - self.left) // self.cell_size
        y_num = (y - self.top) // self.cell_size
        return x_num, y_num

    def on_click(self, cell):
        if cell:
            x, y = cell
            if self.lab[y][x] == 1:
                self.player = y, x

    def print_value(self, screen):
        font = pygame.font.Font(None, 40)
        text = font.render("Количество ходов:", True, (70, 160, 170))
        text1 = font.render(str(self.value), True, (70, 160, 170))
        text_x = 40
        text_y = 50
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        screen.blit(text1, (text_x, text_y + 50))
        pygame.draw.rect(screen, (70, 160, 170), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 80), 1)

    def print_earning(self, screen):
        font = pygame.font.Font(None, 70)
        text = font.render("Играть", True, (70, 160, 170))
        text_x = 50
        text_y = 750
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (70, 160, 170), (text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20), 1)

    def print_chance(self, chance, screen):
        font = pygame.font.Font(None, 50)
        if chance < 0:
            stroka = str(chance)
        else:
            stroka = '+' + str(chance)
        text = font.render(stroka, True, (70, 160, 170))
        text_x = 50
        text_y = 400
        screen.blit(text, (text_x, text_y))


class Earn():
    def __init__(self):
        self.coords = 600, 450
        self.land = Land()
        self.player = Player()
        for i in range(6):
            self.zont = Umbrella()
        for j in range(3):
            self.black = Black()
        for e in range(2):
            self.super = SuperUmb()

    def update(self):
        self.coords = 600, 450
        for sprite in third_sprites:
            sprite.rect.x = random.choice(range(10, 1100))
            sprite.rect.y = random.choice(range(-1000, -90))

    def render(self):
        for sprite in third_sprites:
            sprite.update()

    def left(self):
        self.player.rect = self.player.rect.move(-30, 0)

    def right(self):
        self.player.rect = self.player.rect.move(30, 0)


class Player(pygame.sprite.Sprite):
    image = load_image("play.png")
    image = pygame.transform.scale(image, (80, 140))

    def __init__(self):
        super().__init__(other_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 550
        self.rect.y = 700


class Black(pygame.sprite.Sprite):
    image = load_image("black2.png")
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self):
        super().__init__(third_sprites)
        self.image = Black.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.choice(range(10, 1100))
        self.rect.y = random.choice(range(-1000, -90))

    def update(self):
        if self.rect.y > 900:
            x = random.choice(range(10, 1190))
            self.rect.x = x
            self.rect.y = random.choice(range(-1000, -90))
        self.rect = self.rect.move(0, 1)
        if pygame.sprite.collide_mask(self, earn.player):
            value = game.get_value() - 1
            game.set_value(value)
            x = random.choice(range(10, 1100))
            self.rect.x = x
            self.rect.y = random.choice(range(-1000, -90))


class Umbrella(pygame.sprite.Sprite):
    image = load_image("zont3.png")
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self):
        super().__init__(third_sprites)
        self.image = Umbrella.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.choice(range(10, 1100))
        self.rect.y = random.choice(range(-1000, -90))

    def update(self):
        if self.rect.y > 900:
            x = random.choice(range(10, 1190))
            self.rect.x = x
            self.rect.y = random.choice(range(-1000, -90))
        self.rect = self.rect.move(0, 1)
        if pygame.sprite.collide_mask(self, earn.player):
            value = game.get_value() + 1
            game.set_value(value)
            x = random.choice(range(10, 1100))
            self.rect.x = x
            self.rect.y = random.choice(range(-1000, -90))


class SuperUmb(pygame.sprite.Sprite):
    image = load_image("zont2.png")
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self):
        super().__init__(third_sprites)
        self.image = SuperUmb.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.choice(range(10, 1100))
        self.rect.y = random.choice(range(-1000, -90))

    def update(self):
        if self.rect.y > 900:
            stop_earning()
        self.rect = self.rect.move(0, 1)
        if pygame.sprite.collide_mask(self, earn.player):
            value = game.get_value() + 3
            game.set_value(value)
            x = random.choice(range(10, 1100))
            self.rect.x = x
            self.rect.y = random.choice(range(-1000, -90))


class Land(pygame.sprite.Sprite):
    image = load_image("land.png")
    image = pygame.transform.scale(image, (1200, 80))

    def __init__(self):
        super().__init__(other_sprites)
        self.image = Land.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Question(pygame.sprite.Sprite):
    image = load_image("comm.png")
    image = pygame.transform.scale(image, (70, 80))

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Question.image
        self.rect = self.image.get_rect()


class Salut(pygame.sprite.Sprite):
    image = load_image("over.jpg")
    image = pygame.transform.scale(image, (1200, 900))

    def __init__(self):
        super().__init__(end_sprites)
        self.image = Salut.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


labirinth = [['TL', 'TR', 'TLB', 'TB', 'T', 'TB', 'TB', 'TB', 'TB', 'TR'],
             ['LR', 'LB', 'TB', 'TR', 'LR', 'TL', 'TB', 'TB', 'TR', 'LR'],
             ['L', 'TR', 'TLR', 'LB', 'RB', 'LB', 'TB', 'TR', 'LBR', 'LR'],
             ['LR', 'LR', 'LB', 'TR', 'TL', 'TB', 'TR', 'LB', 'TB', 'RB'],
             ['LR', 'L', 'TB', 'RB', 'L', 'TR', 'LR', 'TL', 'TR', 'TLR'],
             ['LR', 'LRB', 'TLR', 'TLB', 'R', 'LR', 'LB', 'RB', 'LB', 'R'],
             ['L', 'TB', '', 'TRB', 'LR', 'LR', 'TL', 'TB', 'TB', 'RB'],
             ['LR', 'TLR', 'LRB', 'TL', 'RB', 'LR', 'LB', 'TB', 'TR', 'TLR'],
             ['LB', 'B', 'TB', 'RB', 'TL', 'B', 'TR', 'TLR', 'LRB', 'LR'],
             ['TLB', 'TB', 'TB', 'TB', 'RB', 'TLB', 'B', 'B', 'TB', 'RB']]


def pictures():
    treasure = pygame.sprite.Sprite(all_sprites)
    image = load_image("klad3.jpg")
    image = pygame.transform.scale(image, (78, 77))
    treasure.image = image
    treasure = game.sprites(treasure)
    return treasure


def game_over(screen):
    salut = Salut()
    font = pygame.font.Font(None, 150)
    text = font.render("GAME OVER", True, (160, 0, 0))
    text_x = 300
    text_y = 360
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def stop_earning():
    global earning

    earning = False


if __name__ == '__main__':
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    game = Game(width, height, labirinth, screen)
    all_sprites = pygame.sprite.Group()
    treasure = pictures()
    all_sprites.add(treasure)
    other_sprites = pygame.sprite.Group()
    third_sprites = pygame.sprite.Group()
    end_sprites = pygame.sprite.Group()
    earn = Earn()
    fps = 100
    clock = pygame.time.Clock()
    running = True
    earning = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = game.get_click(event.pos)
                if click == 'earn':
                    earning = True
                    earn.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if earning:
                        earn.left()
                    else:
                        game.move('L')
                elif event.key == pygame.K_RIGHT:
                    if earning:
                        earn.right()
                    else:
                        game.move('R')
                elif event.key == pygame.K_UP:
                    game.move('T')
                elif event.key == pygame.K_DOWN:
                    game.move('B')
                if event.key == pygame.K_BACKSPACE:
                    earning = False
        if not earning:
            screen.fill((0, 0, 0))
            game.print_value(screen)
            game.print_earning(screen)
            game.render(screen)
            all_sprites.draw(screen)
        else:
            screen.fill((255, 255, 255))
            earn.render()
            other_sprites.draw(screen)
            third_sprites.draw(screen)
        if game.get_value() >= 7000:
            screen.fill((0, 0, 0))
            end_sprites.draw(screen)
            game_over(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()