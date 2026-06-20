import pygame
import random

pygame.init()
width, height = 900, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dino Game")
fps = 60
clock = pygame.time.Clock()

dino_img = pygame.image.load('dinosaur.png')
cactus_img = pygame.image.load('cactus.png')
ground_img = pygame.image.load('ground.png')
bird_img = pygame.image.load('bird.png')

dino_img = pygame.transform.scale(dino_img, (60, 60))
cactus_img = pygame.transform.scale(cactus_img, (35, 60))
bird_img = pygame.transform.scale(bird_img, (45, 40))
ground_img = pygame.transform.scale(ground_img, (width, 20))

jump_sound = pygame.mixer.Sound('jump.mp3')
score_sound = pygame.mixer.Sound('score.mp3')
collision_sound = pygame.mixer.Sound('collision.mp3')
pygame.mixer.music.load('music.mp3')
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)

class Dino:
    def __init__(self):
        self.image = dino_img
        self.x = 50
        self.floor_y = height - self.image.get_height() - 50
        self.y = self.floor_y
        self.vel_y = 0
        self.gravity = 1
        self.jump_height = -16
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.jump_count = 0

    def update(self):
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.y > self.floor_y:
            self.y = self.floor_y
            self.vel_y = 0
            self.is_jumping = False

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_height
            self.is_jumping = True
            self.jump_count += 1
            print(f"Прыжков совершено: {self.jump_count}")
            jump_sound.play()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, y_pos, speed):
        self.image = image
        self.x = width
        self.y = y_pos
        self.vel_x = speed
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self):
        self.x -= self.vel_x
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Cactus(Obstacle):
    def __init__(self, speed):
        y_pos = height - cactus_img.get_height() - 50
        super().__init__(cactus_img, y_pos, speed)


class Bird(Obstacle):
    def __init__(self, speed):
        y_pos = height - 130 if random.random() > 0.5 else height - 90
        super().__init__(bird_img, y_pos, speed)

class Ground:
    def __init__(self,y,speed):
        self.image = ground_img
        self.x1 = 0
        self.x2 = self.image.get_width()
        self.y = y
        self.speed = speed

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 <= -self.image.get_width():
            self.x1 = self.x2 + self.image.get_width()
        if self.x2 <= -self.image.get_width():
            self.x2 = self.x1 + self.image.get_width()

    def draw(self):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))

def check_Collision(dino, obstacle):
    return dino.rect.colliderect(obstacle.rect)


def display_score():
    font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (10, 50))

def create_random_obstacle(speed):
    if random.random() > 0.5:
        return Cactus(speed)
    else:
        return Bird(speed)

def start_menu():
    font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
    title = font.render("DINO GAME", True, (0, 0, 0))
    start = font.render("press SPACE to start", True, (0, 0, 0))

    waiting = True
    while waiting:
        color=(255,255,255)
        screen.fill(color)
        screen.blit(title, (title.get_width() / 2, title.get_height() / 2+120))
        screen.blit(start,(start.get_width() / 2, start.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_over():
    font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
    text = font.render("game over", True, (0, 0, 0))
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

running = True
dino = Dino()
obstacle_speed = 8
current_obstacle = create_random_obstacle(obstacle_speed)
score = 0
ground = Ground(400, 5)
high_score = 0
start_menu()

while running:
    bg_color = (255, 255, 255)
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()

    dino.update()
    current_obstacle.update()
    ground.update()

    if current_obstacle.x + current_obstacle.image.get_width() < dino.x:
        score += 1
        score_sound.play()
        if score > 0:
            obstacle_speed += 0.3
        current_obstacle = create_random_obstacle(obstacle_speed)

    if check_Collision(dino, current_obstacle):
        collision_sound.play()
        print(f"Всего прыжков за игру: {dino.jump_count}")
        if score > high_score:
            high_score = score
        game_over()

        dino = Dino()
        obstacle_speed = 8
        current_obstacle = create_random_obstacle(obstacle_speed)
        score = 0
        continue

    dino.draw()
    current_obstacle.draw()
    display_score()
    ground.draw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()