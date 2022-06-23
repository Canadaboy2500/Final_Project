import pygame
from os import path
import random
import objects3 as o
import player3 as p
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


class Meteor(pygame.sprite.Sprite): #all meteors
    def __init__(self, image_list, center, lvl, origin, health_mult, dmg_mult):
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
        self.health = self.rect.width / 2 * health_mult
        self.last_update = pygame.time.get_ticks()
        self.kind = 'meteor'
        self.lvl = lvl
        self.health *= lvl
        self.origin = origin
        self.dmg = self.health * dmg_mult
        if self.origin == 'normal':
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
        elif self.origin == 'mini':
            self.rect.center = center
            
    def update(self, health_mult, dmg_mult, rock_mult):
        self.dmg = self.health
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -125 or self.rect.right > WIDTH + 125:
            if self.origin == 'normal':
                self.kill()
                new_meteor('lrg', [0, 0], 'normal', health_mult, dmg_mult, rock_mult)
                all_sprites.remove(self)
                meteors.remove(self)
            elif self.origin == 'mini':
                self.kill()
                all_sprites.remove(self)
                meteors.remove(self)
                
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
            
def new_meteor(image_list, center, origin, health_mult, dmg_mult, rock_mult):
    i = random.random()
    if i >= 0.9 - rock_mult:
        lvl = 2
        if image_list == 'lrg':
            image_list = meteors_rock_lrg
        elif image_list == 'med':
            image_list = meteors_rock_med
        else:
            image_list = meteors_rock_sml
    else:
        lvl = 1
        if image_list == 'lrg':
            image_list = meteors_dirt_lrg
        elif image_list == 'med':
            image_list = meteors_dirt_med
        else:
            image_list = meteors_dirt_sml
    mob = Meteor(image_list, center, lvl, origin, health_mult, dmg_mult)
    all_sprites.add(mob)
    meteors.add(mob)
    
def new_alien(kind, health_mult, dmg_mult):
    if kind == 0:
        alien = Alien(random.randrange(1, 6), health_mult, dmg_mult)
    else:
        alien = Alien(kind, health_mult, dmg_mult)
    all_sprites.add(alien)
    aliens.add(alien)
                       
def new_boss(kind, health_mult, dmg_mult):
    boss = Boss(kind, health_mult, dmg_mult)
    all_sprites.add(boss)
    aliens.add(boss)

class Alien(pygame.sprite.Sprite):
    def __init__(self, kind, health_mult, dmg_mult):
        super().__init__()
        if kind == 1: #Regular
            self.dmg = 10 * dmg_mult
            self.health = 200 * health_mult
            if self.health < 300:
                lvl = 0
            elif self.health > 500:
                lvl = 3
            else:
                lvl = 2
            #print(lvl)
            self.image = aliens_regular[lvl]
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (46.5, 42))
            self.rect = self.image.get_rect()
            self.rect.y = random.randrange(100, 200)
            self.speedy = 0
            self.speed_rangex = [200, 300]
            self.kind = 'heavy_bullets'
            self.shot_delay = 500
            self.bullet_speed = 8
        elif kind== 2: #Tank
            self.dmg = 5 * dmg_mult
            self.health = 400 * health_mult
            if self.health < 650:
                lvl = 0
            elif self.health > 1000:
                lvl = 3
            else:
                lvl = 2
            #print(lvl)
            self.image = aliens_tank[lvl]
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (46.5, 42))
            self.rect = self.image.get_rect()
            self.rect.y = random.randrange(200, 250)
            self.speedy = 0
            self.speed_rangex = [100, 150]
            self.kind = 'light_bullets'
            self.shot_delay = 675
            self.bullet_speed = 5
        elif kind == 3: #DPS
            self.dmg = 15 * dmg_mult
            self.health = 250 * health_mult
            if self.health < 325:
                lvl = 0
            elif self.health > 500:
                lvl = 3
            else:
                lvl = 2
            #print(lvl)
            self.image = (aliens_dps[lvl])
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (46.5, 42))
            self.rect = self.image.get_rect()
            self.rect.y = random.randrange(150, 200)
            self.health = 100 * health_mult
            self.speedy = 0
            self.speed_rangex = [200, 250]
            self.kind = 'heavy_bullets'
            self.shot_delay = 500
            self.dmg = 10 * dmg_mult
            self.bullet_speed = 8
        elif kind == 4: #Speed
            self.dmg = 7 * dmg_mult
            self.health = 150 * health_mult
            if self.health < 225:
                lvl = 0
            elif self.health > 350:
                lvl = 3
            else:
                lvl = 2
            #print(lvl)
            self.image = (aliens_speed[lvl])
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (46.5, 42))
            self.rect = self.image.get_rect()
            self.rect.y = random.randrange(200, 225)
            self.health = 100 * health_mult
            self.speedy = 0
            self.speed_rangex = [250, 350]
            self.kind = 'light_bullets'
            self.shot_delay = 350
            self.dmg = 10 * dmg_mult
            self.bullet_speed = 10
        elif kind == 5: #Missile
            self.dmg = 50 * dmg_mult
            self.health = 100 * health_mult
            if self.health < 150:
                lvl = 0
            elif self.health > 250:
                lvl = 3
            else:
                lvl = 2
            #print(lvl)
            self.image = (aliens_missile[lvl])
            self.image.set_colorkey(BLACK)
            self.image = pygame.transform.scale(self.image, (46.5, 42))
            self.rect = self.image.get_rect()
            self.rect.y = 100
            self.health = 100 * health_mult
            self.speed_rangex = [150, 250]
            self.speedy = 0
            self.kind = 'light_missiles'
            self.shot_delay = 1250
            self.dmg = 50 * dmg_mult
            self.bullet_speed = 3
        self.rect.x = random.choice([-50, WIDTH + 50])
        self.speedx = 0
        self.last_shot = pygame.time.get_ticks()
    def update(self, health_mult, dmg_mult, rock_mult):
        now = pygame.time.get_ticks()
        if self.rect.left <= -50:
            self.speedx = random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
        elif self.rect.right >= WIDTH + 50:
            self.speedx = -random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            bullet = o.Bullet(self.rect.centerx, self.rect.bottom + 20, self.bullet_speed, self.dmg, self.kind)
            ai_bullets.add(bullet)
            self.last_shot = pygame.time.get_ticks()
            
class Boss(pygame.sprite.Sprite):
    def __init__(self, kind, health_mult, dmg_mult):
        super().__init__()
        self.image = bosses[kind]
        self.image.set_colorkey(BLACK)
        self.kind = kind
        self.last_shot = 0
        self.last_missile = 0
        self.last_laser = 0
        self.last_summon = 0
        self.last_xchange = 0
        self.last_burst = 0
        if kind == 0:#dps
            self.image = pygame.transform.scale(self.image, (91, 78))
            self.rect = self.image.get_rect()
            self.health = 650 * health_mult
            self.bullet_dmg = 20 * dmg_mult
            self.bullet_speed = 15
            self.speed_rangex = [200, 400]
            self.speed_rangey = [100, 200]
            self.rangey = [0, 200]
            self.shot_delay = 75
            self.burst_delay = 2250
            self.burst = 3
            self.burst_max = 3
            self.xchange_delay = 1000
            self.kind_bullets = 'heavy_bullets'
        elif kind == 1:#speed
            self.image = pygame.transform.scale(self.image, (90, 56))
            self.rect = self.image.get_rect()
            self.health = 400 * health_mult
            self.bullet_dmg = 5 * dmg_mult
            self.bullet_speed = 25
            self.speed_rangex = [500, 600]
            self.speed_rangey = [300, 400]
            self.rangey = [-20, 350]
            self.shot_delay = 125
            self.burst_delay = 1500
            self.burst = 5
            self.burst_max = 5
            self.xchange_delay = 750
            self.kind_bullets = 'light_bullets'
        elif kind == 2:#laser
            self.image = pygame.transform.scale(self.image, (93, 147))
            self.rect = self.image.get_rect()
            self.health = 750 * health_mult
            self.laser_dmg = 2.5 * dmg_mult
            self.speed_rangex = [100, 200]
            self.speed_rangey = [1, 2]
            self.rangey = [0,150]
            self.laser_delay = 5000
            self.xchange_delay = 200
            self.laser_life = 2000
            self.kind_lasers = 'laser'
        elif kind == 3:#missile
            self.image = pygame.transform.scale(self.image, (88, 84))
            self.rect = self.image.get_rect()
            self.health = 750 * health_mult
            self.missile_dmg = 80 * dmg_mult
            self.missile_speed = 5
            self.speed_rangex = [200, 400]
            self.speed_rangey = [100, 200]
            self.rangey = [-10, 150]
            self.missile_delay = 2000
            self.xchange_delay = 1000
            self.kind_missiles = 'heavy_missiles'
        elif kind == 4:#summoner
            self.image = pygame.transform.scale(self.image, (147, 129))
            self.rect = self.image.get_rect()
            self.health = 1500 * health_mult
            self.health_max = self.health
            self.bullet_dmg = 15 * dmg_mult
            self.burst = 4
            self.burst_max = 4
            self.laser_dmg = 2 * dmg_mult
            self.missile_dmg = 80 * dmg_mult
            self.speed_rangex = [150, 250]
            self.speed_rangey = [100, 150]
            self.rangey = [-10, 225]
            self.shot_delay = 150
            self.summon_delay = 20000
            self.laser_delay = 6000
            self.missile_delay = 5000
            self.burst_delay = 2500
            self.xchange_delay = 3000
            self.bullet_speed = 12
            self.missile_speed = 3
            self.laser_life = 2500
            self.kind_bullets = 'heavy_bullets'
            self.kind_missiles = 'heavy_missiles'
            self.kind_lasers = 'laser'
        self.speedy = random.randrange(self.speed_rangey[0], self.speed_rangey[1])/100
        self.speedx = random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
        self.rect.x = random.choice([-150, WIDTH + 150])
        print(self.rect.width, self.rect.height)
        self.rect.y = 50
    def update(self, health_mult, dmg_mult, rock_mult):
        now = pygame.time.get_ticks()
        if self.rect.left <= -50:
            self.speedx = random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
            self.last_changex = pygame.time.get_ticks()
        elif self.rect.right >= WIDTH + 50:
            self.speedx = -random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
            self.last_changex = pygame.time.get_ticks()
        if self.rect.top <= self.rangey[0]:
            self.speedy = random.randrange(self.speed_rangey[0], self.speed_rangey[1])/100
        elif self.rect.bottom >= self.rangey[1]:
            self.speedy = -random.randrange(self.speed_rangey[0], self.speed_rangey[1])/100
        if now - self.last_xchange >= self.xchange_delay:
            if p.player.rect.center > self.rect.center:
                self.speedx = random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
            elif p.player.rect.center < self.rect.center:
                self.speedx = -random.randrange(self.speed_rangex[0], self.speed_rangex[1])/100
            self.last_xchange = now
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.kind == 0 or self.kind == 1 or self.kind == 4:
            if now - self.last_burst > self.burst_delay:
                self.burst = True
                self.burst = 0
                self.last_burst = now
            if self.burst < self.burst_max:
                if now - self.last_shot > self.shot_delay:
                    self.burst += 1
                    bullet = o.Bullet(self.rect.centerx - 25, self.rect.bottom + 10, self.bullet_speed, self.bullet_dmg, self.kind_bullets)
                    ai_bullets.add(bullet)
                    bullet = o.Bullet(self.rect.centerx + 25, self.rect.bottom + 10, self.bullet_speed, self.bullet_dmg, self.kind_bullets)
                    ai_bullets.add(bullet)
                    self.last_shot = now
    
        if self.kind == 2 or self.kind == 4:
            if now - self.last_laser > self.laser_delay:
                laser = o.Laser(self, self.laser_life, 'ai', self.laser_dmg)
                ai_lasers.add(laser)
                self.last_laser = now
        if self.kind == 3 or self.kind == 4:
            if now - self.last_missile > self.missile_delay:
                bullet = o.Bullet(self.rect.centerx, self.rect.bottom - 15, self.missile_speed, self.missile_dmg, self.kind_missiles)
                ai_bullets.add(bullet)
                self.last_missile = now
        if self.kind == 4:
            if now - self.last_summon > self.summon_delay:
                kind = random.randint(1, 5)
                alien = Alien(kind, health_mult, dmg_mult)
                all_sprites.add(alien)
                aliens.add(alien)
                self.last_summon = now
            if self.health <= self.health_max/2:
                self.burst_max = 6
                self.burst_delay = 1500
                self.shot_delay = 100
                self.missile_delay = 2500
            
        
     
def convert_list(images_name, list_name):
    for img in images_name:
        list_name.append(pygame.image.load(path.join(img_dir, 'enemies', img)).convert())
        
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
meteors = pygame.sprite.Group()
aliens = pygame.sprite.Group()
ai_bullets = pygame.sprite.Group()
ai_lasers = pygame.sprite.Group()
powerups = pygame.sprite.Group()


meteors_rock_lrg = []
meteors_rock_med = []
meteors_rock_sml = []
meteors_dirt_lrg = []
meteors_dirt_med = []
meteors_dirt_sml = []
aliens_regular = []
aliens_tank = []
aliens_dps = []
aliens_speed = []
aliens_missile = []
bosses = []
bosses_images = ['boss_rapid_fire.png', 'boss_speed.png',  'boss_laser.png', 'boss_missile.png', 'boss_summoner.png']
alien_regular_images = ['regular_lvl1.png', 'regular_lvl2.png', 'regular_lvl3.png', 'regular_lvl4.png']
alien_tank_images = ['tank_lvl1.png', 'tank_lvl2.png', 'tank_lvl3.png', 'tank_lvl4.png']
alien_dps_images = ['dps_lvl1.png', 'dps_lvl2.png', 'dps_lvl3.png', 'dps_lvl4.png']
alien_speed_images = ['speed_lvl1.png', 'speed_lvl2.png', 'speed_lvl3.png', 'speed_lvl4.png']
alien_missile_images = ['missile_lvl1.png', 'missile_lvl2.png', 'missile_lvl3.png', 'missile_lvl4.png']
convert_list(alien_regular_images, aliens_regular)
convert_list(alien_tank_images, aliens_tank)
convert_list(alien_dps_images, aliens_dps)
convert_list(alien_speed_images, aliens_speed)
convert_list(alien_missile_images, aliens_missile)
convert_list(bosses_images, bosses)
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



