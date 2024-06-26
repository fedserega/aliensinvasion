import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game_settings, game_screen, player_ship):
        """Create a bullet object, at the ship's current position."""
        super(Bullet, self).__init__()
        self.game_screen = game_screen

        # Create bullet rect at (0, 0), then set correct position.
        self.rect = pygame.Rect(
            0, 0, game_settings.bullet_width, game_settings.bullet_height
        )
        self.rect.centerx = player_ship.rect.centerx
        self.rect.top = player_ship.rect.top

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.game_screen, self.color, self.rect)
