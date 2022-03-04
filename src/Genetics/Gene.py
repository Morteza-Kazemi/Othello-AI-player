class Gene:
    def __init__(self, weight_list):
        self.weight_list = weight_list
        self.total_games = 0
        self.total_wins = 0
        self.fitness = 0

    def fitness_calc(self):
        self.fitness = self.total_wins / self.total_games

    def increment_total_game(self):
        self.total_games += 1

    def increment_for_winning(self):
        self.total_wins += 2

    def increment_for_tie(self):
        self.total_wins += 1

