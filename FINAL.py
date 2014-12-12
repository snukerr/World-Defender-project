import pygame
import sys
from random import shuffle
from pygame.locals import *
from definitions import *


### Mäng ###
class App(object):
    
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.gameStart = True
        self.gameOver = False
        self.beginGame = False
        self.score = 0
        self.score2 = 0
        self.lifes = 3
        self.game_font = pygame.font.Font("orange juice 2.0.ttf", 20)
        self.game_font2 = pygame.font.Font("orange juice 2.0.ttf", 60)
        
    def refresh_scores(self):
        self.displaySurf.blit(self.game_font.render(
            "SCORE: " + str(self.score), 1, WHITE), (780, 27))

    def refresh_scores2(self):
        self.displaySurf.blit(self.game_font2.render(
            "Your Score: " + str(self.score2), 1, WHITE), (280, 297))

    def refresh_lifes(self):
        self.displaySurf.blit(self.game_font.render(
            "LIFES: " + str(self.lifes), 1, WHITE), (781, 7))


    def refresh_screen(self):
        self.refresh_scores()
        self.refresh_lifes()

    def refresh_screen2(self):
        self.refresh_scores2()

    def resetGame(self):
        self.gameStart = True
        self.needToMakeEnemies = True
        pygame.display.update()
        
        self.introMessage1 = Text('orange juice 2.0.ttf', 110,
                                 'WORLD DEFENDER!',
                                 ORANGE, self.displayRect,
                                 self.displaySurf)
        self.introMessage2 = Text('orange juice 2.0.ttf', 45,
                                  'Press "S" to Start Game',
                                  WHITE, self.displayRect,
                                  self.displaySurf)
        self.introMessage3 = Text('orange juice 2.0.ttf', 45,
                                  'Press "ESC" to Exit Game',
                                  WHITE, self.displayRect,
                                  self.displaySurf)
        
        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 9
        self.introMessage3.rect.top = self.introMessage2.rect.bottom + 9

        self.gameOverMessage1 = Text('orange juice 2.0.ttf', 130,
                                    'GAME OVER!', RED,
                                    self.displayRect, self.displaySurf)

        self.gameOverMessage2 = Text('orange juice 2.0.ttf', 130,
                                    'YOU WIN!', GREEN,
                                    self.displayRect, self.displaySurf)

        self.gameOverMessage3 = Text('orange juice 2.0.ttf', 35,
                                    'Press "M" to Main Menu', WHITE,
                                    self.displayRect, self.displaySurf)

        self.gameOverMessage3.rect.top = self.gameOverMessage1.rect.bottom + 58
        
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.greenBullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group(self.player)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.enemyMoves = 0
        self.enemyBulletTimer = pygame.time.get_ticks()
        self.gameOver = False
        self.gameOverTime = pygame.time.get_ticks()
        pygame.display.update()
        


    def checkForEnemyBullets(self):
        redBulletsGroup = pygame.sprite.Group()

        for bullet in self.bullets:
            if bullet.color == RED:
                redBulletsGroup.add(bullet)

        for bullet in redBulletsGroup:
            if pygame.sprite.collide_rect(bullet, self.player):
                if self.player.color == GREEN:
                    self.player.color = YELLOW
                    self.player.image = pygame.image.load('alienhit.png')
                    self.lifes -= 1
                elif self.player.color == YELLOW:
                    self.player.color = RED
                    self.player.image = pygame.image.load('aliendead.png')
                    self.lifes -= 1
                elif self.player.color == RED:
                    self.gameOver = True
                    self.gameOverTime = pygame.time.get_ticks()
                bullet.kill()



    def shootEnemyBullet(self, rect):
        if (pygame.time.get_ticks() - self.enemyBulletTimer) > BULLETOFFSET:
            self.bullets.add(Enemy_bullet(rect, RED, 1, 5))
            self.allSprites.add(self.bullets)
            self.enemyBulletTimer = pygame.time.get_ticks()



    def findEnemyShooter(self):
        columnList = []
        for enemy in self.enemies:
            columnList.append(enemy.column)

        columnSet = set(columnList)
        columnList = list(columnSet)
        shuffle(columnList)
        column = columnList[0]
        enemyList = []
        rowList = []

        for enemy in self.enemies:
            if enemy.column == column:
                rowList.append(enemy.row)

        row = max(rowList)

        for enemy in self.enemies:
            if enemy.column == column and enemy.row == row:
                self.shooter = enemy 
        
    

    def makeScreen(self):
        pygame.display.set_caption(GAMETITLE)
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect



    def makePlayer(self):
        player = Player()
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player



    def makeEnemies(self):
        enemies = pygame.sprite.Group()
        
        for row in range(ARRAYHEIGHT):
            for column in range(ARRAYWIDTH):
                enemy = Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                enemies.add(enemy)

        return enemies



    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            if event.type == KEYDOWN:
                if event.key == K_SPACE and len(self.greenBullets) < 1:
                    bullet = Bullet(self.player.rect, GREEN, -1, 20)
                    self.greenBullets.add(bullet)
                    self.bullets.add(self.greenBullets)
                    self.allSprites.add(self.bullets)
                elif event.key == K_ESCAPE:
                    self.terminate()


    def gameStartInput(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate()
            elif event.type == KEYUP:
                if event.key == K_s:
                    self.gameOver = False
                    self.gameStart = False
                    self.beginGame = True


    def gameOverInput(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate()
            elif event.type == KEYUP:
                if event.key == K_m:
                    self.gameStart = True
                    self.beginGame = False
                    self.gameOver = False
          


    def checkCollisions(self):
        self.checkForEnemyBullets()
        for hit in pygame.sprite.groupcollide(self.bullets, self.enemies, True, True):
            self.score += 10
            self.score2 += 10

          

    def checkGameOver(self):
        if len(self.enemies) == 0:
            self.gameOver = True
            self.gameStart = False
            self.beginGame = False
            self.gameOverTime = pygame.time.get_ticks()

        else:
            for enemy in self.enemies:
                if enemy.rect.bottom > DISPLAYHEIGHT - 100:
                    self.gameOver = True
                    self.gameStart = False
                    self.beginGame = False
                    self.gameOverTime = pygame.time.get_ticks()
       
        
                

    def terminate(self):
        pygame.quit()
        sys.exit()


    def mainLoop(self):
        while True:
            if self.gameStart:
                self.resetGame()
                self.gameOver = False
                self.displaySurf.fill(BGCOLOR)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.introMessage3.draw(self.displaySurf)
                self.gameStartInput()
                pygame.display.update()
                self.score2 = 0

            elif self.gameOver:
                self.displaySurf.fill(BGCOLOR)
                if len(self.enemies) == 0:
                    self.gameOverMessage2.draw(self.displaySurf)
                else:
                    self.gameOverMessage1.draw(self.displaySurf)
                self.gameOverMessage3.draw(self.displaySurf)
                self.refresh_screen2()
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                if self.gameOver == True:
                    self.score = 0
                    self.lifes = 3
                pygame.display.update()
                
                
            elif self.beginGame:
                if self.needToMakeEnemies:
                    
                    self.enemies = self.makeEnemies()
                    self.allSprites.add(self.enemies)
                    self.needToMakeEnemies = False
                    pygame.event.clear()
                    
                    
                        
                else:    
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(BGCOLOR)
                    self.checkInput()
                    self.refresh_screen()
                    self.allSprites.update(self.keys, currentTime)
                    if len(self.enemies) > 0:
                        self.findEnemyShooter()
                        self.shootEnemyBullet(self.shooter.rect)
                    self.checkCollisions()
                    self.allSprites.draw(self.displaySurf)
                    pygame.display.update()
                    self.checkGameOver()
                    self.clock.tick(self.fps)
                    
            
            
if __name__ == '__main__':
    app = App()
    app.mainLoop()
