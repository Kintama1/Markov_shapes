import pygame
import time
import random

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Markov shapes")

SHAPE_WIDTH = 40
SHAPE_HEIGHT = 60
SHAPE_VELOCITY = 5
ROTATION_ANGLE = 0
FPS = 60
SPAWN_DELAY= 5

def draw(shape,shapes_list):
    WIN.fill((255,255,255))
    for position, angle in shapes_list:
        old_shape_surface = pygame.Surface((SHAPE_WIDTH,SHAPE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(old_shape_surface,(141,171,206),(0,0,SHAPE_WIDTH,SHAPE_HEIGHT) )
        old_rotated_surface = pygame.transform.rotate(old_shape_surface, angle)
        old_rotated_rect = old_rotated_surface.get_rect(center = position.center)
        WIN.blit(old_rotated_surface,old_rotated_rect.topleft)
    #Manipulating current shape
    #Creating a surface for the shape
    shape_surface = pygame.Surface((SHAPE_WIDTH,SHAPE_HEIGHT), pygame.SRCALPHA) #WILL HAVE TO MODULARIZE THIS
    pygame.draw.rect(shape_surface,(141,171,206),(0,0,SHAPE_WIDTH,SHAPE_HEIGHT) )
    #rotating the shape surface
    rotated_surface = pygame.transform.rotate(shape_surface, ROTATION_ANGLE)
    rotated_rect = rotated_surface.get_rect(center= shape.center)

    #drawing of a rectangle
    WIN.blit(rotated_surface, rotated_rect.topleft)
    pygame.display.update()
    

def main():
    global ROTATION_ANGLE
#main game loop
    clock = pygame.time.Clock()
    running = True
    shape = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
    #Will store a list of all the shapes after the 
    shapes_list = []
    last_spawn_time = time.time()
    #a while loop that updates each frame of the game
    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the close button is clicked, close the game
                running = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and shape.x - SHAPE_VELOCITY >= 0:
            shape.x -= SHAPE_VELOCITY
        if keys[pygame.K_RIGHT] and shape.x + SHAPE_VELOCITY + SHAPE_WIDTH  <= WIDTH:
            shape.x += SHAPE_VELOCITY
        if keys[pygame.K_UP] and shape.y - SHAPE_VELOCITY >= 0:
            shape.y -= SHAPE_VELOCITY
        if keys[pygame.K_DOWN] and shape.y + SHAPE_VELOCITY + SHAPE_HEIGHT <= HEIGHT:
            shape.y += SHAPE_VELOCITY
        if keys[pygame.K_a]:
            ROTATION_ANGLE += SHAPE_VELOCITY 
        if keys[pygame.K_d]:
            
            ROTATION_ANGLE -= SHAPE_VELOCITY 
        if current_time - last_spawn_time > SPAWN_DELAY:
            shapes_list.append((shape, ROTATION_ANGLE))
            shape = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
            ROTATION_ANGLE = 0
            last_spawn_time = current_time
        draw(shape, shapes_list)
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":

    main()