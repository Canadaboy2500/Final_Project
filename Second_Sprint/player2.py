import pygame
from os import path
import random
import objects2 as o
import mobs2 as m
import effects2 as e
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

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.wav'))
player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
player_img.set_colorkey(BLACK)
player_img = pygame.transform.scale(player_img, (50,38))
forcefield_img = pygame.image.load(path.join(img_dir, 'forcefield.png')).convert()
forcefield_img.set_colorkey(BLACK)
bullet_img = o.heavy_bullets[0]
bullet_img.set_colorkey(BLACK)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
       # self.image = pygame.transform.scale(player_img, (50,38))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.dmg = 10
        self.last_shot = 0
        self.lives = 3
        self.hide_timer = pygame.time.get_ticks()
        self.power = 0
        self.shields = 0
        self.lasers = 0
        self.power_time = 0
        self.shield_time = 0
        self.laser_time = 0
        self.POWERTIME = 10000
        self.SHIELDTIME = 8000
        self.LASERTIME = 5000
        self.dead = False
        self.respawn = False
        self.old = 0
        self.i = 0
        
    def update(self):
        self.speedx = 0
        if self.dead == False:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            self.rect.x += self.speedx
            if keystate[pygame.K_SPACE]:
                if self.lasers <= 0:
                    self.shoot()
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0 
        if self.dead and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.dead = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            start = pygame.time.get_ticks()
            self.old = 0
            self.i = 0
            self.respawn = True
        if self.respawn == True:
            now = pygame.time.get_ticks()
            if now - self.old >= 200:
                self.rect.bottom = HEIGHT + 100
                self.old = now
                self.i += 1
            elif now - self.old  >= 100:
                self.rect.bottom = HEIGHT - 10
            if self.i == 10:
                self.rect.bottom = HEIGHT - 10
                self.respawn = False
        if self.power >= 1 and pygame.time.get_ticks() - self.power_time > self.POWERTIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            if self.power == 0:
                self.power_time = 0
                player_shield.on = False
        if self.shields >= 1 and pygame.time.get_ticks() - self.shield_time > self.SHIELDTIME:
            self.shields -= 1
            self.shield_time = pygame.time.get_ticks()
            if self.shields == 0:
                player_shield.on = False
                self.shield_time = 0
        if self.lasers >= 1 and pygame.time.get_ticks() - self.laser_time > self.LASERTIME:
            self.lasers -= 1
            self.laser_time = pygame.time.get_ticks()

    def kill_self(self):
        self.dead = True
        player_shield.on = False
        self.lasers = 0
        self.shields = 0
        if self.power >= 1:
            self.power -= 1
        player.rect.center = [-500, -500]
        self.hide_timer = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 0:
                bullet = o.Bullet(self.rect.centerx, self.rect.top, -10, self.dmg, o.heavy_bullets[0])
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 1:
                bullet1 = o.Bullet(self.rect.left, self.rect.centery, -10, self.dmg, o.heavy_bullets[0])
                bullet2 = o.Bullet(self.rect.right, self.rect.centery, -10, self.dmg, o.heavy_bullets[0])
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    
    def reset(self):
        self.lives = 3
        self.dmg = 10
        self.power = 0
        self.shields = 0
        self.lasers = 0

    def powerup(self):
        self.power += 1
        if self.power_time == 0:
            self.power_time = pygame.time.get_ticks()
    def invulnerable(self):
        self.shields += 1
        player_shield.on = True
        if self.shield_time == 0:
            self.shield_time = pygame.time.get_ticks()
    def laser_gun(self):
        if self.lasers == 0:
            player_laser = o.Laser(self, 5000, 'player', self.dmg/4)
            player_group.add(player_laser)
            all_sprites.add(player_laser)
            player_laser_group.add(player_laser)
            self.laser_time = pygame.time.get_ticks()
        else:
            player_laser.life_span += 5000
        self.lasers += 1
            
class Forcefield(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.image = forcefield_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.height * 0.90 / 2)
        self.rect.center = [-500, -500]
        self.on = False
    def update(self):
        if self.on == True:
            self.rect.centerx = self.owner.rect.centerx
            self.rect.bottom = self.owner.rect.y
        else:
            self.rect.center = [-500, -500]        

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
player_shield = Forcefield(player)
player_group.add(player)
player_group.add(player_shield)
player_laser_group = pygame.sprite.Group()