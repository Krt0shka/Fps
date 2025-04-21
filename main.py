import pygame, time
from random import randint

pygame.init()

config = {
    "FPS": 40,
    "WIDTH": 700,
    "HEIGHT": 503,
    "SIZE": 70,
    "PLAYER": {
        "SIZE": 50,
        "SPEED": 7,
        "X": 5,
        "Y": 380
    },
    "ENEMY": {
        "SIZE": 60
    },
    "MONSTERS_COUNT": 5,
    "ASTEROIDS_COUNT": 3
}

screen = pygame.display.set_mode((config["WIDTH"], config["HEIGHT"]))
pygame.display.set_caption("FPS")
pygame.display.set_icon(pygame.image.load("files/imgs/player.png"))


pygame.mixer.init()
pygame.mixer.music.load("files/music/space.ogg")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)

bg = pygame.transform.scale(pygame.image.load("files/imgs/bg.png"), (700, 500))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img: pygame.Surface, speed, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < config['WIDTH'] - config["PLAYER"]["SIZE"] - 5:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > config["HEIGHT"] - self.rect.height:
            self.rect.y = 0
            self.rect.x = randint(0, config["WIDTH"] - self.rect.width)
            self.speed = randint(2, 3)
            global lcounter
            lcounter += 1
class Asteroid(GameSprite):
    def __init__(self, img, speed, x, y):
        super().__init__(img, speed, x, y)
        self.starty = self.rect.y
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > config["HEIGHT"] - self.rect.height:
            self.rect.y = self.starty
            self.rect.x = randint(0, config["WIDTH"] - self.rect.width)
            self.speed = randint(2, 3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -10:
            self.kill()
            
lcounter = 0
kills = 1
shots = 1
bullets_count = 10

monsters = pygame.sprite.Group()
for m in range(config["MONSTERS_COUNT"]):
    monster = Enemy(pygame.transform.scale(pygame.image.load("files/imgs/enemy1.png"), (config["ENEMY"]["SIZE"], config["ENEMY"]["SIZE"])), randint(1, 3), randint(0, config["WIDTH"] - config["ENEMY"]["SIZE"]), 0)
    monsters.add(monster)

asteroids = pygame.sprite.Group()
asteroid1 = Asteroid(pygame.transform.scale(pygame.image.load("files/imgs/asteroid.png"), (config["ENEMY"]["SIZE"], config["ENEMY"]["SIZE"])), randint(1, 2), randint(0, config["WIDTH"] - config["ENEMY"]["SIZE"]), -700)
asteroid2 = Asteroid(pygame.transform.scale(pygame.image.load("files/imgs/asteroid.png"), (config["ENEMY"]["SIZE"], config["ENEMY"]["SIZE"])), randint(1, 2), randint(0, config["WIDTH"] - config["ENEMY"]["SIZE"]), -1400)
asteroid3 = Asteroid(pygame.transform.scale(pygame.image.load("files/imgs/asteroid.png"), (config["ENEMY"]["SIZE"], config["ENEMY"]["SIZE"])), randint(1, 2), randint(0, config["WIDTH"] - config["ENEMY"]["SIZE"]), -2000)
asteroids.add(asteroid1, asteroid2, asteroid3)


bullets = pygame.sprite.Group()

rocket = Player(pygame.transform.scale(pygame.image.load("files/imgs/playerv2.png"), (config["PLAYER"]["SIZE"], config["PLAYER"]["SIZE"]*1.666)), config["PLAYER"]["SPEED"], 5, 400)

font = pygame.font.SysFont("Arial", 24)
lfont = pygame.font.SysFont("Impact", 60)



def update_wcounter():
    text = font.render(f"Ваш счёт: {kills - 1}", True, (255, 255, 255))
    screen.blit(text, (config["WIDTH"] - text.get_width() - 10, 10))
def update_lcounter():
    text = font.render(f"Вы пропустили: {lcounter}", True, (255, 255, 255))
    screen.blit(text, (config["WIDTH"] - text.get_width() - 10, 35))
def update_acounter():
    acc = round(kills / shots * 100, 2)
    text = font.render(f"Ваша аккуратность: {acc}", True, (255, 255, 255))
    screen.blit(text, (config["WIDTH"] - text.get_width() - 10, 60))
def update_bullets_counter(md):
    global bullets_count
    #md: 0 - патроны кончились, 1 - перезарядка
    text = font.render(f"{bullets_count}/10 патронов", True, (255, 255, 255))
    screen.blit(text, (config["WIDTH"] - text.get_width() - 10, 85))
    if bullets_count == 0 and md == 0:
        text2 = font.render("R - перезарядка", True, (255, 255,  255))
        screen.blit(text2, (config["WIDTH"] - text2.get_width() - 10, 110))
    elif bullets_count == 0 and md == 1:
        text2 = font.render("Презарядка...", True, (255, 255,  255))
        screen.blit(text2, (config["WIDTH"] - text2.get_width() - 10, 110))


clock = pygame.time.Clock()
finish = False
running = True
mode = -1
startrel = -1
rellock = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullets_count > 0 and bullets_count <= 10:
                mode = -1
                bullets_count -= 1
                shots += 1
                shot = pygame.mixer.Sound("files\music\\fire.mp3")
                shot.play()
                bullet = Bullet(pygame.transform.scale(pygame.image.load("files/imgs/bullet.png"), (20, 50)), 30, rocket.rect.centerx - 17, rocket.rect.centery)
                bullets.add(bullet)
            if event.key == pygame.K_r and mode == 0 and rellock == False:
                mode = 1
                startrel = time.time()
                rellock = True


                
    if not finish:
        if mode == 1:
            if time.time() - int(startrel) >= 3:
                bullets_count = 10
                mode = -1
                rellock = False
        elif bullets_count == 0:
            mode = 0

        screen.blit(bg, (0, 0))
        
        monsters.update()
        monsters.draw(screen)

        asteroids.update()
        asteroids.draw(screen)

        bullets.update()
        bullets.draw(screen)

        rocket.update()
        rocket.reset()

        update_lcounter()
        update_wcounter()
        update_acounter()
        update_bullets_counter(mode)

        sprite_list = pygame.sprite.groupcollide(
            monsters, bullets, True, True
        )

        if len(sprite_list) != 0:
            kills += 1
            monster = Enemy(pygame.transform.scale(pygame.image.load("files/imgs/enemy1.png"), (config["ENEMY"]["SIZE"], config["ENEMY"]["SIZE"])), randint(1, 3), randint(0, config["WIDTH"] - config["ENEMY"]["SIZE"]), 0)
            monsters.add(monster)

        sprite_list2 = pygame.sprite.spritecollide(
            rocket, monsters, True
        )

        if len(sprite_list2) != 0:
            finish = True
            ltext = text = lfont.render("Вы проиграли!", True, (255, 0, 0))
            screen.blit(ltext, (screen.get_width()/2 - 200, screen.get_height()/2 - 50))

        sprite_list3 = pygame.sprite.groupcollide(
            asteroids, bullets, False, True
        )

        sprite_list4 = pygame.sprite.spritecollide(
            rocket, asteroids, True
        )

        if len(sprite_list4) != 0:
            finish = True
            ltext = text = lfont.render("Вы проиграли!", True, (255, 0, 0))
            screen.blit(ltext, (screen.get_width()/2 - 200, screen.get_height()/2 - 50))

        pygame.display.update()
        clock.tick(config["FPS"])