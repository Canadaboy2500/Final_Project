import pygame
from os import path
import random
import player1 as p
import mobs1 as m
import effects1 as e
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()
bullet_img.set_colorkey(BLACK)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
class Pow(pygame.sprite.Sprite):
    def __init__(self, image, speed, center):
        super().__init__()
        self.type = image
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            
class Super_Pow(Pow):
    def __init__(self, speed, center):
        image = random.choice(super_powerup_images)
        super().__init__(image, speed, center)
        

class Basic_Pow(Pow):
    def __init__(self, speed, center):
        image = random.choice(basic_powerup_images)
        super().__init__(image, speed, center)

def convert_dict(images, scale):
    i = 0
    for img in images:
        powerup_images[img] = pygame.image.load(path.join(img_dir, img + '.png')).convert()
        powerup_images[img] = pygame.transform.scale(powerup_images[img], (scale[i]))
        i += 1
        
powerup_images = {}
super_powerup_images = ['pow_invulnerable', 'pow_laser', 'pow_extralife']
super_powerup_scales = [[27,27], [35,20], [25,20]]
basic_powerup_images = ['pow_shield', 'pow_power', 'pow_gun']
basic_powerup_scales = [[20,20], [18,25], [25,25]]
        
convert_dict(basic_powerup_images, basic_powerup_scales)
convert_dict(super_powerup_images, super_powerup_scales)



                    
