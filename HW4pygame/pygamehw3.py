import math
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

pygame.init()
 
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background('stars.bmp', [0,0])

#screen.fill([255, 255, 255])
#screen.blit(BackGround.image, BackGround.rect)      