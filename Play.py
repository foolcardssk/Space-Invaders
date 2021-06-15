import pygame,random,math
from pygame import mixer

# icon from flaticon , font from google fonts

pygame.init()

# window creation
screen = pygame.display.set_mode((800,600))

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Icons\\space-invaders icon.png')
pygame.display.set_icon(icon)

# Background, BGM and other sounds
background = pygame.image.load('Icons\\bg-image.jpg')
mixer.music.load('Sounds\\background.wav')  # .music for bgm
mixer.music.play(-1)  # -1 arguments makes it to loop the music

bulletSound = mixer.Sound('Sounds\\laser.wav')
explosionSound = mixer.Sound('Sounds\\explosion.wav') 

# Score ---------------------------------
scoreVal = 0
font = pygame.font.Font('Fonts\\Staatliches-Regular.ttf',30)

def showScore():
    score = font.render('score : ' + str(scoreVal), True, (255,255,255))
    screen.blit(score,(10,10))

# Player --------------------------------
playerImg = pygame.image.load('Icons\\space-ship.png')
playerX = 370
playerY = 480
playerChangeX = playerChangeY = 0

def player(change):  # handles player rendering
    global playerX,playerY
    playerX += change

    # boundry
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    screen.blit(playerImg,(playerX,playerY))

# Bullet ----------------------------------
bulletImg = pygame.image.load('Icons\\bullet.png')
bulletX = 386
bulletY = 480
bulletState = 'ready'

def bullet():
    global bulletX,playerX,bulletY,bulletState
    
    if bulletY <= 0:
        bulletState = 'ready'
        bulletY = 480
    if bulletState == 'fire':
        bulletY -= 1
        screen.blit(bulletImg,(bulletX + 16,bulletY))

# Enemy ------------------------------------
enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
enemyCount = 6

for i in range(enemyCount): 
    enemyImg.append(pygame.image.load('Icons\\ufo.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))
    enemyChangeX.append(0.5) # 0.3
    enemyChangeY.append(0)


def enemy():
    global enemyX,enemyY,enemyChangeX,enemyChangeY

    for i in range(enemyCount):
        if enemyY[i] >= 440: # 440
            for j in range(enemyCount):
                enemyY[j] = 2000
            return 'over'
        elif enemyX[i] <= 0:
            enemyChangeX[i] = 0.5 # 0.3
            enemyY[i] += 20
        elif enemyX[i] >= 736:
            enemyChangeX[i] = -0.5 # 0.3
            enemyY[i] += 20

        enemyX[i] += enemyChangeX[i]
        screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))

# Collision ---------------------------------

def collision():
    global bulletX,bulletY,enemyX,enemyY,bulletState,enemyCount,scoreVal

    for i in range(enemyCount):
        if math.sqrt(math.pow((enemyX[i] - bulletX),2) + math.pow((enemyY[i]-bulletY),2)) <= 30:
            explosionSound.play()
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,150)
            bulletState = 'ready'
            bulletY = 480
            scoreVal += 1
        
# Game loop -----------------------------------------------------------------------------------------------------------------------
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))

    # cross button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movement detection
        if event.type == pygame.KEYDOWN:  # key press down
            if event.key == pygame.K_RIGHT:
                playerChangeX += 0.4
            if event.key == pygame.K_LEFT:
                playerChangeX -= 0.4
            if event.key == pygame.K_SPACE:  # For bullet launch
                bulletSound.play()
                bulletState = 'fire'
                bulletX = playerX
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerChangeX = 0

    # calling render functions
    state = enemy()
    if state == 'over':
        gameOver = pygame.font.Font('Fonts\\Staatliches-Regular.ttf',64)
        go = gameOver.render('GAME OVER', True, (255,255,255))
        screen.blit(go,(260,250))

    player(playerChangeX)
    bullet()
    collision()
    showScore()
    pygame.display.update() # update the display every time

pygame.quit() # quits pygame process