import pygame
import sys

def handle_events(game_state, shop, towers, wave_manager, enemies, player_coins, selected_tower, start_game, existing_towers, scoreboard):
    current_coins = player_coins
    
    message = ''  # Initialize the message variable
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if game_state.is_start_screen():
                    start_game()
                    current_coins = 100  # Reset coins when starting a new game
                    
                elif game_state.is_running():
                    if shop.button_rect.collidepoint(mouse_x, mouse_y):
                        shop.toggle_shop()
                    elif shop.placing_tower:
                        new_coins, new_tower, placement_success = shop.finalize_placement(current_coins, mouse_x, mouse_y, existing_towers)
                        if placement_success:
                            towers.append(new_tower)
                            selected_tower[0] = None
                            amount_spent = current_coins - new_coins  # Calculate the amount spent
                            scoreboard.add_coins_spent(amount_spent)   # Update coins_spent
                            current_coins = new_coins  # Update current coins
                        else:
                            message = "You can't build here"
                    else:
                        shop.handle_shop_interaction((mouse_x, mouse_y), current_coins)
                        for tower in towers:
                            if tower.is_clicked(mouse_x, mouse_y):
                                selected_tower[0] = tower
                                break
                elif game_state.is_game_over():
                    game_state.set_start_screen()
            elif event.button == 3:  # Right click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_state.is_running():
                    for tower in towers:
                        if tower.is_clicked(mouse_x, mouse_y):
                            upgrade_cost = tower.get_upgrade_cost()
                            if current_coins >= upgrade_cost:
                                tower.upgrade()
                                current_coins -= upgrade_cost
                                scoreboard.add_coins_spent(upgrade_cost)  # Update coins_spent
                                message = 'Tower Upgraded!'
                            else:
                                message = 'Not enough coins to upgrade. It costs ' + str(upgrade_cost) + ' coins.'
                            break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if shop.placing_tower:
                    shop.cancel_placement()
                elif game_state.is_game_over():
                    game_state.set_start_screen()
                elif game_state.is_scoreboard_screen():
                    game_state.set_start_screen()    
            if event.key == pygame.K_s:
                if game_state.is_game_over():
                    game_state.set_scoreboard_screen()    
    
    return current_coins, message