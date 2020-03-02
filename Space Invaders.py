import math, random, pygame
from pygame import mixer


def enemyMovement():  # RUCH PRZECIWNIKOW
    global bulletY, score_value, bullet_state, secondBullet_state, secondBulletY, second_score_value

    for i in range(num_of_enemies):
        if enemyY[i] >= playerY - 30:  # GAME OVER PRZY DOTKNIECIU GRACZA
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameoverSound = mixer.Sound("gameover.wav")
            gameoverSound.set_volume(0.12)
            gameoverSound.play()
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # "SCHODZENIE" W DOL
            if score_value >= 110 or second_score_value >= 110:
                enemyX_change[i] = 12
            elif score_value >= 75 or second_score_value >= 75 and second_score_value < 110 and score_value < 110:
                enemyX_change[i] = 10
            elif score_value >= 50 or second_score_value >= 50 and second_score_value < 75 and score_value < 75:
                enemyX_change[i] = 8
            elif score_value >= 25 or second_score_value >= 25 and second_score_value < 50 and score_value < 50:
                enemyX_change[i] = 6
            elif score_value >= 10 or second_score_value >= 10 and second_score_value < 25 and score_value < 25:
                enemyX_change[i] = 5
            else:
                enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 64:
            if score_value >= 110 or second_score_value >= 110:
                enemyX_change[i] = -12
            elif score_value >= 75 or second_score_value >= 75 and second_score_value < 110 and score_value < 110:
                enemyX_change[i] = -10
            elif score_value >= 50 or second_score_value >= 50 and second_score_value < 75 and score_value < 75:
                enemyX_change[i] = -8
            elif score_value >= 25 or second_score_value >= 25 and second_score_value < 50 and score_value < 50:
                enemyX_change[i] = -6
            elif score_value >= 10 or second_score_value >= 10 and second_score_value < 25 and score_value < 25:
                enemyX_change[i] = -5
            else:
                enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        # KOLIZJA
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        secondCollision = isCollision(enemyX[i], enemyY[i], secondBulletX, secondBulletY)
        if collision:
            explosionSound = mixer.Sound("invaderkilled.wav")
            explosionSound.set_volume(0.10)
            explosionSound.play()
            bulletY = int(playerY - 10)
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        if secondCollision:
            explosionSound = mixer.Sound("invaderkilled.wav")
            explosionSound.set_volume(0.10)
            explosionSound.play()
            secondBulletY = int(secondPlayerY - 10)
            secondBullet_state = "ready"
            second_score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        if i % 3 == 0:
            if enemyX_change[i] > 0:
                screen.blit(enemyImg, (enemyX[i], enemyY[i]))
            elif enemyX_change[i] < 0:
                screen.blit(enemyImg2, (enemyX[i], enemyY[i]))
        elif i % 3 == 1:
            if enemyX_change[i] > 0:
                screen.blit(enemyImg3, (enemyX[i], enemyY[i]))
            elif enemyX_change[i] < 0:
                screen.blit(enemyImg4, (enemyX[i], enemyY[i]))
        elif i % 3 != 0 and i % 3 != 1:
            if enemyX_change[i] > 0:
                screen.blit(enemyImg2, (enemyX[i], enemyY[i]))
            elif enemyX_change[i] < 0:
                screen.blit(enemyImg, (enemyX[i], enemyY[i]))


def playerAnimation():  # RUCH I ANIMACJA GRACZA
    global playerX, playerX_change, player
    player = screen.blit(playerImg, (int(playerX), int(playerY)))
    playerX += playerX_change
    if playerX <= screen_width / 2 + 16:
        playerX = screen_width / 2 + 16
    elif playerX >= int(screen_width - 64):
        playerX = int(screen_width - 64)


def secondPlayerAnimation():  # RUCH I ANIMACJA GRACZA2
    global secondPlayerX, secondPlayerX_change, secondPlayer
    secondPlayer = screen.blit(secondPlayerImg, (int(secondPlayerX), int(secondPlayerY)))
    secondPlayerX += secondPlayerX_change
    if secondPlayerX <= 0:
        secondPlayerX = 0
    elif secondPlayerX >= int(screen_width / 2 - 64):
        secondPlayerX = int(screen_width / 2 - 64)


def show_score(x, y):  # RENDEROWANIE WYNIKU
    playerOne = font.render("Player 1", True, (255, 255, 255))
    score = font.render("" + str(score_value), True, (255, 255, 255))
    playerTwo = font.render("Player 2", True, (255, 255, 255))
    second_score = font.render("" + str(second_score_value), True, (255, 255, 255))
    screen.blit(second_score, (int(screen_width / 4), 65))
    screen.blit(playerOne, (int(screen_width / 4 - 58), 15))
    screen.blit(playerTwo, (int(3 * screen_width / 4 - 58), 15))
    screen.blit(score, (int(3 * screen_width / 4), 65))


def game_over_text():  # RENDEROWANIE TEXTU GAMEOVER
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    if second_score_value > score_value:
        winner = over_font.render(("PLAYER 1 WINS"), True, (255, 215, 0))
        score_text = over_font.render(str(second_score_value), True, (255, 255, 255))
        draw = over_font.render((""), True, (255, 215, 0))
    elif score_value > second_score_value:
        winner = over_font.render(("PLAYER 2 WINS"), True, (255, 215, 0))
        score_text = over_font.render(str(score_value), True, (255, 255, 255))
        draw = over_font.render((""), True, (255, 215, 0))
    else:
        draw = over_font.render(("DRAW"), True, (255, 215, 0))
        winner = over_font.render("", True, (255, 255, 255))
        score_text = over_font.render("", True, (255, 255, 255))

    screen.blit(winner, (130, 210))
    screen.blit(draw, (int(screen_width / 2 - 100), 210))
    screen.blit(score_text, (int(screen_width / 2 - 18), 280))
    screen.blit(over_text, (200, 120))


def fire_bullet(x, y):  # WYSTRZELENIE POCISKU
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x + 16), int(y + 10)))


def second_fire_bullet(x, y):  # WYSTRZELENIE POCISKU
    global secondBullet_state
    secondBullet_state = "fire"
    screen.blit(secondBulletImg, (int(x + 16), int(y + 10)))


def bulletMovement():  # RUCH POCISKU
    global bulletY, bulletX, bulletY_change, bullet_state
    if bulletY <= 0:
        bulletY = int(playerY - 10)
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


def secondBulletMovement():  # RUCH POCISKU
    global secondBulletY, secondBulletX, secondBulletY_change, secondBullet_state
    if secondBulletY <= 0:
        secondBulletY = int(secondPlayerY - 10)
        secondBullet_state = "ready"
    if secondBullet_state == "fire":
        second_fire_bullet(secondBulletX, secondBulletY)
        secondBulletY -= secondBulletY_change


def isCollision(enemyX, enemyY, bulletX, bulletY):  # KOLIZJA
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Inicjalizacja gry
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
font = pygame.font.Font('Retro Gaming.ttf', 32)
mixer.music.load("soundtrack.wav")
mixer.music.set_volume(1.4)
mixer.music.play(-1)

# Ustawienia ekranu
screen_width = 800
screen_hight = 600
screen = pygame.display.set_mode((screen_width, screen_hight))
background = pygame.image.load("background.png")

# Gracz
playerImg = pygame.image.load('player.png')
playerX = 3 * screen_width / 4 - 16
playerY = screen_hight / 2 + 220
playerX_change = 0
# Gracz2
secondPlayerImg = pygame.image.load('player2.png')
secondPlayerX = screen_width / 4 - 16
secondPlayerY = screen_hight / 2 + 220
secondPlayerX_change = 0

# Enemy
enemyImg = pygame.image.load('alien.png')
enemyImg2 = pygame.image.load('alien2.png')
enemyImg3 = pygame.image.load('alien3.png')
enemyImg4 = pygame.image.load('alien4.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 28

x = random.randint(0, screen_width - 64)
y = random.randint(0, screen_hight / 4)

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(0, screen_hight / 4))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Pocisk
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY - 10
bulletY_change = 10
bullet_state = "ready"
# Pocisk2
secondBulletImg = pygame.image.load('bullet2.png')
secondBulletX = secondPlayerX
secondBulletY = secondPlayerY - 10
secondBulletY_change = 10
secondBullet_state = "ready"

score_value = 0
second_score_value = 0
over_font = pygame.font.Font('Retro Gaming.ttf', 64)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_a:
                secondPlayerX_change -= 5
            if event.key == pygame.K_d:
                secondPlayerX_change += 5
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("shoot.wav")
                    bulletSound.set_volume(0.12)
                    bulletSound.play()
                    bulletX = int(playerX)
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_w:
                if secondBullet_state == "ready":
                    secondBulletSound = mixer.Sound("shoot.wav")
                    secondBulletSound.set_volume(0.12)
                    secondBulletSound.play()
                    secondBulletX = int(secondPlayerX)
                    second_fire_bullet(secondBulletX, secondBulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change += 5
            if event.key == pygame.K_RIGHT:
                playerX_change -= 5
            if event.key == pygame.K_a:
                secondPlayerX_change += 5
            if event.key == pygame.K_d:
                secondPlayerX_change -= 5

    screen.fill((0, 0, 0))
    screen.blit(background, [0, 0])

    playerAnimation()
    secondPlayerAnimation()
    bulletMovement()
    secondBulletMovement()
    enemyMovement()

    show_score(10, 10)
    pygame.display.flip()
    clock.tick(60)
