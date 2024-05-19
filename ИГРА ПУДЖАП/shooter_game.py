   #Создай собственный Шутер!

from pygame import *
from random import *
font.init()
text2 = font.Font(None, 30)
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("пуджара.jpg"), (win_width, win_height))
mixer.init()
mixer.music.load('08279.wav')
mixer.music.play(-1)
run = True
clock=time.Clock()
FPS = 60
score = 0
lost = 0
miss = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT]:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet('images-_6_.png', self.rect.centerx,self.rect.top, 25, 3, 5 )
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
            lost = lost + 1
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
font.init()
font1 = font.Font(None, 36) #52
font2 = font.Font(None, 36) 

bullets = sprite.Group()
    
    
sprite1 = GameSprite('птица.png', 400,400, 1, 65,65)
svin = Enemy('пнг11.png',400, 0, 3, 50, 50)
svin2 = Enemy('пнг11.png',300, 0, 4, 50, 50)
svin3 = Enemy('пнг11.png',200, 0, 1, 50, 50)
svin4 = Enemy('пнг11.png',100, 0, 6, 50, 50)
svin5 = Enemy('пнг11.png',50, 0, 1, 50, 50)

enemies = sprite.Group()
enemies.add(svin)
enemies.add(svin2)
enemies.add(svin3)
enemies.add(svin4)
enemies.add(svin5)





















finish = False
game = True
while game:
    clock.tick(FPS)
    window.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            sprite1.fire()
       
    if finish != True:
        t = font2.render("Убито страшных свиней:" + str(score), True, (255,255,255))
        window.blit(t, (10, 50)) 
        sprite1.reset()
        sprite1.move()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        if sprite.groupcollide(enemies, bullets, True, True):
            score +=1
            svin6 = Enemy('пнг11.png',randint(50, 650), 0, randint(1,3), 50, 50)
            enemies.add(svin6)
        if sprite.spritecollide(sprite1, enemies, False):
            score = 0
            lost = 0
            finish = True
        display.update()
    else:
        time.delay(3000)
        for m in enemies:
            m.kill()
        svin = Enemy('пнг11.png',400, 0, 3, 50, 50)
        svin2 = Enemy('пнг11.png',300, 0, 4, 50, 50)
        svin3 = Enemy('пнг11.png',200, 0, 1, 50, 50)
        svin4 = Enemy('пнг11.png',100, 0, 6, 50, 50)
        svin5 = Enemy('пнг11.png',50, 0, 1, 50, 50)
        for m in bullets:
            m.kill()


        enemies.add(svin)
        enemies.add(svin2)
        enemies.add(svin3)
        enemies.add(svin4)
        enemies.add(svin5)





