import pygame
import random
from game.enemies import BasicEnemy, FastEnemy, TankEnemy, BossEnemy

class WaveManager:
    def __init__(self):
        self.total_waves = 10
        self.enemy_types = [BasicEnemy, FastEnemy, TankEnemy]
        self.reset()
        self.enemies_spawned_in_wave = 0  # Initialize counter

    def reset(self):
        self.current_wave = 0
        self.wave_in_progress = False
        self.next_wave_timer = pygame.time.get_ticks() + 3000  # Start initial 3-second timer
        self.time_between_waves = 5000  # 5000 ms (5 seconds)
        self.enemies_to_spawn = 0
        self.enemy_spawn_timer = 0  # Timer for spacing out enemy spawns
        self.time_between_enemy_spawns = 500  # 500 ms (0.5 seconds)
        self.enemies_spawned_in_wave = 0  # Reset counter

    def start_wave(self):
        self.current_wave += 1
        self.wave_in_progress = True
        if self.current_wave == 3:  # Boss wave
            self.enemies_to_spawn = 1  # Only spawn one boss
        else:
            self.enemies_to_spawn = self.current_wave
        self.enemy_spawn_timer = pygame.time.get_ticks()  # Initialize spawn timer
        self.enemies_spawned_in_wave = 0  # Reset counter at the start of each wave

    def get_enemy_type(self):
        if self.current_wave == 3:
            return BossEnemy
        # Increase chances of stronger enemies in later waves
        if self.current_wave < 3:
            return BasicEnemy
        elif self.current_wave < 6:
            return random.choice([BasicEnemy, FastEnemy])
        else:
            return random.choice(self.enemy_types)

    def get_time_until_next_wave(self):
        current_time = pygame.time.get_ticks()
        if self.next_wave_timer > current_time:
            return (self.next_wave_timer - current_time) // 1000  # Return time in seconds
        return 0

    def update(self, enemies_list):
        current_time = pygame.time.get_ticks()

        if not self.wave_in_progress and current_time >= self.next_wave_timer:
            self.start_wave()

        if self.wave_in_progress and self.enemies_spawned_in_wave > 0 and not enemies_list:
            self.wave_in_progress = False
            self.next_wave_timer = current_time + self.time_between_waves

        if self.wave_in_progress and self.enemies_to_spawn > 0:
            if current_time >= self.enemy_spawn_timer:
                EnemyType = self.get_enemy_type()
                enemy = EnemyType(0, 300)  # Position new enemies; adjust as needed
                enemies_list.append(enemy)
                self.enemies_to_spawn -= 1
                self.enemies_spawned_in_wave += 1  # Increment counter
                self.enemy_spawn_timer = current_time + self.time_between_enemy_spawns

    def draw_wave_message(self, screen, font):
        if not self.wave_in_progress and pygame.time.get_ticks() < self.next_wave_timer:
            if self.current_wave == 3:
                wave_text = font.render("You defeated the Boss!", True, (148, 0, 211))  # Purple text for boss
            else:
                wave_text = font.render(f"You defeated Wave: {self.current_wave}", True, (0, 0, 0))
            screen.blit(wave_text, (300, 50))
