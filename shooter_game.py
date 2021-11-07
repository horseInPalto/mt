from pygame import *
from random import randint
from time import time as timer 

x = 900
y = 500

window = display.set_mode((900, 500))
display.set_caption("Шутер")
background = transform.scale (image.load("galaxy.jpg"), (900, 500))
FPS = 60
clock = time.Clock()

finish = False

font.init()
font2 = font.SysFont('Arial', 36)

score = 0
lost = 0
ssh = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(70,70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def recet(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < x - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.bottom = 0
            self.rect.x = randint(50, x-50)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
           
class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.rect.bottom = 0
            self.rect.x = randint(50, x-50)

hero = Player('rocket.png', 100, 400, 20)

asteroid = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1, 15):
    enemy1 = Enemy('ufo.png', randint(0, 900) ,10, randint(1, 4))
    monsters.add(enemy1)

for r in range(1, 3):
    asteroid1 = Aster('asteroid.png', randint(0, 900) ,10, randint(1, 4))
    asteroid.add(asteroid1)

num_fire= 0
rel_time= False

game= True

while game:
    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        hero.recet() 
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroid.draw(window)
        asteroid.update()

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif  e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire= num_fire+ 1
                    hero.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time= True

    if rel_time== True:
        now_time=timer()
        if now_time - last_time< 3:
            reload_fire = font2.render('перезарядка', 1, (200, 0 ,0))
            window.blit(reload_fire,(260,460))
        else:
            num_fire= 0
            rel_time = False

    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for w in sprites_list:
        monster = Enemy('ufo.png', randint(0, 900) ,10, randint(1, 4))
        monsters.add(monsters)
        score = score + 1
    
    for aster in asteroid:
        if aster.rect.colliderect(hero.rect):
            aster.kill()
            asteroid1 = Aster('asteroid.png', randint(0, 900) ,10, randint(1, 4))
            asteroid.add(asteroid1)
            ssh += 1


    text = font2.render('Счет: ' + str(score),1, (176, 163, 212))
    window.blit(text, (10, 20))
    text_2 = font2.render('Пропущенно: ' + str(lost),1, (176, 163, 212))
    window.blit(text_2, (10, 50))
    text_3 = font2.render('Ранение: ' + str(ssh),1, (176, 163, 212))
    window.blit(text_3, (10, 80))  
    window.blit(font2.render(str(len(monsters)), 1, (176, 163, 212)), (10, 100))

    clock.tick(FPS)
    display.update()
    