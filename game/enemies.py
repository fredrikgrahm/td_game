import pygame
import math

class Enemy:
    _id_counter = 0  # Class variable to generate unique IDs
    
    def __init__(self, x, y):
        self.id = Enemy._id_counter
        Enemy._id_counter += 1
        self.x = x
        self.y = y
        self.size = 20
        self.waypoint_index = 0
        self.frozen_timer = 0
        self.frozen = False
        self.burn_duration = 0
        self.burn_damage = 0
        self.burn_delay = False  # Initialize burn delay

    def move(self, waypoints):
        if self.frozen:
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.unfreeze()
            return

        if self.waypoint_index < len(waypoints):
            target_x, target_y = waypoints[self.waypoint_index]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            if distance <= self.speed:
                # Reached waypoint, move to next one
                self.x = target_x
                self.y = target_y
                self.waypoint_index += 1
            else:
                # Move towards waypoint
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                self.x += move_x
                self.y += move_y

        # Handle burn effect
        if self.burn_duration > 0:
            if not self.burn_delay:
                self.take_damage(self.burn_damage)
            else:
                self.burn_delay = False
            self.burn_duration -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw health bar
        health_bar_width = self.size
        current_health_width = (self.health / self.max_health) * health_bar_width

        # Background (max health)
        health_bar_background_rect = pygame.Rect(self.x, self.y - 10, health_bar_width, 5)
        pygame.draw.rect(screen, (255, 0, 0), health_bar_background_rect)  # Red background for missing health

        # Current health
        health_bar_rect = pygame.Rect(self.x, self.y - 10, current_health_width, 5)
        pygame.draw.rect(screen, (0, 255, 0), health_bar_rect)  # Green for current health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Enemy is destroyed
        return False

    def freeze(self, duration):
        self.frozen = True
        self.frozen_timer = duration

    def unfreeze(self):
        self.frozen = False
        self.frozen_timer = 0

    def apply_burn(self, duration, damage):
        self.burn_duration = duration
        self.burn_damage = damage
        self.burn_delay = True  # Set delay to skip immediate damage


class BasicEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 0, 0)  # Red
        self.speed = 2
        self.health = 100
        self.max_health = 100
        self.coin_reward = 10

class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 0)  # Green
        self.speed = 4
        self.health = 50
        self.max_health = 50
        self.coin_reward = 15

class TankEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (128, 128, 128)  # Gray
        self.speed = 1
        self.health = 200
        self.max_health = 200
        self.coin_reward = 20

class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (148, 0, 211)  # Purple
        self.size = 40  # Bigger size
        self.speed = 1.5
        self.health = 500
        self.max_health = 500
        self.coin_reward = 100

    def draw(self, screen):
        # Main body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
        # Crown on top
        crown_points = [
            (self.x + self.size//4, self.y - 10),
            (self.x + self.size//2, self.y - 20),
            (self.x + 3*self.size//4, self.y - 10),
            (self.x + self.size, self.y),
            (self.x, self.y)
        ]
        pygame.draw.polygon(screen, (255, 215, 0), crown_points)  # Gold crown

        # Health bar
        health_bar_width = self.size
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 30, health_bar_width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 30, current_health_width, 5))
