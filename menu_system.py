import pygame
import asyncio
from utils.settings import GameSettings, WIDTH, HEIGHT
from utils.button import Button

class WebMenuManager:
    """Handles web-specific display and menu management"""
    def __init__(self, screen=None):
        # Use provided screen or create one if not provided
        if screen is None:
            self.screen = pygame.display.set_mode(
                (WIDTH, HEIGHT),
                pygame.SCALED | pygame.RESIZABLE,
                vsync=1
            )
            pygame.display.set_caption("Markov Shapes")
        else:
            self.screen = screen
        
        # Initialize fonts with fallbacks
        try:
            self.main_font = pygame.font.SysFont('Arial', 32)
            self.small_font = pygame.font.SysFont('Arial', 24)
        except:
            self.main_font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 24)
        
        # Initialize game components
        self.settings = GameSettings()
        self.state = "menu"
        self._create_menus()
        
    def _create_menus(self):
        """Create all menu buttons and layouts"""
        # Main menu buttons
        center_x = WIDTH // 2
        start_y = HEIGHT // 2 - 100
        button_spacing = 80
        button_width = 200
        button_height = 50
        
        self.main_buttons = [
            Button(center_x - button_width//2, start_y, 
                  button_width, button_height, "Start Game"),
            Button(center_x - button_width//2, start_y + button_spacing, 
                  button_width, button_height, "Settings"),
            Button(center_x - button_width//2, start_y + button_spacing * 2, 
                  button_width, button_height, "How to Play"),
            Button(center_x - button_width//2, start_y + button_spacing * 3, 
                  button_width, button_height, "Quit")
        ]
        
        # Settings menu buttons
        settings_y = 200
        settings_spacing = 70
        settings_width = 300
        arrow_width = 40
        
        self.settings_buttons = []
        # Add settings controls (spawn delay, shapes, velocity, rotation)
        for i, (label, value) in enumerate([
            ("Spawn Delay", self.settings.spawn_delay),
            ("Number of Shapes", self.settings.num_shapes),
            ("Movement Speed", self.settings.shape_velocity),
            ("Rotation Speed", self.settings.rotation_speed)
        ]):
            y_pos = settings_y + settings_spacing * i
            self.settings_buttons.extend([
                Button(center_x - settings_width//2 - 50, y_pos, 
                      arrow_width, button_height, "<"),
                Button(center_x - settings_width//2, y_pos,
                      settings_width, button_height, f"{label}: {value}"),
                Button(center_x + settings_width//2 + 10, y_pos,
                      arrow_width, button_height, ">")
            ])
        
        # Add back button for settings
        self.settings_buttons.append(
            Button(center_x - button_width//2, 
                  settings_y + settings_spacing * 4,
                  button_width, button_height, "Back to Menu")
        )
        
        # Help menu button (just back button)
        self.help_buttons = [
            Button(center_x - button_width//2, HEIGHT - 100,
                  button_width, button_height, "Back to Menu")
        ]

    def draw_main_menu(self):
        """Draw the main menu screen"""
        self.screen.fill((255, 255, 255))
        
        # Draw title
        title = self.main_font.render("Markov Shapes", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.small_font.render("Create Art with Shapes", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for button in self.main_buttons:
            button.draw(self.screen)

    def draw_settings_menu(self):
        """Draw the settings menu screen"""
        self.screen.fill((255, 255, 255))
        
        # Draw title
        title = self.main_font.render("Settings", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.small_font.render("Click arrows to adjust values", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        for button in self.settings_buttons:
            button.draw(self.screen)

    def draw_help_menu(self):
        """Draw the help menu screen"""
        self.screen.fill((255, 255, 255))
        
        # Draw title
        title = self.main_font.render("How to Play", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "• Arrow Keys - Move shape",
            "• A/D - Rotate shape left/right",
            "• Spacebar - Skip to next shape",
            "",
            "Gameplay:",
            "• Each shape appears for a limited time",
            "• Place shapes to create your artwork",
            "• Be creative with shape combinations",
            "• Try to use all shapes before time runs out"
        ]
        
        y_pos = 150
        for line in instructions:
            if line:
                text = self.small_font.render(line, True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH//2, y_pos))
                self.screen.blit(text, text_rect)
            y_pos += 30
        
        # Draw back button
        for button in self.help_buttons:
            button.draw(self.screen)

    async def handle_events(self):
        """Handle menu events and return state changes"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if self.state == "menu":
                for i, button in enumerate(self.main_buttons):
                    if button.handle_event(event):
                        if i == 0:
                            return "game"
                        elif i == 1:
                            self.state = "settings"
                        elif i == 2:
                            self.state = "help"
                        elif i == 3:
                            return "quit"
            
            elif self.state == "settings":
                for i, button in enumerate(self.settings_buttons):
                    if button.handle_event(event):
                        if i == len(self.settings_buttons) - 1:  # Back button
                            self.state = "menu"
                        else:
                            # Handle settings adjustments
                            setting_index = i // 3
                            is_decrease = (i % 3) == 0
                            self._update_setting(setting_index, -1 if is_decrease else 1)
            
            elif self.state == "help":
                for button in self.help_buttons:
                    if button.handle_event(event):
                        self.state = "menu"
        
        return None

    def _update_setting(self, index, direction):
        """Update a setting value based on index and direction"""
        settings_map = [
            ("spawn_delay", range(1, 11)),
            ("num_shapes", range(5, 31, 5)),
            ("shape_velocity", range(1, 11)),
            ("rotation_speed", range(1, 11))
        ]
        
        if index < len(settings_map):
            setting_name, value_range = settings_map[index]
            current_value = getattr(self.settings, setting_name)
            
            # Find current index and calculate new value
            try:
                current_index = list(value_range).index(current_value)
                new_index = (current_index + direction) % len(value_range)
                new_value = list(value_range)[new_index]
                setattr(self.settings, setting_name, new_value)
            except ValueError:
                print(f"Warning: Current value {current_value} not in range for {setting_name}")
            
            # Update button text
            button_index = index * 3 + 1
            if button_index < len(self.settings_buttons):
                self.settings_buttons[button_index].text = f"{settings_map[index][0]}: {new_value}"

    def draw(self):
        """Draw the current menu state"""
        if self.state == "menu":
            self.draw_main_menu()
        elif self.state == "settings":
            self.draw_settings_menu()
        elif self.state == "help":
            self.draw_help_menu()
        
        pygame.display.flip()

    def get_settings(self):
        """Return the current settings"""
        return self.settings