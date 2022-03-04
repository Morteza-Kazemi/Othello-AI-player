import src.Logic.Othello_logic
from src.Agent import Tree
from src.Logic.Othello_logic import Player
import src.Gui.Components
from tkinter import *

# Constant values
BG_COLOR = '#580000'  # red
othello_logic = src.Logic.Othello_logic
components = src.Gui.Components
BLACK = 'b'
WHITE = 'w'


class OthelloGui:
    """ Everything about the game's gui, using the components in Components.py """

    def __init__(self):
        # Make an instance from OthelloLogic for logical state of game
        self.game_logic = othello_logic.OthelloLogic()

        # Initialize window
        self.main_window = Tk()
        self.main_window.title('Othello')
        self.main_window.iconphoto(False, PhotoImage(file='icon.png'))
        self.main_window.configure(background=BG_COLOR)

        # Initialize all window components
        self.game_board = components.GameBoard(self.main_window, self.game_logic)
        self.score_board = components.ScoreBoard(self.main_window, self.game_logic)
        self.turn_section = components.Turn(self.main_window, self.game_logic)
        # Bind click event to game board
        self.game_board.get_root().bind('<Button-1>', self.click_on_board)
        # initialize minimax tree depth
        self.DEPTH_IN_TREE = 0

    def run(self):
        """ Call mainloop to run main window """
        self.main_window.mainloop()

    def click_on_board(self, event: Event):
        """ this function is called when the player(human) clicks on the board """
        self.move_in_gui(event, False)  # agent is False

    def move_in_gui(self, event: Event, agent):
        """Parameter agent:boolean shows if the caller of the function is an agent or human
        this function is called by click_on_board and itself and operates movements for both agent and human player
        """
        player_ch = othello_logic.BLACK if self.game_logic.turn == Player.BLACK.value else othello_logic.WHITE
        opponent_ch = othello_logic.WHITE if self.game_logic.turn == Player.BLACK.value else othello_logic.BLACK
        # find the target cell
        if agent:  # Find target cell using Minimax algorithm
            state_node = Tree.Node(self.game_logic, self.DEPTH_IN_TREE)
            (dest_row, dest_col) = self.game_logic.minimax.minimax_with_alpha_beta(state_node, player_ch)

        else:  # Find target cell by coordination of clicked spot (chosen cell on board)
            dest_row = int(event.y / self.game_board.get_cell_height())
            dest_col = int(event.x / self.game_board.get_cell_width())
            if (not (self.game_logic.valid_cell(dest_row, dest_col)) or
                    not (self.game_logic.check_movements(player_ch, dest_row, dest_col, False))):
                return

        self.DEPTH_IN_TREE += 1
        # make the movement for the player (agent or human)
        self.game_logic.check_movements(player_ch, dest_row, dest_col, True)

        # change the turn if the opponent has any moves
        if self.game_logic.player_has_any_moves(opponent_ch, True):
            self.game_logic.turn = Player.WHITE.value if self.game_logic.turn == Player.BLACK.value else Player.BLACK.value

        # if next turn is agent's turn execute its move
        if self.game_logic.turn == Player.WHITE.value:  # agent is the white player
            if self.game_logic.end_of_game():
                self.turn_section.display_winner(self.main_window, self.game_logic.find_winner())
                self.update_window_components()
                self.main_window.update()

            else:
                self.update_window_components()
                self.turn_section.toggle_turn(self.game_logic, self.game_board)  # Update turn in ui
                self.main_window.update()  # draw the game board
                self.move_in_gui(event, True)  # makes a movement for the agent (event is the same as null)

        # it's player turn so draw the game board and wait until 'click_on_board' is called with another player movement
        else:
            # Update all of the window components
            self.update_window_components()
            # Display winner instead of turn if game ended
            if self.game_logic.end_of_game():
                self.turn_section.display_winner(self.main_window, self.game_logic.find_winner())
            else:  # Update turn
                self.turn_section.toggle_turn(self.game_logic, self.game_board)

    def update_window_components(self):
        self.game_board.draw_disks()
        self.score_board.update_score_board(self.game_logic)


if __name__ == '__main__':
    OthelloGui().run()
