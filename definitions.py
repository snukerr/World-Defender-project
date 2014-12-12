from pygame.locals import *
import pygame

# Värvid
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
BLACK     = (  0,   0,   0)


# Mängija
PLAYERWIDTH = 40
PLAYERHEIGHT = 10
PLAYERSPEED = 5
PLAYERCOLOR = GREEN

# Ekraan
GAMETITLE = 'World Defender'
DISPLAYWIDTH = 900
DISPLAYHEIGHT = 500
BGCOLOR = BLACK
XMARGIN = 50
YMARGIN = 50

# Laskemoon
BULLETWIDTH = 5
BULLETHEIGHT = 5
BULLETOFFSET = 700

# Vaenlane
ENEMYWIDTH = 25
ENEMYHEIGHT = 25
ENEMYGAP = 20
ARRAYWIDTH = 12
ARRAYHEIGHT = 4
MOVETIME = 700
MOVEX = 10
MOVEY = ENEMYHEIGHT
TIMEOFFSET = 100
WHATLEVEL = 2  #Leveli nr, vajadusel muuta

# Kontrollklahvid
DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}


### Mängu elemendid ###

# Mängija
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = pygame.image.load('alien.png')
        self.color = PLAYERCOLOR
        self.rect = self.image.get_rect()
        self.speed = PLAYERSPEED
        self.vectorx = 0

    
    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += DIRECT_DICT[key] * self.speed
                
        self.checkForSide()
        


    def checkForSide(self):
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
            self.vectorx = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vectorx = 0


# Vaenlase laskemoon
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, rect, color, vectory, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLETWIDTH
        self.height = BULLETHEIGHT
        self.color = color
        self.image = pygame.image.load('enemybomb.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = rect.bottom
        self.vectory = vectory
        self.speed = speed
    

    def update(self, *args):
        self.oldLocation = (self.rect.x, self.rect.y)
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0:
            self.kill()

        elif self.rect.bottom > 500:
            self.kill()

# Mängija laskemoon
class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, color, vectory, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLETWIDTH
        self.height = BULLETHEIGHT
        self.color = color
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = rect.bottom
        self.vectory = vectory
        self.speed = speed
    

    def update(self, *args):
        self.oldLocation = (self.rect.x, self.rect.y)
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0:
            self.kill()

        elif self.rect.bottom > 500:
            self.kill()

        
# Vaenlane
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = ENEMYWIDTH
        self.height = ENEMYHEIGHT
        self.row = row
        self.column = column
        self.image = self.setImage()
        self.rect = self.image.get_rect()
        self.name = 'enemy'
        self.vectorx = 1
        self.level = WHATLEVEL
        self.moveNumber = 0
        self.moveTime = MOVETIME
        self.timeOffset = row * TIMEOFFSET
        self.timer = pygame.time.get_ticks() - self.timeOffset
        if self.level == 1:
            self.moveTime = MOVETIME
        elif self.level == 2:
            self.moveTime = MOVETIME - 60
        elif self.level == 3:
            self.moveTime = MOVETIME - 120
        elif self.level == 4:
            self.moveTime = MOVETIME - 180
        elif self.level == 5:
            self.moveTime = MOVETIME - 240
        elif self.level == 6:
            self.moveTime = MOVETIME - 300
        elif self.level == 7:
            self.moveTime = MOVETIME - 360
        elif self.level == 8:
            self.moveTime = MOVETIME - 420
        elif self.level == 9:
            self.moveTime = MOVETIME - 480
        elif self.level == 10:
            self.moveTime = MOVETIME - 540


    def update(self, keys, currentTime):
        if currentTime - self.timer > self.moveTime:
            if self.moveNumber < 28:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber += 1
            elif self.moveNumber >= 28:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += MOVEY
                if self.moveTime > 100:
                    self.moveTime -= 5
            self.timer = currentTime


    def setImage(self):
        if self.row == 0:
            image = pygame.image.load('ufo.png')
        elif self.row == 1:
            image = pygame.image.load('ufo.png')
        elif self.row == 2:
            image = pygame.image.load('ufo.png')
        else:
            image = pygame.image.load('ufo.png')
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image


# Teksti jaoks
class Text(object):
    def __init__(self, font, size, message, color, rect, surface):
        self.font = pygame.font.Font(font, size)
        self.message = message
        self.surface = self.font.render(self.message, True, color)
        self.rect = self.surface.get_rect()
        self.setRect(rect)

    def setRect(self, rect):
        self.rect.centerx, self.rect.centery = rect.centerx, rect.centery - 5


    def draw(self, surface):
        surface.blit(self.surface, self.rect)
