import src.Logic.Othello_logic
from tkinter import *

# Constant values
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BG_COLOR = '#580000'  # red
BOARD_COLOR = '#696969'  # gray
ROW_SIZE, COLUMN_SIZE = (8, 8)
FONT = ('Courier', 30, 'bold')
TITLE_FONT = ('Courier', 25)
othello_logic = src.Logic.Othello_logic


# *************************** Game Board ************************
class GameBoard:
    """
        Contains all the elements that you see on the board
        including the cells and the disks in proper cells
    """

    def __init__(self, main_window, game_logic):
        # Draw a square for game board
        self.root = Canvas(master=main_window,
                           width=WINDOW_WIDTH,
                           height=WINDOW_HEIGHT,
                           bg=BOARD_COLOR,
                           cursor="hand2")
        self.root.pack(side=LEFT, padx=20, pady=20)
        self.game_logic = game_logic

        # Create game board once get an instance of GameBoard class
        self.create_game_board()

    def create_game_board(self):
        """ Draw vertical and horizontal lines to have cells, then put the initial disks """
        # self.root.delete()
        self.root.update()
        cell_height = self.get_cell_height()
        cell_width = self.get_cell_width()

        # Draw the horizontal lines of game board
        for row_num in range(1, ROW_SIZE):
            self.root.create_line(0, row_num * cell_height, self.get_board_height(), row_num * cell_height)

        # Draw the vertical lines
        for col_num in range(1, COLUMN_SIZE):
            self.root.create_line(col_num * cell_width, 0, col_num * cell_width, self.get_board_width())

        # Draw disks (in here, we just have 4)
        self.draw_disks()

    def draw_disks(self):
        """ Draw disks with proper colors in proper cells according to state of game_logic """
        cell_height = self.get_cell_height()
        cell_width = self.get_cell_width()
        for row in range(ROW_SIZE):
            for col in range(COLUMN_SIZE):
                if self.game_logic.get_board()[row][col] != othello_logic.EMPTY:
                    self.root.create_oval(
                        col * cell_width,  # top left point of the box in which the circle is drawn
                        row * cell_height,
                        (col + 1) * cell_width,  # bottom right point of the box
                        (row + 1) * cell_height,
                        outline=BG_COLOR,
                        fill=('Black' if (self.game_logic.get_board()[row][col] == 'b') else 'White'),
                        width=2)

    # Getter functions
    def get_root(self):
        return self.root

    def get_board_height(self):
        return self.root.winfo_height()

    def get_board_width(self):
        return self.root.winfo_width()

    def get_cell_height(self):
        """ Get height of the cell, that is equal for all cells """
        return self.get_board_height() / ROW_SIZE

    def get_cell_width(self):
        """ Get width of the cell, that is equal for all cells """
        return self.get_board_width() / COLUMN_SIZE


# *************************** Score Board ************************
class ScoreBoard:
    """
        Contains a title and two labels with black and white background
        black label's text is black player's score and the same for white label
    """

    def __init__(self, main_window, game_logic):
        # Integer value of scores from logic
        self.black_score = game_logic.score_calculate(othello_logic.BLACK)
        self.white_score = game_logic.score_calculate(othello_logic.WHITE)

        # Title of score board
        self.score_board_title = Label(master=main_window,
                                       text="Score Board",
                                       background=BG_COLOR,
                                       fg='white',
                                       font=TITLE_FONT).pack(side=TOP, pady=(30, 0))

        # Black label that displays black player's score
        self.black_score_label = Label(master=main_window,
                                       text=str(self.black_score),
                                       background='black',
                                       fg='white',
                                       font=FONT,
                                       width=10)
        self.black_score_label.pack(side=TOP, padx=(20, 20), pady=(20, 0))

        # White label that displays white player's score
        self.white_score_label = Label(master=main_window,
                                       text=str(self.white_score),
                                       background='white',
                                       fg=BG_COLOR,
                                       font=FONT,
                                       width=10)
        self.white_score_label.pack(side=TOP)

    def update_score_board(self, game_logic):
        """ Update the numbers on score board for each new movements """
        # calculate new scores for black and white
        self.black_score = game_logic.score_calculate(othello_logic.BLACK)
        self.white_score = game_logic.score_calculate(othello_logic.WHITE)
        # change score board numbers
        self.black_score_label['text'] = str(self.black_score)
        self.white_score_label['text'] = str(self.white_score)


# *************************** Turn Section ************************
class Turn:
    """
        Contains a title and a square shaped label with white/black background
        when the square is black means it's black player's turn;
        same meaning for white background
    """

    def __init__(self, main_window, game_logic):
        # Get turn from the logic
        self.player_turn = game_logic.get_turn()

        # Title for turn section
        self.turn_title = Label(master=main_window,
                                text="Turn",
                                background=BG_COLOR,
                                fg="White",
                                font=TITLE_FONT)
        self.turn_title.pack(side=TOP, padx=(20, 20), pady=(150, 5))

        # Colored label to show turn
        self.turn_label = Label(master=main_window,
                                background='black',
                                width=8,
                                height=4)
        self.turn_label.pack(side=TOP, padx=(20, 20), pady=(0, 0))

    def toggle_turn(self, game_logic, game_board):
        """ Switch the turn between players once a player do a movement """
        self.player_turn = game_logic.get_turn()
        self.turn_label["background"] = self.player_turn
        # game_board.get_root().configure(cursor="dot")

    def display_winner(self, main_window, winner):
        """ Eliminate two labels for turn display and show winner """
        self.turn_title.destroy()
        self.turn_label.destroy()

        # New Label to show winner
        winner_label = Label(master=main_window,
                             background=BG_COLOR,
                             fg="white",
                             font=FONT)
        winner_label.pack(side=TOP, padx=(15, 0), pady=(150, 5))

        if winner == 'b':
            winner_label["text"] = "Black Wins!"
        elif winner == 'w':
            winner_label["text"] = "White Wins!"
        else:
            winner_label["text"] = "Tie!"
            self.turn_label = Label(master=main_window,
                                    background=BG_COLOR,
                                    text="The End",
                                    fg="white",
                                    font=FONT).pack(side=TOP, padx=(20, 20), pady=(0, 0))
