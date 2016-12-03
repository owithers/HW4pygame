import pygame
import random

width = 800
height = 600
size = (width, height)

black = (0,0,0)
yellow = (255, 255, 0)

pygame.init()
pygame.mixer.init() 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Emoji Fight")

shooting_sound = pygame.mixer.Sound("laser.wav")
gameover = pygame.mixer.Sound("gameover.wav")
explosion = pygame.mixer.Sound("explosion.wav")

default_font = pygame.font.get_default_font()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image = pygame.image.load("alien.bmp").convert_alpha()
        self.rect = self.image.get_rect() 
        self.radius = int(self.rect.width*.9/2)
        self.speedy = random.randrange(3, 10) 
        self.rect.x = random.randrange(0, width - self.rect.width) 
        self.rect.y = random.randrange(-100, -40)
         

    def update(self):
        self.rect.y += self.speedy 
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(0, width - self.rect.width) 
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 10)

class Cat(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cat.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 30 
        self.rect.centerx = width/2
        self.rect.bottom = height-10 
        self.shooting_time = 200
        self.last_shot = pygame.time.get_ticks() 

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5 
        if keys[pygame.K_RIGHT]:
            self.speedx = 5 
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width: 
            self.rect.right = width
        if self.rect.left < 0: 
            self.rect.left = 0 
    def shoot(self):
        time = pygame.time.get_ticks()
        if time - self.last_shot > self.shooting_time: 
            self.last_shot = time
            laser = Laser(self.rect.centerx, self.rect.top) 
            everything.add(laser) 
            lasers.add(laser)
            shooting_sound.play() 
            shooting_sound.set_volume(.8) 

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.image = pygame.Surface((10, 10))
        for i in range(5, 0, -1):
            color = 255.0 * float(i)/5
            pygame.draw.circle(self.image,
                               (0, 0, color),
                               (5, 5),
                               i,
                               0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-25)

    def update(self):
        x, y = self.rect.center
        y -= 20
        self.rect.center = x, y
        if y <= 0:
            self.kill()

def text(surface, text, size, x, y):
    font = pygame.font.Font(default_font, size) 
    text_s = font.render(text, True, yellow) 
    text_rect = text_s.get_rect() 
    text_rect.center = (x, y) 
    surface.blit(text_s, text_rect) 


everything = pygame.sprite.Group()
aliens = pygame.sprite.Group()
lasers = pygame.sprite.Group()
player = Cat()
everything.add(player) 

points = 0
lives = 3

for i in range(20):
    a = Alien() 
    everything.add(a) 
    aliens.add(a)


runs = True
while runs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = False 

    
    everything.update()

    
    hits = pygame.sprite.groupcollide(aliens, lasers, True, True)
    for hit in hits:
        points = points + 5 
        a = Alien() 
        aliens.add(a) 
    if points >= 50:
        runs = False
        screen.fill(black)
        everything.draw(screen)
        text(screen, "You win!!", 36, width/2, height/2)
        pygame.display.flip()
        break

    

    hits = pygame.sprite.spritecollide(player, aliens, True, pygame.sprite.collide_circle)
    if hits:
        explosion.play()
        explosion.set_volume(.8)
        lives -= 1
        if not lives:
            gameover.play(0)
            gameover.set_volume(.8) 
            runs = False

    
    screen.fill(black)
    everything.draw(screen)
    text(screen, "Lives Left: " + str(lives), 28, width/2, 10)
    text(screen, "Points: " + str(points), 28, width/12, 10) 
    pygame.display.flip() 

while not runs:
    everything = pygame.sprite.Group()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        screen.fill(black)
        everything.draw(screen)
        text(screen, "Game Over", 36, width/2, height/2)
        pygame.display.flip()

pygame.quit()
