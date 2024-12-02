import pygame
import json

class Scoreboard:
    def __init__(self):
        self.enemy_counts = {
            'BasicEnemy': 0,
            'FastEnemy': 0,
            'TankEnemy': 0,
            'BossEnemy': 0

        }
        self.wave_reached = 0
        self.coins_spent = 0
        self.top_scores = self.load_scores()

    def add_enemy_destroyed(self, enemy_type):
        if enemy_type in self.enemy_counts:
            self.enemy_counts[enemy_type] += 1
    def set_wave_reached(self, wave):
        self.wave_reached = wave

    def add_coins_spent(self, coins):
        self.coins_spent += coins  # Add the spent coins

    def save_Score(self):
        score = {
            'wave_reached': self.wave_reached,
            'coins_spent': self.coins_spent,
            'enemy_counts': self.enemy_counts
        }        
        self.top_scores.append(score)
        self.top_scores = sorted(self.top_scores, key=lambda x: x['wave_reached'], reverse=True)[:3]
        with open('top_scores.json', 'w') as f:
            json.dump(self.top_scores, f)
        
    def load_scores(self):
        try:
            with open('top_scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    

    def draw(self, screen, font):
        y_offset = 50
        title_text = font.render('Scoreboard', True, (0, 0, 0))
        screen.blit(title_text, (50, y_offset))
        y_offset += 30  

        for i, score in enumerate(self.top_scores):
            score_text = font.render(f'Rank {i + 1}: Wave {score["wave_reached"]}, Coins Spent {score["coins_spent"]}', True, (0, 0, 0))
            screen.blit(score_text, (50, y_offset))
            y_offset += 20
            for enemy_type, count in score['enemy_counts'].items():
                enemy_text = font.render(f'{enemy_type}: {count}', True, (0, 0, 0))
                screen.blit(enemy_text, (70, y_offset))
                y_offset += 20
            y_offset += 10