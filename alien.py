import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, game_settings, game_screen):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.game_screen = game_screen
        self.game_settings = game_settings

        # Load the alien image, and set its rect attribute.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.game_screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.game_settings.alien_speed_factor * self.game_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location."""
        self.game_screen.blit(self.image, self.rect)
