import os
from pygame import *
from random import randint, choice

os.chdir(os.path.dirname(os.path.abspath(__file__)))

init()
mixer.init()
font.init()

info = display.Info()
win_width = info.current_w
win_height = info.current_h

window = display.set_mode((win_width, win_height), FULLSCREEN)
display.set_caption("Shooter")

FPS = 60
score = 0
lost = 0
is_boss_alive = False
finish = False
game = True

font_main = font.Font(None, 45)
font_win = font.Font(None, 100)

img_back = "пуджара.jpg"
img_hero = "птица.png"
img_bullet = "images-_6_.png"
img_scrimer = "scrimer.jpg"    
img_boss = "ьувмув.png"         
enemy_images = ['ivan2.png', '8.jpg', 'ivan1.png', 'пнг11.png']

try:
    mixer.music.load('08279.wav')
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)
    scream_sound = mixer.Sound('scream.wav')
except:
    pass

background = transform.scale(image.load(img_back), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        try:
            self.image = transform.scale(image.load(player_image), (w, h))
        except:
            self.image = Surface((w, h))
            self.image.fill((255, 0, 0))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 15
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += 15
            
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 10, self.rect.top, 15, 30, 45)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(50, win_width - 100)
            self.rect.y = -100
            lost += 1

class Boss(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h, hp):
        super().__init__(player_image, player_x, player_y, player_speed, w, h)
        self.hp = hp
        self.speed_x = player_speed
        self.speed_y = player_speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= win_width - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.speed_y *= -1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, win_width//2, win_height - 150, 15, 100, 100)
bullets = sprite.Group()
enemies = sprite.Group()

def create_enemies():
    for i in range(5):
        enemy = Enemy(choice(enemy_images), randint(50, win_width - 100), -100, randint(1, 2), 90, 90)
        enemies.add(enemy)

create_enemies()
clock = time.Clock()
won = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                ship.fire()
            if e.key == K_ESCAPE:
                game = False

    if not finish:
        window.blit(background, (0, 0))
        window.blit(font_main.render("Убито: " + str(score), True, (255, 255, 255)), (30, 30))
        window.blit(font_main.render("Пропущено: " + str(lost), True, (255, 255, 255)), (30, 80))

        ship.update()
        enemies.update()
        bullets.update()

        ship.reset()
        enemies.draw(window)
        bullets.draw(window)

        if not is_boss_alive:
            collides = sprite.groupcollide(enemies, bullets, True, True)
            for c in collides:
                score += 1
                new_enemy = Enemy(choice(enemy_images), randint(50, win_width - 100), -100, randint(1, 2), 90, 90)
                enemies.add(new_enemy)
            
            if score >= 2:
                is_boss_alive = True
                for e in enemies: e.kill()
                boss = Boss(img_boss, win_width//2, 100, 6, 300, 300, 25)
                enemies.add(boss)
        else:
            window.blit(font_main.render("HP БОССА: " + str(boss.hp), True, (255, 0, 0)), (win_width//2 - 100, 30))
            boss_hit = sprite.spritecollide(boss, bullets, True)
            if boss_hit:
                boss.hp -= 1
                if boss.hp <= 0:
                    boss.kill()
                    finish = True
                    won = True

        if sprite.spritecollide(ship, enemies, False) or lost >= 100:
            if is_boss_alive:
                mixer.music.stop()
                try:
                    scream_sound.play()
                    scr_img = transform.scale(image.load(img_scrimer), (win_width, win_height))
                    window.blit(scr_img, (0, 0))
                    display.flip() # Обновляем экран немедленно
                    time.wait(2000) # Замираем на 2 секунды
                except:
                    pass
            finish = True
            won = False

        display.update()
    else:
        if won:
            msg = font_win.render("ПОБЕДА!", True, (0, 255, 0))
        else:
            msg = font_win.render("ТЫ ПРОИГРАЛ", True, (255, 0, 0))
        
        window.blit(msg, (win_width//2 - 250, win_height//2))
        display.update()
        time.delay(3000)
        
        score, lost = 0, 0
        is_boss_alive, finish, won = False, False, False
        for e in enemies: e.kill()
        for b in bullets: b.kill()
        create_enemies()
        try: mixer.music.play(-1)
        except: pass

    clock.tick(FPS)





