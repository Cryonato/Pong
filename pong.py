import pygame 
import os
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500
WIDTH, HEIGHT = 15, 80

FPS = 60
SPEED = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


TEXT_FONT = pygame.font.SysFont("comicsans", 40)

POINT_1 = pygame.USEREVENT + 1
POINT_2 = pygame.USEREVENT + 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


pygame.display.set_caption("Pong Game")

def handle_player_motion(p1, p2):
    keys = pygame.key.get_pressed()
    #Player left movements
    if keys[pygame.K_w] and p1.y > 0:
        p1.y = p1.y - SPEED
    if keys[pygame.K_s] and p1.y + HEIGHT < SCREEN_HEIGHT:
        p1.y = p1.y + SPEED
    #Player right movements
    if keys[pygame.K_UP] and p2.y > 0:
        p2.y = p2.y - SPEED
    if keys[pygame.K_DOWN] and p2.y + HEIGHT < SCREEN_HEIGHT:
        p2.y = p2.y + SPEED
    
def handle_pong_movement(pong, vector, p1, p2, delay):
    x_speed = vector[0]
    y_speed = vector[1]
    
    #Handling colision with walls
    if (pong.y + y_speed < 0):
        y_speed = -y_speed
    if (pong.y + y_speed > SCREEN_HEIGHT - 20):
        y_speed = -y_speed
    
    
    #Handling point system
    if (pong.x < 0):
        pong.x = SCREEN_WIDTH/2
        pong.y = SCREEN_HEIGHT/2
        pygame.event.post(pygame.event.Event(POINT_1))
        
    if (pong.x > SCREEN_WIDTH - WIDTH):
        pong.x = SCREEN_WIDTH/2
        pong.y = SCREEN_HEIGHT/2
        pygame.event.post(pygame.event.Event(POINT_2))
    
    pong.x = pong.x + x_speed
    pong.y = pong.y + y_speed
    
    #Timedelay for bug fix
    current_time = pygame.time.get_ticks()
    
    if (current_time - delay["last_bounce"] > delay["delay_time"]):
        #Handling player colision
        if (pong.colliderect(p1)):
            delay["last_bounce"] = current_time
            variable = random.randint(-20, 20)
            y_speed += variable/10
            x_speed = abs(x_speed)
            
        if (pong.colliderect(p2)):
            delay["last_bounce"] = current_time
            variable = random.randint(-20, 20)
            y_speed += variable/10
            x_speed = -abs(x_speed)
    
    vector[0] = x_speed
    vector[1] = y_speed
    
#drawing the window
def draw_window(p1, p2, pong, score_1, score_2):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, BACKGROUND)
    pygame.draw.rect(screen, WHITE, p1)
    pygame.draw.rect(screen, WHITE, p2)
    pygame.draw.rect(screen, WHITE, pong)
    
    score_text = TEXT_FONT.render(
        str(score_1), 1, WHITE
    )
    screen.blit(score_text, (SCREEN_WIDTH/6, 50))

    score_text = TEXT_FONT.render(
        str(score_2), 1, WHITE
    )
    screen.blit(score_text, (SCREEN_WIDTH * 3/4, 50))
    
    pygame.display.update()
    
def main():
    run = True
    
    #Moving player characters
    p1 = pygame.Rect(20, 40, WIDTH, HEIGHT)
    p2 = pygame.Rect(SCREEN_WIDTH - WIDTH - 20, 40, WIDTH, HEIGHT)
    
    score_1 = 0
    score_2 = 0
    vector = [10, 6]
    
    delay = {
        'last_bounce': 0,    # Time of the last bounce
        'delay_time': 200    # Delay time in milliseconds
    }
    pong = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 20, 20)
    
    clock = pygame.time.Clock() 
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == POINT_1:
                score_1 += 1
                vector = [10, 6]

            if event.type == POINT_2:
                score_2 += 1
                vector = [10, 6]
                
            
                    
        handle_player_motion(p1, p2)
        handle_pong_movement(pong, vector, p1, p2, delay)
        draw_window(p1, p2, pong, score_1, score_2)

    pygame.quit()
    

if __name__ == "__main__":
    main()