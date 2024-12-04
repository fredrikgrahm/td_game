import pygame
import math

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shoot_timer = 0
        self.shoot_interval = 30
        self.range = 100
        self.level = 1
        self.upgrade_cost = 50
        self.laser_tower_asset = pygame.image.load('assets/images/laser_tower_128x128.png')
        self.laser_tower_asset = pygame.transform.scale(self.laser_tower_asset, (40, 40))  
        self.laser_tower_asset.set_colorkey((255, 255, 255))
        self.freeze_tower_asset = pygame.image.load('assets/images/freeze_tower_128x128.png')
        self.freeze_tower_asset = pygame.transform.scale(self.freeze_tower_asset, (40, 40)) 
        self.freeze_tower_asset.set_colorkey((255, 255, 255))
        self.fire_tower_asset = pygame.image.load('assets/images/fire_tower_128x128.png')
        self.fire_tower_asset = pygame.transform.scale(self.fire_tower_asset, (40, 40)) 
        self.fire_tower_asset.set_colorkey((255, 255, 255))  


    def draw(self, screen):
        screen.blit(self.laser_tower_asset, (self.x - 20, self.y - 20))
        # pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 20)  # Blue for LaserTower



    def draw_highlight(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 25, 2)
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.range, 1)  # Draw range indicator
        font = pygame.font.SysFont('Arial', 16)
        level_text = font.render(f'Lvl {self.level}', True, (0, 0, 0))
        screen.blit(level_text, (self.x - 15, self.y - 20))

    def draw_transparent(self, screen, color):
        # Create a transparent surface for the tower
        temp_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        temp_surface.blit(self.laser_tower_asset, (0, 0))
        temp_surface.fill((*color, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_surface, (self.x - 20, self.y - 20))
        # Draw the range circle
        pygame.draw.circle(screen, color, (self.x, self.y), self.range, 1)

    def shoot(self, enemies, screen):
        for enemy in enemies:
            if self.in_range(enemy):
                pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (enemy.x, enemy.y), 2)  # Red laser line
                enemy.take_damage(10)  # Example damage value
                # Enemy was hit
                if enemy.health <= 0:
                    return True, enemy  # Enemy was hit and killed
                else:
                    return True, None   # Enemy was hit but not killed
        return False, None  # No enemy was hit

    def in_range(self, enemy):
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range

    def is_clicked(self, mouse_x, mouse_y):
        distance = ((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2) ** 0.5
        return distance <= 20  # Assuming the tower's radius is 20

    def upgrade(self):
        self.level += 1
        self.range += 20  # Increase range
        self.shoot_interval = max(10, self.shoot_interval - 5)  # Decrease shoot interval
        self.upgrade_cost += 50  # Increase upgrade cost

    def get_upgrade_cost(self):
        return self.upgrade_cost

class FreezingTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shoot_interval = 50
        self.hit_enemies = set()  # Set to track enemies already hit


    def shoot(self, enemies, screen):
        for enemy in enemies:
            if self.in_range(enemy) and enemy.id not in self.hit_enemies:
                pygame.draw.line(screen, (0, 255, 255), (self.x, self.y), (enemy.x, enemy.y), 2)  # Cyan laser line
                enemy.freeze(100)  # Apply freeze effect
                enemy.take_damage(0)  # No initial damage
                self.hit_enemies.add(enemy.id)  # Mark enemy as hit
                print('Hit by freezing tower!')
                # Enemy was hit
                if enemy.health <= 0:
                    return True, enemy
                else:
                    return True, None
        return False, None

    def draw(self, screen):
        screen.blit(self.freeze_tower_asset, (self.x - 20, self.y - 20))


    def draw_transparent(self, screen, color):

        temp_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        temp_surface.blit(self.freeze_tower_asset, (0, 0))
        temp_surface.fill((*color, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_surface, (self.x - 20, self.y - 20))

        pygame.draw.circle(screen, color, (self.x, self.y), self.range, 1)

    def upgrade(self):
        super().upgrade()
        # Additional upgrade effects if any

class FireTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shoot_interval = 30  # FireTower shoots every 40 frames
        self.burn_duration = 50  # Burn effect lasts for 100 frames
        self.burn_damage = 1  # Burn effect deals 1 damage per frame
        self.burn_dies = set()  # Set to track if enemy is hit by burn effect

    def shoot(self, enemies, screen):
        for enemy in enemies:
            if self.in_range(enemy):
                pygame.draw.line(screen, (255, 69, 0), (self.x, self.y), (enemy.x, enemy.y), 2)  # Orange laser line
                enemy.take_damage(1)
                enemy.apply_burn(self.burn_duration, self.burn_damage)
                if enemy.health <= 0:
                    return True, enemy  # Enemy was killed
                else:
                    return True, None   # Enemy was hit but not killed
        return False, None

    def draw(self, screen):
        screen.blit(self.fire_tower_asset, (self.x - 20, self.y - 20))


    def draw_highlight(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 25, 2)
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.range, 1)
        font = pygame.font.SysFont('Arial', 16)
        level_text = font.render(f'Lvl {self.level}', True, (0, 0, 0))
        screen.blit(level_text, (self.x - 15, self.y - 20))

    def draw_transparent(self, screen, color):
        # Create a transparent surface for the tower
        temp_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        temp_surface.blit(self.fire_tower_asset, (0, 0))
        temp_surface.fill((*color, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_surface, (self.x - 20, self.y - 20))
        # Draw the range circle
        pygame.draw.circle(screen, color, (self.x, self.y), self.range, 1)    

    def upgrade(self):
        super().upgrade()
        # Additional upgrade effects if any

class Shop:
    def __init__(self, width, height, path_rects):
        self.shop_open = False  
        self.button_rect = pygame.Rect(10, height - 60, 100, 50) 
        self.tower_prices = {
            'LaserTower': 30,
            'FreezingTower': 50,
            'FireTower': 50 
        }
        self.selected_tower = None
        self.placing_tower = False
        self.width = width
        self.height = height
        self.path_rects = path_rects  

    def toggle_shop(self):
        self.shop_open = not self.shop_open

    def handle_shop_interaction(self, mouse_pos, player_coins):
        if self.shop_open:
            if pygame.Rect(10, self.height - 200 + 10, 200, 30).collidepoint(mouse_pos):
                if player_coins >= self.tower_prices['LaserTower']:
                    self.select_tower('LaserTower', player_coins)
            elif pygame.Rect(10, self.height - 200 + 40, 200, 30).collidepoint(mouse_pos):
                if player_coins >= self.tower_prices['FreezingTower']:
                    self.select_tower('FreezingTower', player_coins)
            elif pygame.Rect(10, self.height - 200 + 70, 200, 30).collidepoint(mouse_pos):
                if player_coins >= self.tower_prices['FireTower']:
                    self.select_tower('FireTower', player_coins)

    def select_tower(self, tower_name, player_coins):
        self.selected_tower = tower_name
        self.placing_tower = True

    def finalize_placement(self, player_coins, x, y, existing_towers):
        if self.selected_tower and player_coins >= self.tower_prices[self.selected_tower]:
            # Create a temporary tower for collision checking
            if self.selected_tower == 'LaserTower':
                new_tower = Tower(x, y)
            elif self.selected_tower == 'FreezingTower':
                new_tower = FreezingTower(x, y)
            elif self.selected_tower == 'FireTower':
                new_tower = FireTower(x, y)
            else:
                return player_coins, None, False  # Placement unsuccessful

            # Collision detection with existing towers
            for tower in existing_towers:
                distance = math.hypot(new_tower.x - tower.x, new_tower.y - tower.y)
                if distance < 40:  
                    return player_coins, None, False  

            # Collision detection with path
            tower_rect = pygame.Rect(new_tower.x - 20, new_tower.y - 20, 40, 40)
            for path_rect in self.path_rects:
                if tower_rect.colliderect(path_rect):
                    return player_coins, None, False  # Cannot place tower on path

            # Proceed to place the tower
            player_coins -= self.tower_prices[self.selected_tower]
            self.placing_tower = False  # Exit placement mode
            self.selected_tower = None  # Clear selected tower
            return player_coins, new_tower, True  # Placement successful
        return player_coins, None, False  # Placement unsuccessful

    def cancel_placement(self):
        self.placing_tower = False
        self.selected_tower = None

    def draw_shop(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        pygame.draw.rect(screen, (200, 200, 200), self.button_rect)
        button_text = font.render('Shop', True, (0, 0, 0))
        screen.blit(button_text, (self.button_rect.x + 10, self.button_rect.y + 5))

        if self.shop_open:
            # Adjust the coordinates for the expanded shop panel
            panel_x = 10
            panel_y = self.height - 200  # Adjusted to be above the button
            
            pygame.draw.rect(screen, (200, 200, 200), (panel_x, panel_y, 200, 130))
            laser_text = font.render(f'Laser Tower: {self.tower_prices["LaserTower"]} coins', True, (0, 0, 0))
            freezing_text = font.render(f'Freezing Tower: {self.tower_prices["FreezingTower"]} coins', True, (0, 0, 0))
            fire_text = font.render(f'Fire Tower: {self.tower_prices["FireTower"]} coins', True, (0, 0, 0))
            screen.blit(laser_text, (panel_x + 10, panel_y + 10))
            screen.blit(freezing_text, (panel_x + 10, panel_y + 40))
            screen.blit(fire_text, (panel_x + 10, panel_y + 70))
