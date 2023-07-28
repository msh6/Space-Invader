import pygame
import time, random, math
from pygame import mixer

# Initializing pygame
pygame.init()

# Creating game window
screen = pygame.display.set_mode((800, 600))

# Adding game intro image
intro = pygame.image.load('intro.png')
intro = pygame.transform.scale(intro,(800, 600))
screen.blit(intro,(0, 0))
pygame.display.update()
time.sleep(1.)

# Adding background
bg_img = pygame.image.load('background-min.png')
bg_img = pygame.transform.scale(bg_img,(800, 600))

# Adding BGM
mixer.music.load('bgm.wav')
mixer.music.play(-1)

# Title of the window and icon
pygame.display.set_caption("Space Invaders") 
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# adding player spaceship
player_img = pygame.image.load('spaceship.png')
player_x_cord = 370 
player_y_cord = 500
player_x_cord_change = 0

# adding aliens
enemy_img = []
enemy_x_cord = []
enemy_y_cord = []
enemy_x_cord_change = []
enemy_y_cord_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemy_x_cord.append(random.randint(0, 736))
    enemy_y_cord.append(random.randint(20, 80))
    enemy_x_cord_change.append(0.3)
    enemy_y_cord_change.append(40)

# adding bullet 
# ready - we cant see the bullet on the screen
# fire - bullet is moving  
bullet_img = pygame.image.load('bullet.png')
bullet_x_cord = 0
bullet_y_cord = 500
bullet_x_cord_change = 0
bullet_y_cord_change = 5
bullet_state = "ready"


def player(x, y):
    # drawing the image of spaceship on specific area
    # blit means to draw 
    screen.blit(player_img, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 23, y + 5))
    
# Collision Detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# Keeping Score
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score_render = score_font.render(f"Score : {str(score)}", True, (255,255,255))
    screen.blit(score_render, (x, y))
    
def game_over_text():
    game_over_msg = game_over_font.render(f"GAME OVER", True, (255,255,255))
    screen.blit(game_over_msg, (200, 250))
    
    
# Game Loop
running = True 
while running:
    
    screen.blit(bg_img,(0, 0))
     # filling the screen with color
    #screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     
    
        # checking if keystroke is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_cord_change = -0.8
            if event.key == pygame.K_RIGHT:
                player_x_cord_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x cordinate of the spaceship
                    bullet_x_cord = player_x_cord
                    fire_bullet(bullet_x_cord, bullet_y_cord)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_cord_change = 0
    
    # movement of spaceship
    player_x_cord += player_x_cord_change
    
    # making sure spaceship stays within window bounds
    if player_x_cord <= 0:
        player_x_cord = 0
    if player_x_cord >= 736:
        player_x_cord = 736
        
    # movement of alien
    for i in range(num_of_enemies):
        
        # Game Over
        if enemy_y_cord[i] > 440:
            #moving enemies out of the screen
            for j in range(num_of_enemies):
                enemy_y_cord[i] = 2000
            game_over_text()
            break
        
        enemy_x_cord[i] += enemy_x_cord_change[i]
        # making sure alien stays within window bounds
        if enemy_x_cord[i] <= 0:
            enemy_x_cord_change[i] = 0.3
            enemy_y_cord[i] += enemy_y_cord_change[i]
        if enemy_x_cord[i] >= 736:
            enemy_x_cord_change[i] = -0.3
            enemy_y_cord[i] += enemy_y_cord_change[i]
        
        # Collision
        collision = isCollision(enemy_x_cord[i], enemy_y_cord[i], bullet_x_cord, bullet_y_cord)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y_cord = 480
            bullet_state = "ready"
            score += 1
            # respawning the enemy
            enemy_x_cord[i] = random.randint(0, 736)
            enemy_y_cord[i] = random.randint(20, 80)
            
        #calling the enemy method
        enemy(enemy_x_cord[i], enemy_y_cord[i], i)
        
    # bullet movement
    if bullet_y_cord <= 0:
        bullet_y_cord = 480
        bullet_state = "ready"
         
    if bullet_state == "fire":
        fire_bullet(bullet_x_cord, bullet_y_cord)
        bullet_y_cord -= bullet_y_cord_change
    
    show_score(textX, textY)
    
    #calling the player method
    player(player_x_cord, player_y_cord)
    
    # updating the screen to see the changes
    pygame.display.update()