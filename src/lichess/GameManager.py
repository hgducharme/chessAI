from ChessGame import ChessGame

class GameManager:
    def __init__(self):
        self.games = {}

    def start_new_game(self, game_info):
        game = ChessGame(game_info)
        game_id = game_info["game"]["fullId"]
        self.games[game_id] = game

    def do_games_exist(self):
        if (self.number_of_games() > 0):
            return True
        
        return False
    
    def number_of_games(self):
        return len(self.games)