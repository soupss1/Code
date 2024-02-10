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
    enemyX_change.append(2)
    enemyY_change.append(40)

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
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY, 2))) # Calculate the distance between the enemy and bullet
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    
    # Change Screen Color Using RGB            
    screen.fill((0 , 0 , 0))
    # Background Image
    screen.blit(background, (0, 0))
    
    # Announce Rounds
    if score_value >= 60:
        round_number = 3
    elif score_value >= 30:
        round_number = 2
        
    

    # Exit Button
    for event in pygame.event.get(): # Check All Events
        if event.type == pygame.QUIT: # If Exit Button is Pressed
            running = False # Stop Game Loop; Stop Game
  
        
        if event.type == pygame.KEYDOWN: # Check for Keystroke
            if event.key == pygame.K_LEFT: # Check if Left Arrow is Pressed
                playerX_change = -3
                
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
                
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
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
            

        enemyX[i] += enemyX_change[i] # Using [i] checks for all enemies in the game 
    
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -2
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