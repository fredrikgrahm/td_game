import pygame
import sys
import math
import json
from game.enemies import Enemy
from game.towers import Tower, FreezingTower, FireTower, Shop
from game.wave_manager import WaveManager
from game.scoreboard import Scoreboard
from game.game_state import GameState
from game.event_handler import handle_events
from game.path_rect import generate_path_polygons  # Use polygons instead of rects

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tower Defense")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (169, 169, 169)
        
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Instantiate game elements
        # Do not instantiate WaveManager here
        # self.wave_manager = WaveManager()
        self.scoreboard = Scoreboard()
        self.game_state = GameState()
        
        
        self.selected_tower = [None]  # Use a list for mutability
        self.enemies = []
        self.towers = []
        self.coins_spent = 0
        self.add_enemy_destroyed = self.scoreboard.add_enemy_destroyed

        self.player_coins = 100
        self.player_health = 3
        self.message = ''  # Current message to display
        self.message_timer = 0  # Timer for message duration

        # Define path rectangles for collision detection
        # self.path_rects = [
        #     pygame.Rect(0, self.HEIGHT // 2 - 20, 150, 40),        # Horizontal path from left to (150, HEIGHT // 2)
        #     pygame.Rect(150 - 20, 100, 40, self.HEIGHT // 2 - 100), # Vertical path up to (150, 100)
        #     pygame.Rect(150, 100 - 20, 300, 40),                   # Horizontal path to the right to (450, 100)
        #     pygame.Rect(450 - 20, 100, 40, 300),                   # Vertical path down to (450, 400)
        #     pygame.Rect(250, 400 - 20, 200, 40),                   # Horizontal path to the left to (250, 400)
        #     pygame.Rect(250 - 20, 400, 40, self.HEIGHT - 500),     # Vertical path down to (250, HEIGHT - 100)
        #     pygame.Rect(250, self.HEIGHT - 100 - 20, self.WIDTH - 300, 40),  # Final horizontal path to the right
        # ]


        # # Define waypoints
        # self.waypoints = [
        #     (0, self.HEIGHT // 2),
        #     (150, self.HEIGHT // 2),
        #     (150, 100),
        #     (450, 100),
        #     (450, 400),
        #     (250, 400),
        #     (250, self.HEIGHT - 100),
        #     (self.WIDTH - 50, self.HEIGHT - 100),
        # ]
        
        # New waypoints loaded from file
        with open('waypoints.json', 'r') as f:
            self.waypoints = json.load(f)

        self.path_polygons = generate_path_polygons(self.waypoints, 40)
        self.shop = Shop(self.WIDTH, self.HEIGHT, self.path_polygons)
        self.wave_manager = WaveManager(self.waypoints)
        
        self.clock = pygame.time.Clock()
        
    def start_game(self):
        self.game_state.set_running()
        self.enemies.clear()
        self.towers.clear()
        self.wave_manager.reset()
        self.player_coins = 100
        self.selected_tower[0] = None  
        self.player_health = 1
        self.shop.shop_open = False

    def draw_map(self):
        # Draw path using polygons
        for polygon in self.path_polygons:
            pygame.draw.polygon(self.screen, self.GREY, polygon)

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.move(self.waypoints)
            if enemy.health <= 0:
                enemy_type_name = enemy.__class__.__name__  # Get enemy type as string
                self.scoreboard.add_enemy_destroyed(enemy_type_name)  # Update enemy_counts
                self.player_coins += enemy.coin_reward
                self.enemies.remove(enemy)
            elif enemy.waypoint_index >= len(self.waypoints):
                self.player_health -= 1
                self.enemies.remove(enemy)
                if self.player_health <= 0:
                    self.game_state.set_game_over()

            
    def draw_hud(self):
        coins_text = self.font.render(f'Coins: {self.player_coins}', True, self.BLACK)
        self.screen.blit(coins_text, (10, 10))
        wave_text = self.font.render(f'Wave: {self.wave_manager.current_wave}/{self.wave_manager.total_waves}', True, self.BLACK)
        self.screen.blit(wave_text, (self.WIDTH // 2 - wave_text.get_width() // 2, 10))
        health_text = self.font.render(f'Health: {self.player_health}', True, self.BLACK)
        self.screen.blit(health_text, (self.WIDTH - health_text.get_width() - 10, 10))
        if not self.wave_manager.wave_in_progress:
            countdown = self.wave_manager.get_time_until_next_wave()
            if countdown > 0:
                countdown_text = self.font.render(f'Next wave in: {countdown}s', True, self.BLACK)
                self.screen.blit(countdown_text, (self.WIDTH // 2 - countdown_text.get_width() // 2, 200))

    def update_towers(self):
        for tower in self.towers:
            if hasattr(tower, 'shoot_timer'):
                tower.shoot_timer += 1
            if tower.shoot_timer >= tower.shoot_interval:
                hit, killed_enemy = tower.shoot(self.enemies, self.screen)
                if killed_enemy:
                    self.player_coins += killed_enemy.coin_reward
                    enemy_type_name = killed_enemy.__class__.__name__
                    self.scoreboard.add_enemy_destroyed(enemy_type_name)
                    self.enemies.remove(killed_enemy)
                tower.shoot_timer = 0

    def draw_game_elements(self):
      
        self.draw_map()
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for tower in self.towers:
            tower.draw(self.screen)
        
        if self.selected_tower[0]:
            self.selected_tower[0].draw_highlight(self.screen)
        
        self.shop.draw_shop(self.screen)
        
        self.wave_manager.draw_wave_message(self.screen, self.font)
        
        self.draw_hud()
        # Draw placement mode message
        if self.shop.placing_tower:
            # placing_text = self.font.render(
            #     'Placing Tower... Left click to Confirm, press ESC to cancel',
            #     True, (255, 0, 0)
            # )
            # self.screen.blit(
            #     placing_text, 
            #     (self.WIDTH // 2 - placing_text.get_width() // 2, 10)
            # )
            
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            

            tower_class = None
            if self.shop.selected_tower == 'LaserTower':
                tower_class = Tower
            elif self.shop.selected_tower == 'FreezingTower':
                tower_class = FreezingTower
            elif self.shop.selected_tower == 'FireTower':
                tower_class = FireTower
            
            if tower_class:
                # Create a temporary tower at mouse position
                temp_tower = tower_class(mouse_x, mouse_y)
                
                # Check for collisions
                invalid_position = False

                # Collision with existing towers
                for tower in self.towers:
                    distance = math.hypot(temp_tower.x - tower.x, temp_tower.y - tower.y)
                    if distance < 40:  # Towers have a radius of 20
                        invalid_position = True
                        break

                # Collision with paths
                tower_point = (temp_tower.x, temp_tower.y)
                for polygon in self.path_polygons:
                    if point_in_polygon(tower_point, polygon):
                        invalid_position = True
                        break

                # Set color based on validity
                if invalid_position:
                    color = (255, 0, 0)  
                else:
                    color = (0, 255, 0)  

                
                temp_tower.draw_transparent(self.screen, color)

    def show_message(self, text, duration=500):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration  

    def draw_message(self):
        if self.message and pygame.time.get_ticks() < self.message_timer:
            message_text = self.font.render(self.message, True, (255, 0, 0))  # Red text
            self.screen.blit(
                message_text,
                (
                    self.WIDTH // 2 - message_text.get_width() // 2,
                    self.HEIGHT // 2 - message_text.get_height() // 2
                )
            )
        else:
            self.message = ''  # Clear the message after the duration

    def game_loop(self):
        self.running = True
        while self.running:
            self.player_coins, message = handle_events(
                self.game_state, self.shop, self.towers, self.wave_manager,
                self.enemies, self.player_coins, self.selected_tower, self.start_game,
                self.towers, self.scoreboard  
            )
            if message:
                self.show_message(message)
            
            # Clear Screen
            self.screen.fill(self.WHITE)

            if self.game_state.is_start_screen():
                title_text = self.font.render('Tower Defense Game', True, self.BLACK)
                start_text = self.font.render('Click to Start', True, self.BLACK)
                self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, self.HEIGHT // 2 - 50))
                self.screen.blit(start_text, (self.WIDTH // 2 - start_text.get_width() // 2, self.HEIGHT // 2 + 10))
            elif self.game_state.is_running():
                # Update game elements
                self.wave_manager.update(self.enemies)
                self.update_enemies()
                self.update_towers()
               
                
                self.draw_game_elements()
                
                self.draw_message()
                # Check for game over
                if self.player_health <= 0:
                    self.scoreboard.set_wave_reached(self.wave_manager.current_wave)
                    self.scoreboard.add_coins_spent(self.coins_spent)
                    self.scoreboard.save_Score()
                    self.game_state.set_game_over()
                    
            elif self.game_state.is_game_over():
                game_over_text = self.font.render('Game Over', True, self.BLACK)
                restart_text = self.font.render('Press ESC to return to the start screen', True, self.BLACK)
                self.scoreboard_text = self.font.render('Press S to view the scoreboard', True, self.BLACK)
                self.screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, self.HEIGHT // 2 - 50))
                self.screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, self.HEIGHT // 2 + 10))
                self.screen.blit(self.scoreboard_text, (self.WIDTH // 2 - self.scoreboard_text.get_width() // 2, self.HEIGHT // 2 + 50))

            elif self.game_state.is_scoreboard_screen():
                self.screen.fill(self.WHITE)
                self.scoreboard.draw(self.screen, self.font)

            pygame.display.flip()
            self.clock.tick(60)

        # Clean up
        pygame.quit()
        sys.exit()

def point_in_polygon(point, polygon):
    x, y = point
    num = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(num + 1):
        p2x, p2y = polygon[i % num]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y + 1e-10) + p1x
                        if x <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y
    return inside

if __name__ == "__main__":
    game = Game()
    game.game_loop()

