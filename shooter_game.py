from pygame import *

import random

from random import randint

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):

    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)
        self.speed = speed
        self.last_shot = 0  # время последнего выстрела

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1190 - self.rect.width:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            player.fire()
    
    def fire(self):
        #global ammo
        #ammo = 70
        current_time = time.get_ticks()  # текущее время 
        if current_time - self.last_shot > 300:  # задержка в 0.3 сек
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -5)
            bullets.add(bullet)
        #ammo = ammo - 1
            mixer.init()
            firel = mixer.Sound('fire.ogg')
            mixer.music.play()
            self.last_shot = current_time

class Enemy(GameSprite):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = randint(80, 1120)
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (10, 20))
    def update(self):
        self.rect.y += self.speed
        global win
        if self.rect.y < 0:
            self.kill()
        if sprite.groupcollide(monsters, bullets, True, True):
            win = win + 1
            monster1 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
            monsters.add(monster1)
        if sprite.groupcollide(asteroids, bullets, True, True):
            win = win + 1
            monster1 = Enemy('asteroid.png', randint(80, 1120), 0, randint(1, 4))
            asteroids.add(asteroid1)

class Asteroid(GameSprite):
    def __init__(self, image_path, x, y, speed):
        super().__init__(image_path, x, y, speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = randint(80, 1120)

monsters = sprite.Group()

monster1 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster2 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster3 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster4 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster5 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster6 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monster7 = Enemy('ufo.png', randint(80, 1120), 0, randint(1, 4))
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
monsters.add(monster6)
monsters.add(monster7)

bullets = sprite.Group()

asteroids = sprite.Group()

asteroid1 = Asteroid('asteroid.png', randint(80, 1120), 0, randint(1, 4))
asteroid2 = Asteroid('asteroid.png', randint(80, 1120), 0, randint(1, 4))
asteroid3 = Asteroid('asteroid.png', randint(80, 1120), 0, randint(1, 4))
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

background1 = ('galaxy-night-panoramic.jpg')
background2 = ('galaxy-space-scene.jpg')
background3 = ('galaxy-night-view.jpg')
background4 = ('galaxy-background-with-fictional-planets.jpg')
backgrounds = [background1, background2, background3, background4]
fon = random.choice(backgrounds)

window = display.set_mode((1200, 900))
display.set_caption('Супер мега крутое название')
background = transform.scale(image.load(fon), (1200, 900))
mixer.init()
mixer.music.load('Galactic-Rap.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()

player = Player('rocket.png', 600, 750, 10)

run = True
finish = False
clock = time.Clock()
FPS = 60
lost = 0
win = 0
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 128)
lose = font3.render('YOU LOSE', True,(255,0,0))
winner = font3.render('YOU WIN', True,(124,252,0))
#ammunition = font2.render('Патроны', True,(255, 255, 255))

#global ammo
#ammo = 70

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire() 
    

    if finish != True:

        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_win = font2.render("Поверженно:" + str(win), 1, (255, 255, 255))
        #text_ammo = font2.render("Патроны:" + str(ammo), 1, (255, 255, 255))

        clock.tick(FPS)
        window.blit(background,(0, 0))
        window.blit(text_lose, (10, 40))
        window.blit(text_win, (10, 10))
        #window.blit(text_ammo, (10, 200))

        player.reset()

        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        display.update()
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        if lost >= 10 or sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (400, 400))
            display.update()
        elif win >= 20:
            finish = True
            window.blit(winner, (400, 400))
            display.update()

display.update()