from src.Genetics.Gene import Gene
import src.Logic.Othello_logic
from src.Agent import Tree
from src.Logic.Othello_logic import Player

othello_logic = src.Logic.Othello_logic


class AgentVsAgent:
    """ in this class game logic for agent vs agent game is implemented
        used in genetic algorithm for learning purpose"""

    def __init__(self, gene1: Gene, gene2: Gene):
        self.gene1 = gene1
        self.gene2 = gene2
        self.game_logic = othello_logic.OthelloLogic()
        self.DEPTH_IN_TREE = 0
        self.winner_gene = None
        self.start_game()

    def move_agent(self):
        """ makes a movement using Minimax algorithm and changes the turn if the opponent has any movements.
            called for both agent1 and agent2 """

        player_ch = othello_logic.BLACK if self.game_logic.turn == Player.BLACK.value else othello_logic.WHITE
        opponent_ch = othello_logic.WHITE if self.game_logic.turn == Player.BLACK.value else othello_logic.BLACK
        player_gene = self.get_player_gene(player_ch)

        # find the target cell using Minimax algorithm
        state_node = Tree.Node(self.game_logic, self.DEPTH_IN_TREE)
        self.game_logic.minimax.set_weight_list(player_gene.weight_list)
        (dest_row, dest_col) = self.game_logic.minimax.minimax_with_alpha_beta(state_node, player_ch)

        # increment depth in game tree (a hypothetical tree that is not stored)
        self.DEPTH_IN_TREE += 1

        # make the movement for the agent whose turn is now
        self.game_logic.check_movements(player_ch, dest_row, dest_col, True)

        # change the turn if the opponent has any moves
        if self.game_logic.player_has_any_moves(opponent_ch, True):
            self.game_logic.turn = Player.WHITE.value if self.game_logic.turn == Player.BLACK.value else Player.BLACK.value

    def start_game(self):
        """ called when the class is instantiated
            starts agent vs agent game
            sets the winning gene in self.winner_gene
         """

        # main loop of the agent vs agent game
        while not self.game_logic.end_of_game():
            self.move_agent()

        winner_color = self.game_logic.find_winner()
        if winner_color == othello_logic.EMPTY:  # the game ended in a draw
            self.winner_gene = None
        else:
            self.winner_gene = self.get_player_gene(winner_color)

    def get_player_gene(self, player_color):
        return self.gene1 if player_color == othello_logic.BLACK else self.gene2

    def get_winner(self):
        return self.winner_gene
