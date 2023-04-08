from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
clock = time.Clock()
window  = display.set_mode((win_width, win_height))
display.set_caption('shoter468')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('opp.ogg')
font.init()
font2 = font.Font(None, 90)
font1 = font.Font(None, 90)
font3 = font.Font(None, 30)
win = font1.render('You Win!', True, (0, 255, 255))
lose = font2.render('You lose!!', True, (255, 0, 0))
now_time = 10
last_time = 0


FPS = 30
lost = 0
score = 0

class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_hight, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_hight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('hh.png', self.rect.centerx, self.rect.top, 15, 20, -15) 
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y  = -40
            self.rect.x = randint(5, win_width - 65)
            lost = lost +1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

player = Player ('raketa.png', 10, 425, 65, 65, 7)
monsters = sprite.Group()
for i in range (15):
    monster = Enemy('ufo.png', randint(5, win_width-80),-40, 80, 50, randint(1,3))
    monsters.add(monster)
bullets = sprite.Group()

rel_time = False #флаг, отвечаю
num_fire = 0
game = True
finish = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            fire_sound.play()
            player.fire()
        elif e.type == KEYDOWN:  
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True





            

    if finish != True:
        window.blit(background, (0, 0))
        player.reset()    
        monsters.draw(window)
        bullets.draw(window)


        player.update()
        monsters.u  ddate()
        bullets.update()



        text_lose = font3.render ('пропущено: '+ str(lost), 1, (89, 122, 255))
        window.blit(text_lose, (10 , 50))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(5, win_width-80),-40, 80, 50, randint(1,1))
            monsters.add(monster)

        text_score = font3.render('Счёт' + str(score), 1, (89, 122, 255))
        window.blit(text_score, (5, 25))



        if sprite.spritecollide(player, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (200, 200))


        if rel_time == True:
            now_time = timer()
        if now_time - last_time<3 :
            reload = font3.render('wait reload...', 1, (250, 0, 0))
            window.blit (reload, (260, 460))
        else:
            num_fire = 0
            rel_time = False

    display.update()
    clock.tick(FPS)


