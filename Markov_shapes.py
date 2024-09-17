import pygame
import time 
import math
import numpy as np

class MarkovShape:
    def __init__(self, transition_matrix):
        """
        Will hold on and draw all the shapes of the markov shapes based on the transition matrix
        Args:
            Transition matrix (dict): Holds the probabily of transitioning from one shape to the other
        potential adding: color matrix so it can be updated for different colors
        """
        self.transition_matrix = transition_matrix
        self.shapes = list(transition_matrix.keys())
    
    def get_next_shape(self,current_shape):
        """
        Decides which shape to give based on the current shape
        Args:
            current_shape (string) : The current shape in the sequence
        """
        return np.random.choice(
            self.shapes,
            p=[self.transition_matrix[current_shape][next_shape] \
            for next_shape in self.shapes])
    
    def shape_sequence(self, current_shape = "rect", length = 15):
        """
        Generates a sequnce of shapes
        Args:
            current_shape(String): the current shape that is being displayed
            length(int): The length or number of shapes to be displayed
        """
        shapes = []
        while len(shapes) < length:
            next_shape = self.get_next_shape(current_shape)
            shapes.append(next_shape)
            current_shape = next_shape
        return shapes
    
    def draw_rectangle(self, surface,rect):
        """
        Function that when called on will draw a pygame rectangle
        Args:
            surface (pygame.surface): the surface that the rectangle will be drawn upon
            width (int): width of the surface
            height (int): height of the surface
        """
        pygame.draw.rect(surface,(141,171,206), rect)
    
    def draw_circle(self,surface, rect):
        """
        Function that when called will draw a pygame circle
        Args:
            surface (pygame.surface): the surface that the rectangle will be drawn upon
            width (int): width of the surface
            height (int): height of the surface
        """
        #Will draw a circle split in two colors so rotation can have a meaning for a circle
        #works but will have to modify this so it fits within the screen.
        radius = (rect.width//2)- 2
        pygame.draw.circle(surface, (49, 233, 129),rect.center,radius)
        pygame.draw.circle(surface, (53,96,90) ,rect.center,radius, draw_top_right=True, draw_bottom_left= True)
    
    def draw_triangle(self,surface,rect):
        """
        Function that when called will draw a pygame triangle
        Args:
            surface (pygame.surface): the surface that the rectangle will be drawn upon
            width (int): width of the surface
            height (int): height of the surface
        """
        point1 = (rect.centerx, rect.top+15)
        point2 = (rect.left, rect.bottom)
        point3 = (rect.right, rect.bottom)
        pygame.draw.polygon(surface, (245, 221,144), [point1,point2,point3])
    
    def draw_arc(self, surface, rect):       
        """ Function that when called will draw a pygame arc         
                Args:             
                surface (pygame.surface): the surface that the rectangle will be drawn upon             
                width (int): width of the surface             
                height (int): height of the surface        
                  
        """         
        pygame.draw.arc(surface, (246,142,0),rect, 0, 3.14, width = 4)

# In your main loop:
    

    def shape_switchboard(self,shape,surface,rect):
        """
        Function that will take the shape name and will draw the corresponding shape
        Args:
            shape (str): name of the shape
            surface (pygame.surface): surface that the shape will be drawn upon
            rect (pygame.rect): the coordinates of the rectangle of the shape
        """
        switch_dict = {
            "rect": self.draw_rectangle,
            "circle":self.draw_circle,
            "triangle": self.draw_triangle,
            "arc": self.draw_arc
        }
        print(switch_dict[shape])
        switch_dict[shape](surface,rect)




if __name__ == "__main__":
    pygame.init()
# Set up the screen (width, height)
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    shapes_matrix = {
        "rect" :{"rect": 0.25,"circle":0.25, "triangle": 0.25, "arc": 0.25},
        "circle" :{"rect":0.25, "triangle": 0.25, "arc": 0.25,"circle":0.25,},
        "triangle" :{"rect":0.25, "circle": 0.25, "arc": 0.25,"triangle": 0.25},
        "arc" :{"rect":0.25, "circle": 0.25, "triangle": 0.25,"arc": 0.25}
    }
    shapes = MarkovShape(shapes_matrix)
    list_sha = shapes.shape_sequence()
    print(list_sha)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255,255,255)) 
        rect = pygame.Rect(300, 200, 40, 60)
        # Fill the screen with white
       
        for shape in list_sha:
            shapes.shape_switchboard(shape,screen,rect)  
            rect.center = (rect.center[0] - 10, rect.center[1] - 10) 
                        

          

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()