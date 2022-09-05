import pygame
import random
import RPi.GPIO as GPIO
from time import sleep
from runner_settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = BLACK
font = pygame.font.Font('freesansbold.ttf', 16)

clock = pygame.time.Clock()

GPIO.setmode(GPIO.BOARD)

button = 12
GPIO.setup(button,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Game loop
running = True

while running:
    clock.tick(FPS)

    index = 0

    if menu:
        if index == 0:
            text = font.render("               runner.py               ", True, BLACK, WHITE)
        else:
            text = font.render("               runner.py               ", True, BLACK, GREY_WHITE)
        screen.blit(text, (HW- 100, HH - 40))
        if index == 1:
            text2 = font.render("               flappy_cube.py               ", True, BLACK, WHITE)
        else:
            text2 = font.render("               flappy_cube.py               ", True, BLACK, GREY_WHITE)
        screen.blit(text2, (HW- 120, HH))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if GPIO.input(button) == 0 and index == 0 and not active:
        runner = True
        menu = False

    pygame.display.flip()

#######################################################################################################################

    if runner:
        screen.fill(background)
        score_text = font.render(f'Score: {score}', True, WHITE, BLACK)
        screen.blit(score_text, (15, 275))

        if not active:
            instruction_text = font.render('Hold "L" To Start / Restart', True, WHITE, BLACK)
            screen.blit(instruction_text, (HW - 200, HH-  50))
        else:
            instruction_text = font.render('Push L Button To Start / Restart', True, BLACK, BLACK)
            screen.blit(instruction_text, (HW - 80, HH -  50))

        hard_text = font.render(f'Twist Completely = hard mode ({hard_mode})', True, WHITE, BLACK)
        screen.blit(hard_text, (HW - 80, 250))

        goMenu_text = font.render(f'Hold "L" To Go Back To Menu ({hard_mode})', True, WHITE, BLACK)
        screen.blit(hard_text, (HW - 80, 250))

        destoryInt = 0

        floor = pygame.draw.rect(screen, (255, 255, 255), [0, 220, WIDTH, 5])
        player = pygame.draw.rect(screen, WHITE, [player_x, player_y, 15, 30])
        obstacle0 = pygame.draw.rect(screen, WHITE, [obstacles[0], 205, 15, 15])
        obstacle1 = pygame.draw.rect(screen, WHITE, [obstacles[1], 205, 15, 15])
        obstacle2 = pygame.draw.rect(screen, WHITE, [obstacles[2], 205, 15, 15])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if GPIO.input(button) == 0 and active:
            if y_change == 0:
                y_change = 20
            sleep(0.01)

        if GPIO.input(button) == 0 and not active:
            sleep(0.5)
            obstacles = [300, 450, 600]
            active = True
            obstacle_speed = 3
            score = 0

            # do not need
        if active:
            score += 3

        for i in range(len(obstacles)):
            if active:
                obstacles[i] -= obstacle_speed
                if obstacles[i] < -20:
                    obstacles[i] = random.randint(470, 570)
                if player.colliderect(obstacle0) or player.colliderect(obstacle1) or player.colliderect(obstacle2):
                    active = False

        if hard_mode:
            speed_mult = 1.5

        if player_x < 50 or player_x > 50:
            player_x = 50

        if y_change > 0 or player_y < 190:
            player_y -= y_change
            y_change -= gravity
        if player_y > 190:
            player_y = 190
        if player_y == 190 and y_change < 0:
            y_change = 0

        # SCALE GAME DIFFICULTY

        if not hard_mode:
            obstacle_speed = score / 300
        else:
            obstacle_speed = score / 150
        if obstacle_speed < 2.5:
            obstacle_speed = 2.5
        if obstacle_speed > 12 and not hard_mode:
            obstacle_speed = 12
        elif obstacle_speed > 15:
            obstacle_speed = 15

        pygame.display.flip()
pygame.QUIT
