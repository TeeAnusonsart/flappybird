import pickle
from msilib.schema import Class
import sys
from traceback import print_tb
import pygame
import random


pygame.init()
pygame.font.init()

size = width, height = 900, 700
speed = 0
black = 0, 0, 0
gravity = 1
max_speed = 12
bird_pos_Y = 350
start=False
pipes = []
pipe_speed = -4
is_jump = False
game_over = False
score = 0
hit=False
FPS=60
bird_speed=-15
bgspeed=1.4

try:
    with open('score.dat', 'rb') as file:
        high_score = pickle.load(file)
except:
    high_score = 0



class PIPE:
    def __init__(self,x):
        self.x=x
        self.h=random.randint(100,400)
        self.passed=False


clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
background = pygame.image.load("map.png")
background = pygame.transform.scale(background,(size))
backgroundX=0
backgroundX2 = background.get_width()
bird = pygame.image.load("bird.png")
bird = pygame.transform.scale(bird, (50, 50))
pipe = pygame.image.load("pipe.png")
pipe = pygame.transform.scale(pipe, (100, 250 + random.randint(0, 50)))
timer_start = pygame.time.get_ticks()
ting = pygame.mixer.Sound("point.wav")
get_hit = pygame.mixer.Sound("hit.wav")
swoosh = pygame.mixer.Sound("swoosh.wav")
myfont = pygame.font.SysFont('Calibri', 40)


    
while True: 
    clock.tick(FPS)
    timer_end = pygame.time.get_ticks()
    deltaTime = (timer_end - timer_start) / 1000

    backgroundX -= bgspeed
    backgroundX2 -= bgspeed

    if backgroundX < background.get_width() * -1:  
        backgroundX = background.get_width()
    
    if backgroundX2 < background.get_width() * -1:
        backgroundX2 = background.get_width()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and start==False:
        start=True

    if start==True:
        if pressed[pygame.K_r] and game_over==True:
            pipes = []
            bird_pos_Y = 0
            speed = 0
            score = 0
            pipe_speed = -3
            game_over = False
            hit=False
            bgspeed=1.4
        


        if bird_pos_Y >= height-50:
            speed = 0
            game_over = True

        if pressed[pygame.K_SPACE] and not game_over:
            if is_jump == False:
                if speed >= 0:
                    speed = bird_speed
                    is_jump = True
                    pygame.mixer.Sound.play(swoosh)

        else:
            is_jump = False
        
            if bird_pos_Y >= height-50:
                speed = 0
                game_over = True

        bird_pos_Y += speed
        speed += gravity

        if speed >= max_speed:
            speed = max_speed
        

        if (deltaTime > 3):
            pipes.append(PIPE(width + random.randint(0, 200)))
            timer_start = timer_end

        for i in range(len(pipes)):
            pipes[i].x += pipe_speed

        for p in pipes:
            if p.x >= 160 - 100 and p.x <= 160 + 100 - 50:
                if bird_pos_Y >= height - p.h - 40 or bird_pos_Y <= height - p.h - 210:
                    game_over = True
            if p.x <= 160 - 25 and p.passed == False:
                score += 1
                pygame.mixer.Sound.play(ting)
                p.passed = True
            if game_over:
                pipe_speed = 0
            if p.x <= -100:
                pipes.remove(p)
        
        if hit==False and game_over==True:
            pygame.mixer.Sound.play(get_hit)
            hit=True
    
        screen.fill(black)  
        screen.blit(background,(0,0))

        screen.blit(background, (backgroundX, 0))
        screen.blit(background, (backgroundX2, 0))
        bird_render = pygame.transform.rotate(bird, -30*speed/max_speed)
        screen.blit(bird_render, (160, bird_pos_Y))


        for _ in pipes:
            pipe_i = pygame.transform.scale(pipe, (100, _.h))
            flipped = pygame.transform.flip(pipe_i, False, True)
            flipped = pygame.transform.scale(flipped, (100,height - _.h-200))
            screen.blit(pipe_i, (_.x, height - _.h))
            screen.blit(flipped, (_.x, 0))

        scoreText = myfont.render(f'Score: {score}', False, (0, 0, 0))
        screen.blit(scoreText,(0,0))
        highscoreText = myfont.render(f'HighScore: {high_score}', False, (0, 0, 0))
        screen.blit(highscoreText,(650,0))
        if(game_over):
            GameOverText = myfont.render('Game Over, press R to restart', False, (0, 0, 0))
            screen.blit(GameOverText,((width-GameOverText.get_width())/2,height/2))
            speed=0
            bgspeed=0
            if score > high_score:
                high_score=score
                with open('score.dat', 'wb') as file:
                    pickle.dump(score, file)
            

    if start==False:
        screen.fill(black)  
        screen.blit(background,(0,0))
        Menutext = myfont.render('Press spacebar to start', False, (0, 0, 0))
        screen.blit(Menutext,((width-Menutext.get_width())/2,height/2))

    pygame.display.flip()