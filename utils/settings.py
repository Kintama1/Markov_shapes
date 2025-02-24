import pygame
from dataclasses import dataclass

# Game window settings
WIDTH = 1000
HEIGHT = 700
FPS = 60

@dataclass
class GameSettings:
    # Gameplay settings
    spawn_delay: int = 5
    num_shapes: int = 20
    shape_velocity: int = 5
    rotation_speed: int = 5
    
    # Shape dimensions
    shape_width: int = 40
    shape_height: int = 60
    
    # Shape probabilities (Markov chain)
    shapes_matrix = {
        "rect": {"rect": 0.25, "circle": 0.25, "triangle": 0.25, "arc": 0.25},
        "circle": {"rect": 0.25, "triangle": 0.25, "arc": 0.25, "circle": 0.25},
        "triangle": {"rect": 0.25, "circle": 0.25, "arc": 0.25, "triangle": 0.25},
        "arc": {"rect": 0.25, "circle": 0.25, "triangle": 0.25, "arc": 0.25}
    }

# Key bindings
CONTROLS = {
    "move_left": pygame.K_LEFT,
    "move_right": pygame.K_RIGHT,
    "move_up": pygame.K_UP,
    "move_down": pygame.K_DOWN,
    "rotate_left": pygame.K_a,
    "rotate_right": pygame.K_d,
    "skip_shape": pygame.K_SPACE,
    "quit": pygame.K_q
}