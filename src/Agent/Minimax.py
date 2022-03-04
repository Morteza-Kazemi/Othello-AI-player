import random
import copy
import src.Agent.Tree as Tree
import src.Agent.Heuristic as Heuristic
import src.Logic.Othello_logic as Othello_logic

# Constant values
MAX_VALUE = float('inf')  # +infinity
MIN_VALUE = float('-inf')  # -infinity
MAX_DEPTH = 4  # TODO: may need to be changed(originally: 9 / for learn: 5)
NUM_OF_FEATURES = 9  # todo: change
CLOSE_TO_END_DEPTH = 64 - MAX_DEPTH


def opponent_color(color):
    return Othello_logic.BLACK if color == Othello_logic.WHITE else Othello_logic.WHITE


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


class Minimax:

    def __init__(self, othello_logic, weight_list):
        self.othello_logic = othello_logic
        self.weight_list = weight_list

    def minimax_with_alpha_beta(self, state_node, color):
        """ Minimax with alpha beta pruning """
        (best_score, best_move) = self.max_alpha_beta(state_node, color, 0, MIN_VALUE, MAX_VALUE)  # Depth is zero here
        # print("final: ", best_score, " ", best_move)
        return best_move

    def max_alpha_beta(self, state_node, color, depth, alpha, beta):
        """ Minimax with alpha beta pruning :part 1
        finds the best move and its best score for a max node
        """
        # Stop diving when reaching to the specific depth
        if depth == MAX_DEPTH or state_node.othello_logic.end_of_game():
            return self.utility(state_node), None

        # Get all possible actions for this color
        actions = state_node.othello_logic.get_possible_moves(color)
        # If there is no possible actions
        if not actions:
            return self.utility(state_node), None

        # sort and select (three) most promising actions or select all actions if it's nearly end of the game
        actions = self.most_promising_actions(actions, state_node, True)

        best_score = MIN_VALUE
        best_move = None
        # check all promising actions and find the best move and its best score
        for action in actions:
            new_node = self.next_node(action, state_node)
            # Find alpha-beta for Min node (opponent player)
            temp_tuple = self.min_alpha_beta(new_node, opponent_color(color), depth + 1, alpha, beta)
            temp_score = temp_tuple[0]
            # Update best score and move if needed
            if temp_score > best_score:
                best_score = temp_score
                best_move = action
            # Pruning, if possible
            if best_score >= beta:
                return best_score, best_move
            alpha = max(alpha, best_score)
        return best_score, best_move

    def min_alpha_beta(self, state_node, color, depth, alpha, beta):
        """ Minimax with alpha beta pruning :part 2
        finds the best move and its best score for a min node
        """
        # Stop diving when reaching to the specific depth
        if depth == MAX_DEPTH or state_node.othello_logic.end_of_game():
            return self.utility(state_node), None

        # Get all possible actions for this color
        actions = state_node.othello_logic.get_possible_moves(color)

        # If there is no possible actions
        if not actions:
            return self.utility(state_node), None

        # sort and select three most promising actions or select all actions if it's nearly end of the game
        actions = self.most_promising_actions(actions, state_node, False)

        best_score = MAX_VALUE
        best_move = None
        # check all promising actions and find the best move and its best score
        for action in actions:
            new_node = self.next_node(action, state_node)
            # Find alpha-beta for Max node (opponent player)
            temp_tuple = self.max_alpha_beta(new_node, opponent_color(color), depth + 1, alpha, beta)
            temp_score = temp_tuple[0]
            # Update best score and move if needed
            if temp_score < best_score:
                best_score = temp_score
                best_move = action
            # Pruning, if possible
            if best_score <= alpha:
                return best_score, best_move
            beta = min(beta, best_score)
        return best_score, best_move

    def utility(self, state_node):
        """ Evaluates the utility of given state according to features """
        total = 0
        agent = Othello_logic.WHITE
        player = Othello_logic.BLACK
        # Evaluate the weighted score for color and add it to the total
        features = Heuristic.Features(state_node, agent)
        feature_list = features.get_features()
        for i in range(0, NUM_OF_FEATURES):
            total += self.weight_list[i] * feature_list[i]

        # Evaluate the weighted score for opponent color and subtract it from the total
        opponent_features = Heuristic.Features(state_node, player)
        feature_list = opponent_features.get_features()
        for i in range(0, NUM_OF_FEATURES):
            total -= self.weight_list[i] * feature_list[i]

        # Return the total weighted score
        return total

    @staticmethod
    def next_node(action, state_node):
        """ Gives a new node performing the given action on the given node """
        new_othello_logic = copy.deepcopy(state_node.othello_logic)  # copy board info to another node
        new_node = Tree.Node(new_othello_logic, state_node.depth + 1)  # Execute action on newly created board
        new_othello_logic.move(action[0], action[1])
        return new_node

    def most_promising_actions(self, actions, state_node, reverse):
        """ gets a list of actions and sorts the actions either with descending or ascending order based on the
        caller function (min_alpha_beta or max_alpha_beta) -> in order to get better cuts on the Minimax tree
        returns the three most promising actions to decrease the
        Minimax tree width (therefore a Minimax tree depth can be increased)
        returns all possible actions if the node has a depth less than CLOSE_TO_END_DEPTH for a better search in
        final movements
        """

        pairs = self.create_pairs_of_utility_action(actions, state_node)
        pairs.sort(reverse=reverse, key=self.cmp_utils)
        if state_node.depth < CLOSE_TO_END_DEPTH:
            actions = [pairs[0][1]]
            if len(pairs) > 1:
                actions.append(pairs[1][1])
            if len(pairs) > 2:
                actions.append(pairs[2][1])
            # if len(pairs) > 3:
            #     actions.append(pairs[3][1])
        else:
            for pair in pairs:
                actions.append(pair[1])
        return actions

    @staticmethod
    def cmp_utils(pair):
        """ compares (utility, move) pairs based on utility """
        return pair[0]

    def create_pairs_of_utility_action(self, actions, state_node):
        """ calculates utility function for every action and adds the actions and their corresponding utility value
        to a list of pairs """
        pairs = []
        for action in actions:
            new_node = self.next_node(action, state_node)
            util = self.utility(new_node)
            pairs.append((util, action))
        return pairs

    def set_weight_list(self, weight_list):
        self.weight_list = weight_list
