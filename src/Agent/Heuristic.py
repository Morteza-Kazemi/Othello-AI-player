from src.Logic.Othello_logic import *

# Constant values
ROW_SIZE = 8
COLUMN_SIZE = 8
MIN_NUM = 0  # Min row/col number
MAX_NUM = ROW_SIZE - 1  # Max row/col number. That is 7 for this game
NORMALIZATION_CONST8 = 2
NORMALIZATION_CONST12 = 3
NORMALIZATION_CONST64 = 6


# Helper functions
def is_corner(x, y, index):  # Can detect Main corner or secondary corners according to given index
    helper1 = MIN_NUM + index
    helper2 = MAX_NUM - index
    return ((x == y == helper1) | (x == y == helper2) |
            ((x == helper1) & (y == helper2)) |
            ((x == helper2) & (y == helper1)))


def on_edge_and_not_corner(x, y, index):
    helper1 = MIN_NUM + index
    helper2 = MAX_NUM - index
    return (((x == MIN_NUM) & ((y == helper1) | (y == helper2))) |
            ((x == MAX_NUM) & ((y == helper1) | (y == helper2))) |
            ((y == MIN_NUM) & ((x == helper1) | (x == helper2))) |
            ((y == MAX_NUM) & ((x == helper1) | (x == helper2))))


def inside_edge_and_not_corner(x, y, index):
    helper1 = MIN_NUM + index
    helper2 = MAX_NUM - index
    return (((x == helper1) & (helper1 + 1 <= y <= helper2 - 1)) |
            ((x == helper2) & (helper1 + 1 <= y <= helper2 - 1)) |
            ((y == helper1) & (helper1 + 1 <= x <= helper2 - 1)) |
            ((y == helper2) & (helper1 + 1 <= x <= helper2 - 1)))


class Features:
    def __init__(self, state_node, color):
        self.board = state_node.othello_logic.board
        self.color = color
        """ Features that shown in the matrix below:
        [1, 2, 3, 4, 4, 3, 2, 1],
        [2, 5, 6, 6, 6, 6, 5, 2],
        [3, 6, 7, 8, 8, 7, 6, 3],
        [4, 6, 8, 8, 8, 8, 6, 4],
        [4, 6, 8, 8, 8, 8, 6, 4],
        [3, 6, 7, 8, 8, 7, 6, 3],
        [2, 5, 6, 6, 6, 6, 5, 2],
        [1, 2, 3, 4, 4, 3, 2, 1]
        """
        self.corners = 0  # 1
        self.edges_next_to_corner = 0  # 2  # negative feature in feature list *NORMALIZATION_CONST =2*
        self.useful_edges = 0  # 3 *NORMALIZATION_CONST =2*
        self.middle_edges = 0  # 4 *NORMALIZATION_CONST =2*
        self.corners_of_one_before_edge = 0  # 5  # negative feature in feature list
        self.one_before_edge_normal = 0  # 6  # negative feature in feature list *NORMALIZATION_CONST =3*
        self.middle_square_corners = 0  # 7
        self.middle_square_normal = 0  # 8 *NORMALIZATION_CONST =3*
        self.point_difference = 0  # (number of color disks - number of opponent disks) *NORMALIZATION_CONST =6*
        self.feature_list = []
        self.set_features()
        # todo other feature: num of moves and num of opponent moves

    def set_features(self):
        """ find each feature according to board and color
            then append them to feature_list """
        for x in range(ROW_SIZE):
            for y in range(COLUMN_SIZE):
                if self.board[x][y] == self.color:
                    self.point_difference += 1
                    # Corner cells
                    if is_corner(x, y, 0):
                        self.corners += 1

                    # Cells on the edges that are next to the corners
                    if on_edge_and_not_corner(x, y, 1):
                        self.edges_next_to_corner += 1

                    # Cells on the edges that have most utility than others on the edge
                    if on_edge_and_not_corner(x, y, 2):
                        self.useful_edges += 1

                    # Cells on the edges that are in two middle rows or colomns
                    if on_edge_and_not_corner(x, y, 3):
                        self.middle_edges += 1

                    # Cells on the rows/columns that are next to the edge rows/columns
                    # Here these cells are also corners
                    if is_corner(x, y, 1):
                        self.corners_of_one_before_edge += 1
                    # Here these cells are not corners
                    if inside_edge_and_not_corner(x, y, 1):
                        self.one_before_edge_normal += 1

                    # Cells inside the 4*4 square in the middle
                    # Here these cells are the corners of this square
                    if is_corner(x, y, 2):
                        self.middle_square_corners += 1
                    # Here these cells are not in the corner of this 4*4 square
                    if inside_edge_and_not_corner(x, y, 2) | is_corner(x, y, 3):
                        self.middle_square_normal += 1
                else:  # it was an opponent disk
                    self.point_difference -= 1

        # negative features get a -1 coefficient when being inserted to the feature_list
        self.feature_list = [self.corners, -self.edges_next_to_corner/NORMALIZATION_CONST8, self.useful_edges/NORMALIZATION_CONST8,
                             self.middle_edges/NORMALIZATION_CONST8, -self.corners_of_one_before_edge,
                             -self.one_before_edge_normal/NORMALIZATION_CONST12, self.middle_square_corners,
                             self.middle_square_normal/NORMALIZATION_CONST12, self.point_difference/NORMALIZATION_CONST64]

    # Getter
    def get_features(self):
        return self.feature_list
