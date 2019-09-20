import pygame
import sys
import random
import time
from pygame.locals import *
from pygame.math import Vector2

pygame.init()
mainclock = pygame.time.Clock()

WINDOWHEIGHT = 500
WINDOWWIDTH = 700
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong')
#Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#win/lose screens
font = pygame.font.Font(None, 60)
sfont = pygame.font.Font(None, 30)
def wingame():
    pygame.mixer_music.load('Congratulations.mp3')
    pygame.mixer.music.play(-1, 0.0)
    window.fill(BLACK)
    while True:
        text = font.render('You Won!', 1, WHITE)
        window.blit(text, (5, 10))
        stext = sfont.render('Play Again? y/n', 1, WHITE)
        window.blit(stext, (100, 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.mixer.music.stop()
                    pygame.mixer_music.load('Background.mid')
                    pygame.mixer.music.play(-1,0.0)
                    return
                elif event.key == K_n or event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

#I suggest not losing
def losegame():
    pygame.mixer_music.load('GameOver.mp3')
    pygame.mixer.music.play(-1, 0.0)
    window.fill(BLACK)
    while True:
        text = font.render("YOU LOST", 1, RED)
        window.blit(text, (0, 0))
        stext = sfont.render("Play Again y/n", 1, WHITE)
        window.blit(stext, (100, 100))
        pygame.display.update()
        for event in pygame.event.get():
           if event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.mixer.music.stop()
                    pygame.mixer_music.load('Background.mid')
                    pygame.mixer.music.play(-1,0.0)
                    return
                elif event.key == K_n or event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

MOVESPEED = 20
ball_movement = Vector2(10,10)

#Paddle images
enemy = pygame.Rect( 0, 175, 20, 60)
enemy2 = pygame.Rect( 175, 0, 60, 20)
enemy3 = pygame.Rect( 175, 480, 60, 20)
enemy_image = pygame.image.load('Green.png')
enemy_fixed_image = pygame.transform.scale(enemy_image, (20,60))
enemy_fixed_image2 = pygame.transform.scale(enemy_image, (60, 20))
player = pygame.Rect( 680, 175, 20, 60)
player2 = pygame.Rect( 700-175, 0, 60, 20)
player3 = pygame.Rect( 700-175, 480, 60, 20)
player_image = pygame.image.load('Green.png')
player_fixed_image = pygame.transform.scale(player_image, (20,60))
player_fixed_image2 = pygame.transform.scale(player_image,(60,20))

#Vertical Line
mid1 = {'rect' : pygame.Rect(340, 25, 10, 50), 'color' :WHITE}
mid2 = {'rect' : pygame.Rect(340, 125, 10, 50), 'color' :WHITE}
mid3 = {'rect' : pygame.Rect(340, 225, 10, 50), 'color' :WHITE}
mid4 = {'rect' : pygame.Rect(340, 325, 10, 50), 'color' :WHITE}
mid5 = {'rect' : pygame.Rect(340, 425, 10, 50), 'color' :WHITE}
middle = [mid1, mid2, mid3, mid4, mid5]
#setting up the ball
ball = {'rect' :pygame.Rect(340, 220, 10, 10), 'color' :GREEN, 'vel' :Vector2(-ball_movement[0], -ball_movement[1])}
balls = [ball]

for b in balls:
    r = b['rect']
    v = b['vel']
    r.left += v[0]
    r.top += v[1]
    pygame.draw.rect(window, b['color'], b['rect'])


#sounds
pygame.mixer_music.load ('background.mid')
boop = pygame.mixer.Sound('Boop.wav')
lose = pygame.mixer.Sound('Lose.wav')
win = pygame.mixer.Sound('Win.wav')
pygame.mixer.music.play(-1,0.0)
#scores
pscore = 0
ptruescore = 0
cscore = 0
ctruescore = 0

#keyboard variables
move_down = False
move_up = False
move_left = False
move_right = False

randir = random.randint(0, 3)
if randir == 0:
    v[0] *= -1
    v[1] *= -1
if randir == 1:
    v[0] *= -1
if randir == 2:
    v[1] *= -1


#game loop
while True:
    #key input check
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == K_s:
                move_up = False
                move_down = True
            if event.key == K_LEFT or event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == K_d:
                move_left = False
                move_right = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False
                if event.key == K_m:
                    if music_playing:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    muscic_playing = not music_playing
        window.fill(BLACK)

        for b in balls:
            r = b['rect']
            v = b['vel']
            r.left += v[0]
            r.top += v[1]
            #enemy gets a point, reset board
            if r.left < 0 or ((r.top < 0 or r.bottom > WINDOWHEIGHT) and r.left + 5 < 350):

                pscore += 1
                if pscore >= 11 and pscore > cscore + 1:
                    win.play()
                    pscore = 0
                    cscore = 0
                    ptruescore += 1
                balls.remove(b)
                ball = {'rect': pygame.Rect(340, 220, 10, 10), 'color': GREEN,
                        'vel': Vector2(-ball_movement[0], -ball_movement[1])}
                balls = [ball]
                for b in balls:
                    v = b['vel']
                randir = random.randint(0, 3)
                if randir == 0:
                    v[0] *= -1
                    v[1] *= -1
                if randir == 1:
                    v[0] *= -1
                if randir == 2:
                    v[1] *= -1

            #Player gets a point, reset board
            if r.right > WINDOWWIDTH or ((r.top < 0 or r.bottom > WINDOWHEIGHT) and r.left +5 >= 350):

                cscore += 1
                if cscore >= 11 and cscore > pscore + 1:
                    lose.play()
                    cscore = 0
                    pscore = 0
                    ctruescore +=1
                balls.remove(b)
                ball = {'rect': pygame.Rect(340, 220, 10, 10), 'color': GREEN,
                        'vel': Vector2(-ball_movement[0], -ball_movement[1])}
                balls = [ball]
                for b in balls:
                    v = b['vel']
                randir = random.randint(0, 3)
                if randir == 0:
                    v[0] *= -1
                    v[1] *= -1
                if randir == 1:
                    v[0] *= -1
                if randir == 2:
                    v[1] *= -1

            #Reverse horitzontal direction when collision detected
            if player.colliderect(r) or enemy.colliderect(r):
                boop.play()
                v[0] *= -1
            if player2.colliderect(r) or  player3.colliderect(r) or enemy2.colliderect(r) or enemy3.colliderect(r):
                boop.play()
                v[1] *= -1

            pygame.draw.rect(window, b['color'], b['rect'])

        #enemy movement logic
        if r.top > enemy.top and enemy.bottom < WINDOWHEIGHT:
            enemy.top += MOVESPEED/2
        else:
            enemy.bottom -= MOVESPEED/2
        if r.left < enemy2.left and enemy2.left > 0:
            enemy2.left -= MOVESPEED/2
            enemy3.left -= MOVESPEED/2
        elif enemy2.right < 350:
            enemy2.left += MOVESPEED/2
            enemy3.left += MOVESPEED/2

        #player movement logic
        if move_down and player.bottom < WINDOWHEIGHT:
            player.top += MOVESPEED
        if move_up and player.top > 0:
            player.bottom -= MOVESPEED
        if move_left and player2.left > 350:
            player2.left -= MOVESPEED
            player3.left -= MOVESPEED
        if move_right and player2.right < WINDOWWIDTH:
            player2.right += MOVESPEED
            player3.right += MOVESPEED

        for m in middle:
            pygame.draw.rect(window, m['color'], m['rect'])
        window.blit(player_fixed_image, player)
        window.blit(player_fixed_image2, player2)
        window.blit(player_fixed_image2, player3)
        window.blit(enemy_fixed_image, enemy)
        window.blit(enemy_fixed_image2, enemy2)
        window.blit(enemy_fixed_image2, enemy3)
        efont = pygame.font.Font(None, 30)
        etext = efont.render(str(cscore) + '|' + str(ctruescore), 1, GREEN)
        window.blit(etext,(150, 250))
        pfont = pygame.font.Font(None, 30)
        ptext = pfont.render(str(pscore) + '|' + str(ptruescore), 1, GREEN)
        window.blit(ptext,(520, 250))

        if ptruescore == 3:
            ptruescore = 0
            ctruescore = 0
            pygame.mixer.music.stop()
            wingame()
        if ctruescore == 3:
            ptruescore = 0
            ctruescore = 0
            pygame.mixer.music.stop()
            losegame()




        pygame.display.update()
        mainclock.tick(40)
