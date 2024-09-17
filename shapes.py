import pygame
import time
from Markov_shapes import MarkovShape


WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Markov shapes")

SHAPE_WIDTH = 40
SHAPE_HEIGHT = 60
SHAPE_VELOCITY = 5
ROTATION_ANGLE = 0
FPS = 60
SPAWN_DELAY= 5

shapes_matrix = {
        "rect" :{"rect": 0.25,"circle":0.25, "triangle": 0.25, "arc": 0.25},
        "circle" :{"rect":0.25, "triangle": 0.25, "arc": 0.25,"circle":0.25,},
        "triangle" :{"rect":0.25, "circle": 0.25, "arc": 0.25,"triangle": 0.25},
        "arc" :{"rect":0.25, "circle": 0.25, "triangle": 0.25,"arc": 0.25}
    }
shapes = MarkovShape(shapes_matrix)
shapes_list = shapes.shape_sequence(length= 20)

def draw(current_shape,shape_rect,old_shapes_list,shapes):
    WIN.fill((255,255,255))
    #drawing all the old shapes
    for shape, position, angle in old_shapes_list:
        old_shape_surface = pygame.Surface((SHAPE_WIDTH,SHAPE_HEIGHT), pygame.SRCALPHA)
        shapes.shape_switchboard(shape,old_shape_surface,position) #this will be the switchboard drawer
        old_rotated_surface = pygame.transform.rotate(old_shape_surface, angle)
        old_rotated_rect = old_rotated_surface.get_rect(center = position.center)
        WIN.blit(old_rotated_surface,old_rotated_rect.topleft)
    #Manipulating current shape
    #Creating a surface for the shape
    shape_surface = pygame.Surface((SHAPE_WIDTH,SHAPE_HEIGHT), pygame.SRCALPHA) #WILL HAVE TO MODULARIZE THIS
    shapes.shape_switchboard(current_shape,shape_surface,shape_rect)
    #rotating the shape surface
    rotated_surface = pygame.transform.rotate(shape_surface, ROTATION_ANGLE)
    rotated_rect = rotated_surface.get_rect(center= shape_rect.center)

    #drawing of a rectangle
    WIN.blit(rotated_surface, rotated_rect.topleft)
    pygame.display.update()
    
def key_moves(shape_rect):
    global ROTATION_ANGLE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and shape_rect.x - SHAPE_VELOCITY >= 0:
        shape_rect.x -= SHAPE_VELOCITY
    if keys[pygame.K_RIGHT] and shape_rect.x + SHAPE_VELOCITY + SHAPE_WIDTH  <= WIDTH:
        shape_rect.x += SHAPE_VELOCITY
    if keys[pygame.K_UP] and shape_rect.y - SHAPE_VELOCITY >= 0:
        shape_rect.y -= SHAPE_VELOCITY
    if keys[pygame.K_DOWN] and shape_rect.y + SHAPE_VELOCITY + SHAPE_HEIGHT <= HEIGHT:
        shape_rect.y += SHAPE_VELOCITY
    if keys[pygame.K_a]:
        ROTATION_ANGLE += SHAPE_VELOCITY 
    if keys[pygame.K_d]:
        ROTATION_ANGLE -= SHAPE_VELOCITY 
    return shape_rect

def main():
    global ROTATION_ANGLE

    shapes_matrix = {
        "rect" :{"rect": 0.25,"circle":0.25, "triangle": 0.25, "arc": 0.25},
        "circle" :{"rect":0.25, "triangle": 0.25, "arc": 0.25,"circle":0.25,},
        "triangle" :{"rect":0.25, "circle": 0.25, "arc": 0.25,"triangle": 0.25},
        "arc" :{"rect":0.25, "circle": 0.25, "triangle": 0.25,"arc": 0.25}
    }
    shapes = MarkovShape(shapes_matrix)
    shapes_list = shapes.shape_sequence(length= 20)
    print(shapes_list)

    #main game loop
    shape_idx = 0
    current_shape = shapes_list[shape_idx]
    print(f"this is the shape after initializing {current_shape}")
    clock = pygame.time.Clock()
    running = True
    shape_rect = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
    #Will store a list of all the shapes after the 
    old_shapes_list = []
    last_spawn_time = time.time()
    #a while loop that updates each frame of the game
    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the close button is clicked, close the game
                running = False
                break
        #Will make this in a separate function for modularity
        shape_rect = key_moves(shape_rect)
        if current_time - last_spawn_time > SPAWN_DELAY:
            old_shapes_list.append((current_shape,shape_rect, ROTATION_ANGLE))
            shape_rect = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
            ROTATION_ANGLE = 0
            last_spawn_time = current_time
            shape_idx+=1
            current_shape = shapes_list[shape_idx]
            print(f"this is the shape after spawning {current_shape}")
        draw(current_shape,shape_rect, old_shapes_list,shapes)
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":

    main()