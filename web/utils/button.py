import pygame

class Button:
    """
    A simple button class for UI elements in Pygame.
    Handles rendering and mouse interaction.
    """
    def __init__(self, x, y, width, height, text, 
                 color=(200, 200, 200), 
                 hover_color=(160, 160, 160), 
                 text_color=(0, 0, 0)):
        """
        Initialize a button with position, size, text and colors.
        
        Args:
            x: X position of the button
            y: Y position of the button
            width: Width of the button
            height: Height of the button
            text: Text to display on the button
            color: Normal button color (RGB tuple)
            hover_color: Button color when hovered (RGB tuple)
            text_color: Text color (RGB tuple)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
        # Font initialization
        try:
            self.font = pygame.font.SysFont('Arial', 20)
        except:
            self.font = pygame.font.Font(None, 20)
        
    def draw(self, surface):
        """
        Draw the button on the provided surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Check for hover
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Draw the button with appropriate color
        pygame.draw.rect(surface, 
                      self.hover_color if self.is_hovered else self.color, 
                      self.rect, 
                      border_radius=5)
        
        # Draw the border
        pygame.draw.rect(surface, 
                      (100, 100, 100), 
                      self.rect, 
                      width=2, 
                      border_radius=5)
        
        # Render and draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """
        Process mouse events for the button.
        
        Args:
            event: Pygame event to process
            
        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return self.rect.collidepoint(event.pos)
        return False
