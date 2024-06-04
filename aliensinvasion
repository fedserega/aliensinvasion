import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    game_settings = Settings()
    game_screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    start_button = Button(game_settings, game_screen, "Play")

    # Create an instance to store game statistics, and a scoreboard.
    game_stats = GameStats(game_settings)
    score_display = Scoreboard(game_settings, game_screen, game_stats)

    # Set the background color.
    background_color = (230, 230, 230)

    # Make a ship, a group of bullets, and a group of aliens.
    player_ship = Ship(game_settings, game_screen)
    bullet_group = Group()
    alien_group = Group()

    # Create the fleet of aliens.
    gf.create_fleet(game_settings, game_screen, player_ship, alien_group)

    # Start the main loop for the game.
    while True:
        gf.check_events(
            game_settings, game_screen, game_stats, score_display, start_button, player_ship, alien_group, bullet_group
        )

        if game_stats.game_active:
            player_ship.update()
            gf.update_bullets(game_settings, game_screen, game_stats, score_display, player_ship, alien_group, bullet_group)
            gf.update_aliens(game_settings, game_screen, game_stats, score_display, player_ship, alien_group, bullet_group)

        gf.update_screen(
            game_settings, game_screen, game_stats, score_display, player_ship, alien_group, bullet_group, start_button
        )


run_game()
