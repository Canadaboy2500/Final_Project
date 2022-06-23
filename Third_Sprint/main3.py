#---------------------
#-----OOP Summative---
#-------June 02, 2022-
#-----Mason Skinner---
#---------------------
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

import pygame
import random
from os import path
import player3 as p
import mobs3 as m
import effects3 as e
import objects3 as o

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
#-----Constants---
WIDTH = 480
HEIGHT = 600
FPS = 60
#-----Colors-----
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
        

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        if i % 3 == 0:
            new_x = x
        elif i % 3 == 1:
            new_x = x + 30
        elif i % 3 == 2:
            new_x = x + 60
        if i % 3 == 0:
            y = y + 30
        img_rect.x = new_x
        img_rect.y = y
        surf.blit(img, img_rect)
    
def draw_shield_bar(surf, x, y, pot):
    if pot < 0:
        pot = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (pot / 200) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                p.player.reset()
                waiting = False
                
def enemy_hit(hits, dmg, score):              
    for hit in hits:
        if hit.health >= dmg:
            score += dmg
        else:
            score += hit.health
        hit.health -= dmg
    return score

font_name = pygame.font.match_font('arial')
background = pygame.image.load(path.join(img_dir, 'back.png')).convert()
background_rect = background.get_rect()
player_mini_img = pygame.transform.scale(p.player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

offensive_power_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield_sound.wav'))
defensive_power_sound = pygame.mixer.Sound(path.join(snd_dir, 'power_sound.wav'))

expl_sounds = []
for snd in ['explosion1.wav', 'explosion2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
    
POWERUP_TIME = 5000
pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
game_end = False
running = True
while running:
    now = pygame.time.get_ticks()
    meteors = m.meteors
    aliens = m.aliens
    ai_bullets = m.ai_bullets
    ai_lasers = m.ai_lasers
    bullets = p.bullets
    powerups = p.powerups
    player_group = p.player_group
    if game_over:
        show_go_screen()
        game_over = False
        m.meteors.empty()
        m.all_sprites.empty()
        m.aliens.empty()
        m.ai_bullets.empty()
        m.ai_lasers.empty()
        p.bullets.empty()
        p.powerups.empty()
        all_sprites = pygame.sprite.Group()
        meteors.empty()
        meteor_bank = 0
        alien_bank = 0
        boss_bank = 0
        rock_bank = 0
        health_dmg_bank = 0
        b = 0
        l = 0
        score = 0
        health_mult = 1
        dmg_mult = 1
        rock_mult = 0
        for i in range(7):
            m.new_meteor('lrg', [0,0], 'normal', health_mult, dmg_mult, rock_mult)
    if score - rock_bank > 10000:
        rock_bank = score
        rock_mult += 0.005
    if score - health_dmg_bank > 2500:
        health_dmg_bank = score
        health_mult += 0.05
        dmg_mult += 0.005
    if score - meteor_bank > 15000:
        meteor_bank = score
        l += 1
        if l < 4:
            m.new_meteor('lrg', [0,0], 'normal',  health_mult, dmg_mult, rock_mult)
    if score - alien_bank > 2500:
        alien_bank = score
        m.new_alien(0, health_mult, dmg_mult)
    if score - boss_bank > 15000:
        boss_bank = score
        if b < 5:
            m.new_boss(b, health_mult, dmg_mult)
            b += 1
        else:
            m.new_boss(random.randrange(0, 4), health_mult)
        if boss_bank >= 150000:
            m.new_boss(random.randrange(0, 4), dmg_mult)
    clock.tick(FPS)
    #Input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Update
    all_sprites.update()
    p.all_sprites.update()
    m.all_sprites.update(health_mult, dmg_mult, rock_mult)
    m.ai_bullets.update()
    m.ai_lasers.update()
    p.player_group.update()
    
    if not p.player.respawn and not p.player.dead:
        if p.player.shields >= 1:
            hits = pygame.sprite.spritecollide(p.player_shield, m.meteors, True, pygame.sprite.collide_circle)
            hits1 = pygame.sprite.spritecollide(p.player_shield, m.ai_bullets, True, pygame.sprite.collide_circle)
            hits.extend(hits1)
            for hit in hits:
                expl = e.Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                if hit.kind == 'meteor':
                    if hit.origin == 'normal':
                        m.new_meteor('lrg', [0,0], 'normal', health_mult, dmg_mult, rock_mult)
                    m.all_sprites.remove(hit)
                    m.meteors.remove(hit)
                        
        hits = pygame.sprite.spritecollide(p.player, m.meteors, True, pygame.sprite.collide_circle)
        hits1 = pygame.sprite.spritecollide(p.player, m.ai_bullets, True, pygame.sprite.collide_circle)
        hits.extend(hits1)
        for hit in hits:
            p.player.shield -= hit.dmg
            expl = e.Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if hit.kind == 'meteor':
                if hit.origin == 'normal':
                    m.new_meteor('lrg', [0,0], 'normal', health_mult, dmg_mult, rock_mult)
        hits = pygame.sprite.spritecollide(p.player, m.ai_lasers, False, pygame.sprite.collide_rect)
        for hit in hits:
            p.player.shield -= hit.dmg
        if p.player.shield <= 0:
            death_explosion = e.Explosion(p.player.rect.center, 'player')
            all_sprites.add(death_explosion)
            if p.player.lives >= 1:
                p.player.kill_self()
                p.player.lives -= 1
                p.player.shield = 100
    if p.player.lives == 0 and not death_explosion.alive():
        game_over = True
      
    hits = pygame.sprite.groupcollide(m.meteors, p.bullets, False, True)
    hits1 = pygame.sprite.groupcollide(m.aliens, p.bullets, False, True)
    hits.update(hits1)
    dmg = p.player.dmg
    score = enemy_hit(hits, dmg, score)
    if p.player.lasers >= 1:
        hits2 = pygame.sprite.groupcollide(m.meteors, p.player_laser_group, False, False)
        hits3 = pygame.sprite.groupcollide(m.aliens, p.player_laser_group, False, False)
        hits2.update(hits3)
        dmg = p.player.dmg * 0.075  
        score = enemy_hit(hits2, dmg, score)
        hits.update(hits2)
    
    for hit in hits:
        if hit.health <= 0:
            score += int(110 - hit.rect.width)
            hit.kill()
            random.choice(expl_sounds).play()
            exp1 = e.Explosion(hit.rect.center, 'lg')
            all_sprites.add(exp1)
            if hit.kind == 'meteor':
                if hit.rect.width >= 88:
                    for i in range(2):
                        m.new_meteor('med', hit.rect.center, 'mini', health_mult, dmg_mult, rock_mult)
                elif hit.rect.width >= 40:
                    for i in range(2):
                        m.new_meteor('sml', hit.rect.center, 'mini', health_mult, dmg_mult, rock_mult)
                if hit.origin == 'normal':
                    m.new_meteor('lrg', [0, 0], 'normal', health_mult, dmg_mult, rock_mult)
            if random.random() > 0.75:
                if random.random() > 0.85:
                    pow = o.Super_Pow(2, hit.rect.center)
                else:
                    pow = o.Basic_Pow(2, hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
                
    hits = pygame.sprite.spritecollide(p.player, p.powerups, True)
    for hit in hits:
        if hit.type == 'pow_shield':
            defensive_power_sound.play()
            p.player.shield += random.randrange(20, 40)
            if p.player.shield >= 200:
                p.player.shield = 200
        elif hit.type == 'pow_power':
            offensive_power_sound.play()
            p.player.dmg += 2.5
        elif hit.type == 'pow_gun':
            p.player.powerup()
            offensive_power_sound.play()
        elif hit.type == 'pow_extralife':
            p.player.lives += 1
            defensive_power_sound.play()
        elif hit.type == 'pow_invulnerable':
            p.player.invulnerable()
            defensive_power_sound.play()
        elif hit.type == 'pow_laser':
            offensive_power_sound.play()
            p.player.laser_gun()

    #Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    p.all_sprites.draw(screen)
    p.player_group.draw(screen)
    m.all_sprites.draw(screen)
    m.ai_bullets.draw(screen)
    m.ai_lasers.draw(screen)
    all_sprites.draw(screen)
    draw_text(screen, str(int(score)), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, p.player.shield)
    draw_lives(screen, WIDTH - 100, -25, p.player.lives, player_mini_img)
    pygame.display.flip()
    
pygame.quit()
