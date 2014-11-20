World-Defender-project
======================

Projekti koodirepositoorium/MTAT.03.100

======================

import pygame

black = (   0,   0,   0)
white = ( 255, 255, 255)
red = ( 255,   0,   0)

width  = 800
height = 600


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    walls = None

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('alien.png')

        self.rect = self.image.get_rect()
        self.rect.y = 520
        self.rect.x = 380

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x



pygame.init()

screen = pygame.display.set_mode([width, height])

pygame.display.set_caption('World Defender')

all_sprite_list = pygame.sprite.Group()

wall_list = pygame.sprite.Group()

wall = Wall(0, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(790, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 590, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)



player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
       
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(5, 0)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-5, 0)
    

    all_sprite_list.update()
    screen.fill(black)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
