#Imports
import pygame, sys
from pygame.locals import *
import random, time
#Initializing 
pygame.init()
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

pygame.mixer.Sound('background.wav').play(-1)


#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = random.randint(1, 5)
SCORE = 0
SCORE1 = 0
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("GAME OVER", True, WHITE)
 
background = pygame.image.load('AnimatedStreet.png')
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40), 0))
 
      def move(self):

        global SCORE
        global SPEED
        self.rect.move_ip(0, SPEED)

        if (self.rect.top > 600):
            SCORE += 1
            SPEED = random.randint(1, 5)
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

class coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("coin.png")
        self.surf = pygame.Surface((20, 20))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40), 0))

    def move(self):
        self.rect.move_ip(0, 4)

        if (self.rect.top > 600):
            self.surf = pygame.Surface((24, 27))
            self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40), 0))
    
    def eat(self):
        C1.kill()
        self.surf = pygame.Surface((24, 27))
        self.rect = self.surf.get_rect(center = (random.randint(40,SCREEN_WIDTH-40), 0))

C1 = coin()
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
    
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.4
          
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    scores1 = font_small.render(str(SCORE1), True, BLACK)
    DISPLAYSURF.blit(scores1, (360,10))
    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(P1, coins):
        SCORE1 += 1
        C1.eat()
        all_sprites.add(C1)
        coins.add(C1)

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(BLACK)
          DISPLAYSURF.blit(game_over, (20,250))
           
          pygame.display.update()

          for entity in all_sprites:
                entity.kill() 
        
          time.sleep(2)
          pygame.quit()
          sys.exit()        
    
    pygame.display.update()
    FramePerSec.tick(FPS)