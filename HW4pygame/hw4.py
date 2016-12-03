import pygame
import random

width = 800
height = 600
size = (width, height)

black = (0,0,0)
white = (255, 255, 255)

pygame.init()
pygame.mixer.init() 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Emoji Fight")

shooting_sound = pygame.mixer.Sound("laser.wav")
gameover = pygame.mixer.Sound("gameover.wav")
explosion = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.set_volume(1) 

font_name = pygame.font.match_font('Arial')


class Cat(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cat.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 30 
        self.rect.centerx = width/2
        self.rect.bottom = height-10 
        self.shooting_wait = 250
        self.last_shot = pygame.time.get_ticks() 

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5 #change to speed up
        if keys[pygame.K_RIGHT]:
            self.speedx = 5 #change to speed up
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > width: #creating a wall so that our right coord. does not get bigger than width
            self.rect.right = width
        if self.rect.left < 0: #coordinate-based screen
            self.rect.left = 0 #constraining player movement to screen

    def shoot(self):
        current = pygame.time.get_ticks()
        if current - self.last_shot > self.shooting_wait: #speeding up shooting delay time
            self.last_shot = current
            laser = Laser(self.rect.centerx, self.rect.top) #bottom of bullet at top of the player
            all_sprites.add(laser) #add to group
            lasers.add(laser)
            shooting_sound.play() #adding sound to shoot
            shooting_sound.set_volume(.6) #adjusting sound to play at 60% full volume

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image = pygame.image.load("alien.bmp").convert_alpha()
        self.rect = self.image.get_rect() 
        self.radius = int(self.rect.width*.9/2)
        self.rect.x = random.randrange(0, width - self.rect.width) #will alwas appear between left and right
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10) #random assignment of speed
  

    def update(self):
        self.rect.y += self.speedy 
        if self.rect.top > height + 10:
            self.rect.x = random.randrange(0, width - self.rect.width) #will alwas appear between left and right
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

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

def text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) #created font object
    text_on = font.render(text, True, white) #surface for writing for pixels, True is set so we can use an anti-aliased font which is cleaner (adds grey pixels)
    text_rect = text_on.get_rect() #surface for rect
    text_rect.midtop = (x, y) #positioning score and lives as found from python documentation
    surf.blit(text_on, text_rect) 

all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
lasers = pygame.sprite.Group()
player = Cat()
all_sprites.add(player) #add any sprite we create so it gets animated and drawn
for i in range(10):
    a = Alien() #make a mob
    all_sprites.add(a) #add it to the new groups
    aliens.add(a)

score = 0
lives = 5


#game loop
runs = True
while runs:
    #clock.tick(FPS) #process input, handle updates, draw on the screen should meet FPS
    #process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = False #game loop ends

    #handle updates
    all_sprites.update()

    #check to see if laser hits a fruit
    hits = pygame.sprite.groupcollide(aliens, lasers, True, True) #if a bullet hits a fruit, both will be deleted
    for hit in hits:
        score = score + 10 
        a = Alien() #create new fruits
        all_sprites.add(a)
        aliens.add(a) #always have 10 fruits because they will be created at the rate they are deleted
        #player.lives -= 1

    
    hits = pygame.sprite.spritecollide(player, aliens, True, pygame.sprite.collide_circle) #mobs are now removed when they hit the player
    if hits:
        explosion.play()
        explosion.set_volume(.7)
        lives -= 1
        if not lives:
            gameover.play(0) #sound added when laser hits fruit target
            gameover.set_volume(.7) #adjusting collision sound
            runs = False

    
    screen.fill(black)
    all_sprites.draw(screen)
    text(screen, "Score: " + str(score), 36, width/2, 10)
    text(screen, "Lives: " + str(lives), 36, width/12, 10) 
    pygame.display.flip() 

while not runs:
    all_sprites = pygame.sprite.Group()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        screen.fill(black)
        all_sprites.draw(screen)
        text(screen, "Game Over :/ ", 36, width/2, height/2)
        pygame.display.flip()

pygame.quit()


