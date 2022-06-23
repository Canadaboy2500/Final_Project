import pygame
from os import path
import random
import player1 as p
import objects1 as o
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

def convert_list(images_name, list_name):
    for img in images_name:
        list_name.append(pygame.image.load(path.join(img_dir, img)).convert())

class Meteor(pygame.sprite.Sprite): #all meteors
    def __init__(self, image_list, kind, center, rock):
        super().__init__()
        self.image_orig = random.choice(image_list)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.90 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.health = self.rect.width / 2
        self.last_update = pygame.time.get_ticks()
        self.kind = kind
        self.rock = rock
        if rock == True:
            self.health *= 2
        if kind == 'normal':
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
        elif kind == 'mini':
            self.rect.center = center
            
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -125 or self.rect.right > WIDTH + 125:
            if self.kind == 'normal':
                self.kill()
                new_meteor('lrg', 'normal', [0, 0])
            elif self.kind == 'mini':
                self.kill()
                
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
def new_meteor(image_list, kind, center):
    i = random.random()
    if i >= 0.9:
        rock = True
        if image_list == 'lrg':
            image_list = meteors_rock_lrg
        elif image_list == 'med':
            image_list = meteors_rock_med
        else:
            image_list = meteors_rock_sml
    else:
        rock = False
        if image_list == 'lrg':
            image_list = meteors_dirt_lrg
        elif image_list == 'med':
            image_list = meteors_dirt_med
        else:
            image_list = meteors_dirt_sml
    mob = Meteor(image_list, kind, center, rock)
    all_sprites.add(mob)
    mobs.add(mob)
    
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

meteors_rock_lrg = []
meteors_rock_med = []
meteors_rock_sml = []
meteors_dirt_lrg = []
meteors_dirt_med = []
meteors_dirt_sml = []
meteors_rock_lrg_images = ['meteor_rock0.png', 'meteor_rock1.png', 'meteor_rock2.png', 'meteor_rock3.png',\
                           'meteor_rock4.png', 'meteor_rock5.png',\
                           'meteor_rock6.png', 'meteor_rock7.png', 'meteor_rock8.png', 'meteor_rock9.png']
meteors_dirt_lrg_images = ['meteor_dirt0.png', 'meteor_dirt1.png', 'meteor_dirt2.png', 'meteor_dirt3.png',\
                           'meteor_dirt4.png', 'meteor_dirt5.png',\
                           'meteor_dirt6.png', 'meteor_dirt7.png', 'meteor_dirt8.png', 'meteor_dirt9.png']
meteors_rock_med_images = ['meteor_rock4.png', 'meteor_rock5.png']
meteors_dirt_med_images = ['meteor_dirt4.png', 'meteor_dirt5.png']
meteors_rock_sml_images = ['meteor_rock0.png', 'meteor_rock1.png', 'meteor_rock2.png', 'meteor_rock3.png']
meteors_dirt_sml_images = ['meteor_dirt0.png', 'meteor_dirt1.png', 'meteor_dirt2.png', 'meteor_dirt3.png']
convert_list(meteors_dirt_lrg_images, meteors_dirt_lrg)
convert_list(meteors_dirt_med_images, meteors_dirt_med)
convert_list(meteors_dirt_sml_images, meteors_dirt_sml)
convert_list(meteors_rock_lrg_images, meteors_rock_lrg)
convert_list(meteors_rock_med_images, meteors_rock_med)
convert_list(meteors_rock_sml_images, meteors_rock_sml)



