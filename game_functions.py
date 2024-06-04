import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, game_settings, game_screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, game_screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(game_settings, game_screen, game_stats, score_display, start_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, game_screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                game_settings,
                game_screen,
                game_stats,
                score_display,
                start_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    game_settings, game_screen, game_stats, score_display, start_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Start a new game when the player clicks Play."""
    button_clicked = start_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game_stats.game_active:
        # Reset the game settings.
        game_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        game_stats.reset_stats()
        game_stats.game_active = True

        # Reset the scoreboard images.
        score_display.prep_score()
        score_display.prep_high_score()
        score_display.prep_level()
        score_display.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(game_settings, game_screen, ship, aliens)
        ship.center_ship()


def fire_bullet(game_settings, game_screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, game_screen, ship)
        bullets.add(new_bullet)


def update_screen(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets, start_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    game_screen.fill(game_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(game_screen)

    # Draw the score information.
    score_display.show_score()

    # Draw the play button if the game is inactive.
    if not game_stats.game_active:
        start_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets)


def check_high_score(game_stats, score_display):
    """Check to see if there's a new high score."""
    if game_stats.score > game_stats.high_score:
        game_stats.high_score = game_stats.score
        score_display.prep_high_score()


def check_bullet_alien_collisions(
    game_settings, game_screen, game_stats, score_display, ship, aliens, bullets
):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            game_stats.score += game_settings.alien_points * len(aliens)
            score_display.prep_score()
        check_high_score(game_stats, score_display)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        game_settings.increase_speed()

        # Increase level.
        game_stats.level += 1
        score_display.prep_level()

        create_fleet(game_settings, game_screen, ship, aliens)


def check_fleet_edges(game_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def ship_hit(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if game_stats.ships_left > 0:
        # Decrement ships_left.
        game_stats.ships_left -= 1

        # Update scoreboard.
        score_display.prep_ships()

    else:
        game_stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet, and center the ship.
    create_fleet(game_settings, game_screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = game_screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets)
            break


def update_aliens(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(game_settings, game_screen, game_stats, score_display, ship, aliens, bullets)


def get_number_aliens_x(game_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = game_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, game_screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(game_settings, game_screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, game_screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(game_settings, game_screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, game_screen, aliens, alien_number, row_number)
