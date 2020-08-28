import pygame
import random

pygame.init()
pygame.mixer.init()

FPS = 60
size = width, height = 500, 500
text_position = text_x, text_y = 10, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

game_window = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('images/background.png'), (500, 500))
# Load sounds
shoot = pygame.mixer.Sound("sounds/shoot.wav")
hit = pygame.mixer.Sound("sounds/hit.wav")


def show_go_screen():
    draw_text(game_window, "Space Invaders", 50, width / 2, width * .2)
    draw_text(game_window, "Press Any Key To Start", 30, width / 2, height / 3)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def draw_text(surface, text, text_size, x, y):
    font = pygame.font.Font('freesansbold.ttf', text_size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/final_spaceship.png')
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.center = (width / 2, 450)

    def update(self):
        keys = pygame.key.get_pressed()
        # Player movement
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 8
        if keys[pygame.K_RIGHT] and self.rect.x < width - 50:
            self.rect.x += 8
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= 8
        if keys[pygame.K_DOWN] and self.rect.y < height - 50:
            self.rect.y += 8

    def shoot(self):
        bullet = Bullet(self.rect.center, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = random.randint(0, width - 40)
        self.rect.y = random.randint(0, 45)
        self.enemy_x_change = random.randint(3, 10)
        self.enemy_y_change = 40

    def update(self):
        # Enemy movement
        self.rect.x += self.enemy_x_change
        if self.rect.x <= 0:
            self.rect.x = 0
            self.rect.y += self.enemy_y_change
            self.enemy_x_change = random.randint(3, 5)
        if self.rect.x >= width - 40:
            self.enemy_x_change = -5
            self.rect.y += self.enemy_y_change


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.center = x
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


game_over = True
running = True
while running:

    game_window.blit(background, (0, 0))

    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        for i in range(10):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Check if bullet hit enemy
    bullet_collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for collision in bullet_collisions:
        hit.play()
        score += 1
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check if enemy hit player
    enemy_collisions = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
    if enemy_collisions:
        game_over = True

    all_sprites.update()
    all_sprites.draw(game_window)
    draw_text(game_window, str(score), 18, width / 2, 10)
    pygame.display.flip()