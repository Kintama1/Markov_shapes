import pygame
import random

class MarkovShape:
    def __init__(self, transition_matrix):
        """
        Creates a web-compatible version of MarkovShape that manages shape transitions
        and drawing.
        
        Args:
            transition_matrix (dict): Dictionary containing shape transition probabilities
        """
        self.transition_matrix = transition_matrix
        self.shapes = list(transition_matrix.keys())
    
    def get_next_shape(self, current_shape):
        """
        Selects the next shape using regular Python random instead of numpy.
        Uses cumulative probability for selection.
        
        Args:
            current_shape (str): The current shape name
        Returns:
            str: The next shape name
        """
        # Get probabilities for current shape
        probs = [self.transition_matrix[current_shape][shape] for shape in self.shapes]
        
        # Generate cumulative probabilities
        cumulative = []
        total = 0
        for p in probs:
            total += p
            cumulative.append(total)
        
        # Generate random number and find corresponding shape
        r = random.random()
        for i, cum_prob in enumerate(cumulative):
            if r <= cum_prob:
                return self.shapes[i]
        return self.shapes[-1]  # Fallback to last shape
    
    def shape_sequence(self, current_shape="rect", length=15):
        """
        Generates a sequence of shapes using the Markov chain.
        
        Args:
            current_shape (str): Starting shape
            length (int): Number of shapes to generate
        Returns:
            list: Sequence of shape names
        """
        shapes = []
        for _ in range(length):
            next_shape = self.get_next_shape(current_shape)
            shapes.append(next_shape)
            current_shape = next_shape
        return shapes
    
    def draw_rectangle(self, surface, rect):
        """
        Draws a rectangle with proper alpha handling.
        """
        # Create a temporary surface with alpha
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, (141, 171, 206, 255), 
                        (0, 0, rect.width, rect.height))
        surface.blit(temp_surface, rect)
    
    def draw_circle(self, surface, rect):
        """
        Draws a two-colored circle with proper alpha handling.
        """
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        radius = (rect.width // 2) - 2
        center = (rect.width // 2, rect.height // 2)
        
        # Draw base circle
        pygame.draw.circle(temp_surface, (49, 233, 129, 255), center, radius)
        
        # Draw half circle overlay
        pygame.draw.circle(temp_surface, (53, 96, 90, 255), center, radius,
                         draw_top_right=True, draw_bottom_left=True)
        
        surface.blit(temp_surface, rect)
    
    def draw_triangle(self, surface, rect):
        """
        Draws a triangle with proper alpha handling.
        """
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        points = [
            (rect.width // 2, 15),  # top
            (0, rect.height),       # bottom left
            (rect.width, rect.height)  # bottom right
        ]
        pygame.draw.polygon(temp_surface, (245, 221, 144, 255), points)
        surface.blit(temp_surface, rect)
    
    def draw_arc(self, surface, rect):
        """
        Draws an arc with proper alpha handling.
        """
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.arc(temp_surface, (246, 142, 0, 255), 
                       (0, 0, rect.width, rect.height),
                       0, 3.14, width=4)
        surface.blit(temp_surface, rect)
    
    def shape_switchboard(self, shape, surface, rect):
        """
        Routes shape drawing to appropriate method with error handling.
        """
        switch_dict = {
            "rect": self.draw_rectangle,
            "circle": self.draw_circle,
            "triangle": self.draw_triangle,
            "arc": self.draw_arc
        }
        
        if shape in switch_dict:
            try:
                switch_dict[shape](surface, rect)
            except Exception as e:
                print(f"Error drawing shape {shape}: {e}")
                # Fallback to rectangle on error
                self.draw_rectangle(surface, rect)