World-Defender-project
======================

Projekti koodirepositoorium/MTAT.03.100

======================

#Arvutis peab olema instaleeritud pygame moodul
#Töötab hiire ja nooleklahvidega
import pygame

# Defineerin värvid
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Loodava akna mõõdud
width  = 800
height = 600

# Mängu täitja 
class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    walls = None

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('alien.png') #Kujutis võetakse failist

        #Stardipositsioon
        self.rect = self.image.get_rect()
        self.rect.y = 520
        self.rect.x = 380

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Liikumine
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

# Seinad, kuhu täitja vastu saab põrgata
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black) # Sama värvi, mis maailm

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# 'Tulistamine'
class Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(red)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 6


# Luuakse maailm
pygame.init()

screen = pygame.display.set_mode([width, height])

pygame.display.set_caption('World Defender')

all_sprite_list = pygame.sprite.Group() #Sprite'd jagatakse listidesse

#Tehakse seinad
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

shoot_list = pygame.sprite.Group()

# Tehakse täitja
player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player) 

# Kasutatakse ekraani framerate'i juures
clock = pygame.time.Clock()

done = False
# Allpool klahvivajutustele reageerimine ja vastavalt liikumine
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            shoot = Shoot()

            shoot.rect.x = player.rect.x + 19 # Objekt asetatakse sinna, kus on täitja
            shoot.rect.y = player.rect.y 
            
            all_sprite_list.add(shoot)
            shoot_list.add(shoot)

    # Peale igakordset mängu 'event'-i uuendatakse andmeid
    all_sprite_list.update()
    for shoot in shoot_list:
        if shoot.rect.y < -10: # Kui lask lendab ekraani piiridest välja, eemaldatakse see vastavast listist
            shoot_list.remove(shoot)
            all_sprite_list.remove(shoot)
            
    screen.fill(black)
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
