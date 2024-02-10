from calendar import c
import pygame
import random
import math
import time
from pygame import mixer


# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background1.png')

# Background Souns
mixer.music.load('background.wav') # mixer.music for longer sounds like background music
mixer.music.play(-1) # Makes music play on a loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Speed Variables
enemySpeed = 2
enemyTwoSpeed = 1
playerSpeed = 3

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0 # Player Speed

# Enemy
enemyImg = [] # Create an empty list
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies): # Creates however many enemies specified in the num_of_enemies variable
    enemyImg.append(pygame.image.load('alien.png')) # Instead of = using .append stores it in the empty list
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemySpeed)
    enemyY_change.append(40)
    
# Enemy 2
enemy2Img = [] 
enemy2X = []
enemy2Y = []
enemy2X_change = []
enemy2Y_change = []
enemy_2_health = []
num_of_enemie2 = 3

for i in range(num_of_enemie2): 
    enemy2Img.append(pygame.image.load('alien2.png')) 
    enemy2X.append(random.randint(0, 736))
    enemy2Y.append(random.randint(50, 150))
    enemy2X_change.append(enemyTwoSpeed)
    enemy2Y_change.append(100)
    enemy_2_health.append(3)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 9
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Round
round_number = 1


def round_text(round):
    round_text = font.render("Round " + str(round), True, (255, 255, 255)) # Renders the text
    screen.blit(round_text, (660, 10)) # Draws text on the screen

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255)) # Renders the text
    screen.blit(over_text, (200, 250)) # Draws text on the screen

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y)) # Draw Image on Screen
    

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) 
    
def enemy2(x, y, i):
    screen.blit(enemy2Img[i], (x, y)) 
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(x, y, bulletX, bulletY):
    distance = math.sqrt((math.pow(x - bulletX,2)) + (math.pow(y - bulletY, 2))) # Calculate the distance between the enemy and bullet
    if distance < 27:
        return True
    else:
        return False
    
def kill_enemies():
    for j in range(num_of_enemies): # Runs for as many enemies 
        enemyY[j] = 2000 # Moves enemies off screen
                    
    for z in range(num_of_enemie2):
        enemy2Y[z] = 2000
    
    
#def gameOver(y):

    #if int(y) > 440:
        #for j in range(num_of_enemies):
            #enemyY[j] = 2000
        #for v in range(num_of_enemie2):
            #enemyY[v] = 2000
        #game_over_text()
        #return True
    #else:
        #return False

# Game Loop
running = True
while running:
    
    # Change Screen Color Using RGB            
    screen.fill((0 , 0 , 0))
    # Background Image
    screen.blit(background, (0, 0))
    
    # Announce Rounds
    if score_value >= 60: # Else if statement with the larger value on top so it prioritizes the higher value when running the code top to bottom
        round_number = 3
    elif score_value >= 30: # When score value reaches this number it enters the next phase
        for i in range(num_of_enemie2):
            # Game Over
            #gameOverCheck = gameOver(enemy2Y)
            #if gameOverCheck == True:
                #break

            if enemy2Y[i] > 440: # Checks if enemy 2 crossese the players border
                kill_enemies()
                game_over_text()
                break
            
            
            enemy2X[i] += enemy2X_change[i] 
    
            if enemy2X[i] <= 0:
                enemy2X[i] = 0
                enemy2X_change[i] = enemyTwoSpeed
                enemy2Y[i] += enemy2Y_change[i]

            elif enemy2X[i] >= 740:
                enemy2X[i] = 740
                enemy2X_change[i] = -enemyTwoSpeed
                enemy2Y[i] += enemy2Y_change[i]
        
        
            # Collision
            bullet_collision2 = isCollision(enemy2X[i], enemy2Y[i], bulletX, bulletY) # Checks for collision
            
            if bullet_collision2: # If collision is True
                
                enemy_2_health[i] -= 1 # Lower the enemy health by one
                
                print (enemy_2_health)
                if enemy_2_health[i] == 0: # If enemy health is zero 
                    
                    bullet_state = "ready"
                    bulletY = 480 # Reset bullet is to starting point
                    explosion_sound = mixer.Sound("explosion.wav") # Loads sound from files and stores it in a variable
                    explosion_sound.play() # Plays sound
                    score_value += 3 # Points for this enemy
                    # "Respawn" Enemy by reseting it's position back to the random starting locations
                    enemy2X[i] = random.randint(0, 732)
                    enemy2Y[i] = random.randint(50, 150)
                    enemy_2_health[i] = 3 # Reset health back to original
                else:
                    bullet_state = "ready"
                    bulletY = 480 # Reset bullet is to starting point
                    explosion_sound = mixer.Sound("bloop.wav") # Play sound affect to alert the player that they hit their target
                    explosion_sound.play()
            enemy2(enemy2X[i], enemy2Y[i], i)
                    
        round_number = 2 # Change the round number at the top left of the screen
        num_of_enemies = 7 # Change number of enemy1 in second phase
        
        

        
    

    # Exit Button
    for event in pygame.event.get(): # Check All Events
        if event.type == pygame.QUIT: # If Exit Button is Pressed
            running = False # Stop Game Loop; Stop Game
  
        
        if event.type == pygame.KEYDOWN: # Check for Keystroke
            if event.key == pygame.K_LEFT: # Check if Left Arrow is Pressed
                playerX_change = -playerSpeed
                
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
                
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav") # Sound is used for shorter sound effects like shooting a bullet
                    bullet_sound.play()
                    bulletX = playerX # Stores the position of the players X value when bullet is shot
                    fire_bullet(bulletX, playerY) # Since bulletX's value isn't changing the x value of the bullet will stop following the player
                    

                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Spaceship boundries
    playerX += playerX_change
    
    if playerX <= 0: # Checks if Player x-value Goes Below Zero (Offscreen)
        playerX = 0 # Resets PlayerX Position Back to Zero
    elif playerX >= 736:# Using 736 instead of 800 because spaceship png is 64px (800 - 64 = 736)
        playerX = 736
        
    # Enemy Movement
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 440:
            kill_enemies()
            game_over_text()
            break
            

        enemyX[i] += enemyX_change[i] # Using [i] checks for all enemies in the game 
    
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = enemySpeed
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -enemySpeed
            enemyY[i] += enemyY_change[i]
            
            # Collision
        bullet_collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY) # Checks for collision
        if bullet_collision: # If collision is True
            explosion_sound = mixer.Sound("explosion.wav") # Loads sound from files and stores it in a variable
            explosion_sound.play() # Plays sound
            bulletY = 480 # Reset bullet is to starting point
            bullet_state = "ready" 
            score_value += 1
            # "Respawn" Enemy by reseting it's position back to the random starting locations
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

           
    
    # Bullet Moovemnet 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        temp = 0
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        

    round_text(round_number)    
    show_score(textX, textY)
    player(playerX, playerY) 
    pygame.display.update() # Update Screen
