"""
    ****************** Othello Game ********************
    ** Artificial Intelligence course - final project **
    **** Written by Shiva Zeymaran & Morteza Kazemi ****
    ******************* Fall 2020 **********************
"""

import src.Agent.Minimax
import src.Agent.Tree
from enum import Enum


class Player(Enum):
    BLACK = "Black"
    WHITE = "White"


# This Exception will raised when invalid move occurs
class MovementError(Exception):
    """ Invalid move occurs """


# Constant values
ROW_SIZE, COLUMN_SIZE = (8, 8)
BLACK = 'b'
WHITE = 'w'
EMPTY = '_'

Minimax = src.Agent.Minimax
Tree = src.Agent.Tree
possible_moves = []  # List of possible actions

OPTIMUM_WEIGHTS = [51, 151, 74, 97, 103, 78, 151, 126, 26]
# [97, 113, 49, 159, 153, 38, 128, 104, 3]  one hour training
# [120, 20, 40, 5, 40, 5, 15, 3, 3]         phase 2 weights
# [110, 99, 142, 116, 116, 76, 67, 120, 4]  new train in depth 2


def init_game_board():
    """ Initialize the game board with 2D array and fill the array """

    # Create 2D array for board with empty cells
    board = [[EMPTY for i in range(COLUMN_SIZE)] for j in range(ROW_SIZE)]

    # Initialize the 4 center disks
    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    return board


# This class controls the flow of game
class OthelloLogic:
    """ Everything about the game's logic """

    def __init__(self):
        # Attributes
        self.row_size = ROW_SIZE
        self.col_size = COLUMN_SIZE
        self.turn = Player.BLACK.value
        self.board = init_game_board()
        self.minimax = Minimax.Minimax(self, OPTIMUM_WEIGHTS)  # Make instance of Minimax class

    def move(self, row, col):  # this function is only called in the Minimax class
        """ Try to perform a movement to given cell
         used only in Minimax algorithm
         """

        player_ch = BLACK if self.turn == Player.BLACK.value else WHITE
        opponent_ch = WHITE if self.turn == Player.BLACK.value else BLACK

        # Check if the movement is valid (destination cell should be on board and also be empty)
        try:
            if self.valid_cell(row, col):
                if self.check_movements(player_ch, row, col, False):
                    self.check_movements(player_ch, row, col, True)
                    if self.player_has_any_moves(opponent_ch, True):
                        self.turn = Player.WHITE.value if self.turn == Player.BLACK.value else Player.BLACK.value
                else:
                    return
            else:
                raise MovementError()
        except MovementError:
            pass

    def valid_cell(self, row, col):
        """ Check if the desired cell is within the board's boundary and selected cell is empty """
        if (0 <= row < self.row_size) & (0 <= col < self.col_size) & (self.board[row][col] == EMPTY):
            return True
        else:
            return False

    def score_calculate(self, player_color):
        """ Count the total number of disks with the color of player_color """
        score = 0
        for row in range(ROW_SIZE):
            for col in range(COLUMN_SIZE):
                if self.board[row][col] == player_color:
                    score += 1
        return score

    def find_winner(self):
        """ Find winner by calculating score for each player """
        black_score = self.score_calculate(BLACK)
        white_score = self.score_calculate(WHITE)

        if black_score > white_score:  # black is winner
            return BLACK
        elif black_score < white_score:  # white is winner
            return WHITE
        else:  # tie
            return EMPTY

    def end_of_game(self):
        """ Check if game is ended when no one has any movements """
        if self.player_has_any_moves(BLACK, True) | self.player_has_any_moves(WHITE, True):
            return False
        return True

    def check_movements(self, player_ch, row, col, move):
        """ Checks if movement from (row, col) is possible and makes the moves if 'move' is true """
        opponent_ch = BLACK if player_ch == WHITE else WHITE

        moved = False
        dir_list = [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]

        for direction in dir_list:
            if self.check_direction(row, col, direction[0], direction[1], player_ch, opponent_ch, move):
                moved = True
        return moved

    def check_direction(self, row, col, x_dir, y_dir, player_ch, opponent_ch, move):
        """ Checks if movement from (row, col) in (x_dir, y_dir) direction is possible and makes the moves if 'move' is true """
        can_move = False
        x = row + x_dir
        y = col + y_dir
        first_time = True
        while -1 < x < ROW_SIZE and -1 < y < COLUMN_SIZE:
            if first_time:
                first_time = False
                if self.board[x][y] != opponent_ch:
                    break
            else:
                if self.board[x][y] == EMPTY:
                    break
                elif self.board[x][y] == opponent_ch:
                    x += x_dir
                    y += y_dir
                    continue
                elif self.board[x][y] == player_ch:
                    can_move = True
                    break
            x += x_dir
            y += y_dir
        # make the moves if it's desired(move) and possible(can_move)
        if can_move and move:
            x = row
            y = col
            while -1 < x < ROW_SIZE and -1 < y < COLUMN_SIZE:
                if x != row or y != col:  # if a move was made (any disks were swapped)
                    if self.board[x][y] == player_ch:
                        break
                self.board[x][y] = player_ch
                x += x_dir
                y += y_dir
        return can_move

    def player_has_any_moves(self, player_ch, check_only):
        """ checks if the player has any movements on board """
        for x in range(ROW_SIZE):
            for y in range(COLUMN_SIZE):
                if self.valid_cell(x, y):
                    if self.check_movements(player_ch, x, y, False):
                        # If the purpose is only check the player has any moves or not
                        if check_only:
                            return True
                        else:
                            # add coordination to the list of possible movements
                            possible_moves.append((x, y))
        if check_only:
            return False

    # For debug purposes
    def print_table(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j] if self.board[i][j] != EMPTY else 'n', end='')
            print()

    # Return list of possible movements for given player
    def get_possible_moves(self, player):
        possible_moves.clear()
        self.player_has_any_moves(player, False)
        return possible_moves  # if there is no move, the list will remain empty

    # Getter functions
    def get_turn(self):
        return self.turn

    def get_board(self):
        return self.board
