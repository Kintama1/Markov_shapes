import pygame
import time
from Markov_shapes import MarkovShape

#Width and height of the screen
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Markov shapes")
#Width, Height, movement speed and angle of ratation of the shapes
SHAPE_WIDTH = 40
SHAPE_HEIGHT = 60
SHAPE_VELOCITY = 5
ROTATION_ANGLE = 0
#Number of Frames per second
FPS = 60
#The timer before each new shape
SPAWN_DELAY= 5

def draw(current_shape, shape_rect, old_shapes_list, shapes,running):
    """
    Function that draws all the shapes on the current frame
    Args:
        Current_shape(string): name of the current shape that is being manipulated by the user
        shape_rect(pygame.rect): rect that holds the position of the current shape
        old_shapes_list(list): list of old shapes containing a tuple of shape name, position and argument to be drawn
        shapes(MarkovShapes):the passed object of Markov shape
    """
    WIN.fill((255,255,255))
    
    # Drawing all the old shapes for the current frame
    for shape, position, angle in old_shapes_list:
        # Create a temporary surface for rotation
        temp_surface = pygame.Surface((SHAPE_WIDTH, SHAPE_HEIGHT), pygame.SRCALPHA)
        #This is what Claude added to debug, building a new temporary rect for drawing
        temp_rect = pygame.Rect(0, 0, SHAPE_WIDTH, SHAPE_HEIGHT)
        shapes.shape_switchboard(shape, temp_surface, temp_rect)
        rotated_surface = pygame.transform.rotate(temp_surface, angle)
        #this is where the position gets updated to the old position
        rotated_rect = rotated_surface.get_rect(center=position.center)
        #the shape gets drawn with the rotated angle and position
        WIN.blit(rotated_surface, rotated_rect.topleft)
    if running:
        # Drawing the current shape for the current frame
        temp_surface = pygame.Surface((SHAPE_WIDTH, SHAPE_HEIGHT), pygame.SRCALPHA)
        temp_rect = pygame.Rect(0, 0, SHAPE_WIDTH, SHAPE_HEIGHT)
        shapes.shape_switchboard(current_shape, temp_surface, temp_rect)
        rotated_surface = pygame.transform.rotate(temp_surface, ROTATION_ANGLE)
        rotated_rect = rotated_surface.get_rect(center=shape_rect.center)
        WIN.blit(rotated_surface, rotated_rect.topleft)
    
    

def draw_texts(time,shapes_left,running):
    """
    Function that draws the text of time left for each shape and number of shapes left on the screen
    Args:
        time (int): time left for current shape
        shapes_left (int): number of shapes left

    """
    pygame.font.init()
    my_font = pygame.font.SysFont('Times New Roman', 20)   
    if running:
        
        timer_surface = my_font.render(f"Time left for this shape {time}",True,(0,0,0))
        shapes_left_surface = my_font.render(f"Shapes left {shapes_left}", True, (0,0,0))
        WIN.blit(timer_surface, (10,20))
        WIN.blit(shapes_left_surface,(10,45))
    else:
        finish_surface = my_font.render("This is your masterpiece!",True, (0,0,0))
        WIN.blit(finish_surface,((WIDTH//2)-100,20))

def key_moves(shape_rect):
    """
    Function that controls the movement of the shape via binding of keys
    args:
        shape_rect(pygame.rect): position of the shape to be moved
    """
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
def skip_shape(skip_current, space_pressed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not space_pressed:  # Set skip_current to True only once per space bar press
            skip_current = True
            space_pressed = True
    else:
        space_pressed = False
    return skip_current, space_pressed
def main():
    global ROTATION_ANGLE

    #The shape matrix
    shapes_matrix = {
        "rect" :{"rect": 0.25,"circle":0.25, "triangle": 0.25, "arc": 0.25},
        "circle" :{"rect":0.25, "triangle": 0.25, "arc": 0.25,"circle":0.25,},
        "triangle" :{"rect":0.25, "circle": 0.25, "arc": 0.25,"triangle": 0.25},
        "arc" :{"rect":0.25, "circle": 0.25, "triangle": 0.25,"arc": 0.25}
    }
    #object of markov shapes class
    shapes = MarkovShape(shapes_matrix)
    number_of_shapes = 20
    #created shapes list to be used in the game
    shapes_list = shapes.shape_sequence(length= number_of_shapes)
    shape_idx = 0
    current_shape = shapes_list[shape_idx]
    clock = pygame.time.Clock()
    running = True
    paused = False
    shape_rect = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
    #Will store a list of all the shapes after the 
    old_shapes_list = []
    last_spawn_time = time.time()

    #for skipping current shapes
    skip_current = False
    space_pressed = False

    #a while loop that updates each frame of the game
    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if the close button is clicked, close the game
                running = False
                break
        #boolean to end the timer for current shape 
        skip_current,space_pressed = skip_shape(skip_current,space_pressed)
        shape_rect = key_moves(shape_rect)
        time_left = int(SPAWN_DELAY - (current_time-last_spawn_time) + 1)
        if current_time - last_spawn_time > SPAWN_DELAY or skip_current:
            old_shapes_list.append((current_shape,shape_rect, ROTATION_ANGLE))
            shape_rect = pygame.Rect(500, HEIGHT-SHAPE_HEIGHT, SHAPE_WIDTH, SHAPE_HEIGHT)
            ROTATION_ANGLE = 0
            skip_current = False
            if shape_idx < number_of_shapes-1:
                last_spawn_time = current_time
                shape_idx+=1
                current_shape = shapes_list[shape_idx]
            else: 
                running = False
                paused = True
        
        shapes_left = number_of_shapes - shape_idx
        draw(current_shape,shape_rect, old_shapes_list,shapes,running)
        draw_texts(time_left,shapes_left,running)
        pygame.display.update()
        clock.tick(FPS)

    while paused:
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN and event.key == pygame.K_q or event.type == pygame.QUIT:
                paused = False
    pygame.quit()

if __name__ == "__main__":

    main()