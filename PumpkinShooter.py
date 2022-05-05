import pygame
import random
import math

pygame.init()

# Game Window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Pumpkin Shooter')
icon = pygame.image.load('data/logo.png')
pygame.display.set_icon(icon)

# Background Image
bg = pygame.image.load('data/background.jpg')

# BGM
pygame.mixer.music.load('data/bg_music.mp3')
pygame.mixer.music.play(-1)

# Bullet Sound
bullet_sound = pygame.mixer.Sound('data/laser.wav')
explosion_sound = pygame.mixer.Sound('data/explosion.wav')

# Player
player_img = pygame.image.load('data/player2.png')
playerX = 368
playerY = 516
playerX_Change = 0

# Enemy and Multiple Enemies for Take it List Items
num_of_enemies = 6

enemy_img = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
# after Created Multiple Enemies
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('data/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(20, 120))
    enemyX_Change.append(0.6)
    enemyY_Change.append(40)

# Bullet
bullet_img = pygame.image.load('data/bullet.png')
bulletX = 0
bulletY = 516
bullet_state = 'ready'
bulletY_Change = -1.5

# Score
score = 0
# Score Text
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 0
scoreY = 0

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_overX = 200
game_overY = 200

# RESTART GAME
restart_font = pygame.font.Font('freesansbold.ttf', 32)
restartX = 180
restartY = 300

game_status = 'running'


def show_restart(x, y):
    restart_img = restart_font.render('To restart the Game press R', True, (0, 255, 0))
    screen.blit(restart_img, (x, y))


def show_game_over(x, y):
    global game_status
    game_over_img = game_over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(game_over_img, (x, y))
    pygame.mixer.music.stop()
    game_status = 'end'


def show_score(x, y):
    score_img = score_font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_img, (x, y))


# playerBLIT
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def bullet(x, y):
    screen.blit(bullet_img, (x + 16, y + 10))


# Coliision
def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:

    # RGB Color for Window
    screen.fill((0, 0, 0))
    # Display Background Image
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movent Mecanic for Plyaer Pressed Key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.3
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bullet_sound.play()
            if event.key == pygame.K_r:
                if game_status == 'end':
                    game_status = 'running'
                    pygame.mixer.music.play(-1)
                    score = 0
                    playerX = 368
                    # To Reload Enemies
                    for i in range(num_of_enemies):
                        enemyX[i] = random.randint(0, 736)
                        enemyY[i] = random.randint(20, 120)
        # Key Released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_Change = 0

    # Bullet Movents
    if bullet_state == 'fire':
        if bulletY < 10:
            bulletY = 516
            bullet_state = 'ready'
            # print('ok')
        bullet(bulletX, bulletY)
        bulletY += bulletY_Change

    # Enemy Movements
    # after multiple enemies for Taking FOR LOOP and taking in this for loop
    for i in range(num_of_enemies):
        # Game Over

        if enemyY[i] > 466:
            for j in range(num_of_enemies):
                enemyY[j] = 1200
            show_game_over(game_overX, game_overY)
            show_restart(restartX, restartY)
        # ****
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_Change[i] = 0.6
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_Change[i] = -0.3
            enemyY[i] += enemyY_Change[i]
        # Taking An Extra Argument in this Function i
        enemy(enemyX[i], enemyY[i], i)

        # CollisionMovements
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 516
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(20, 120)
            score += 5
            # explosion_sound.play()
            # print(score)

    show_score(scoreX, scoreY)

    # Player Movements
    playerX += playerX_Change
    # Boundaries For Player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    player(playerX, playerY)

    pygame.display.update()
