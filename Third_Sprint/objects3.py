import pygame
from os import path
import random
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, dmg, kind):
        super().__init__()
        self.kind = kind
        if kind == 'light_bullets':
            if dmg <= 10:
                self.image = light_bullets[0]
            elif dmg >= 20:
                self.image = light_bullets[2]
            else:
                self.image = light_bullets[1]
        if kind == 'heavy_bullets':
            if dmg <= 20:
                self.image = heavy_bullets[0]
            elif dmg >= 40:
                self.image = heavy_bullets[2]
            else:
                self.image = heavy_bullets[1]
        if kind == 'light_missiles':
            if dmg <= 60:
                self.image = light_missiles[0]
            elif dmg >= 100:
                self.image = light_missiles[2]
            else:
                self.image = light_missiles[1]
            self.image = pygame.transform.scale(self.image, (15, 50))
        if kind == 'heavy_missiles':
            if dmg <= 100:
                self.image = heavy_missiles[0]
            elif dmg >= 200:
                self.image = heavy_missiles[2]
            else:
                self.image = heavy_missiles[1]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed
        self.dmg = dmg
        if speed > 0:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.top = y
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
       
class Laser(pygame.sprite.Sprite):
    def __init__(self, owner, life, side, dmg):
        super().__init__()
        dmg = dmg * 0.75
        self.owner = owner
        self.side = side
        if dmg <= 3:
            lvl = 0
        elif dmg >= 6:
            lvl = 2
        else:
            lvl = 1
        self.image = lasers[lvl]
        self.image.set_colorkey(BLACK)
        if self.side == 'ai':
            self.image = pygame.transform.scale(self.image, (20, 700))
        else:
            self.image = pygame.transform.scale(self.image, (20, 400))
        self.rect = self.image.get_rect()
        self.rect.center = [-100, -1000]
        self.life_span = life
        self.dmg = dmg
        self.spawn = pygame.time.get_ticks()
        self.kind = 'laser'
    def update(self):
        if self.side == 'ai':
            self.rect.y = self.owner.rect.centery + 25
            self.rect.x = self.owner.rect.centerx - 10
        elif self.side == 'player':
            self.rect.bottom = self.owner.rect.centery - 25
            self.rect.centerx = self.owner.rect.centerx
        if pygame.time.get_ticks() - self.spawn > self.life_span:
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


def convert_list(images_name, list_name):
    for img in images_name:
        list_name.append(pygame.image.load(path.join(img_dir, 'bullets', img)).convert())




light_bullets = []
heavy_bullets = []
light_missiles = []
heavy_missiles = []
lasers = []
light_bullet_imgs = ['light_lvl1.png', 'light_lvl2.png', 'light_lvl3.png']
heavy_bullet_imgs = ['heavy_lvl1.png', 'heavy_lvl2.png', 'heavy_lvl3.png']
light_missiles_imgs = ['light_missile_lvl1.png', 'light_missile_lvl2.png', 'light_missile_lvl3.png']
heavy_missiles_imgs = ['heavy_missile_lvl1.png', 'heavy_missile_lvl2.png', 'heavy_missile_lvl3.png']
laser_imgs = ['laser_lvl1.png', 'laser_lvl2.png', 'laser_lvl3.png']

convert_list(light_bullet_imgs, light_bullets)
convert_list(heavy_bullet_imgs, heavy_bullets)
convert_list(light_missiles_imgs, light_missiles)
convert_list(heavy_missiles_imgs, heavy_missiles)
convert_list(laser_imgs, lasers)


        
convert_dict(basic_powerup_images, basic_powerup_scales)
convert_dict(super_powerup_images, super_powerup_scales)



                    
