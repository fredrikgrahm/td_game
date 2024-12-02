import pygame
from main import Shop

class TestEventHandling:
    def setUp(self):
        pygame.init()
        self.screen = None
        self.shop = Shop()
        self.player_coins = 100
        self.towers = []

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    pass
