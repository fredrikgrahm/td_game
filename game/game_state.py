class GameState:
    START_SCREEN = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    SCOREBOARD_SCREEN = 3

    def __init__(self):
        self.state = self.START_SCREEN

    def set_start_screen(self):
        self.state = self.START_SCREEN

    def set_running(self):
        self.state = self.GAME_RUNNING

    def set_game_over(self):
        self.state = self.GAME_OVER

    def set_scoreboard_screen(self):
        self.state = self.SCOREBOARD_SCREEN

    def is_start_screen(self):
        return self.state == self.START_SCREEN

    def is_running(self):
        return self.state == self.GAME_RUNNING

    def is_game_over(self):
        return self.state == self.GAME_OVER
    
    def is_scoreboard_screen(self):
        return self.state == self.SCOREBOARD_SCREEN
