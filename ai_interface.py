import math

from player_interface import PlayerInterface
import copy


class AiInterface(PlayerInterface):
    """
    A class that keeps track of the board,
    checks weather the game is terminated or not and
    finds the best possible move within 5 levels of
    depth using a simple recursive algorithm

    Attributes
    ----------
    size : int
        the size of the board.
    amount : int
        the amount of marks needed for the game to end.
    ---------
    """
    states = dict()
    max_depth = 5

    def make_a_move(self):
        """
        Makes the next best known move.
        """
        AiInterface.states.clear()
        print(f'Player {self.id+1} makes a move')
        best_move = self.solve(PlayerInterface.current, True)
        PlayerInterface.current.set_request(best_move[0], best_move[1], self.id)

    def solve(self, board, maximizing, depth=0):
        """
        Finds the best next move using the minimax algorithm
        :param maximizing: weather the algorithm is maximizing or minimizing the answer
        :param board: current state of the board
        :param depth: the depth of recursion
        :return: returns the best board (most wins) and its score
        """
        term = board.terminated()
        if term == self.get_num():
            return 1
        elif term == 2:
            return 0
        elif term == -self.get_num():
            return -1

        if depth == AiInterface.max_depth:
            return 0

        if board.to_string() in AiInterface.states:
            return AiInterface.states[board.to_string()]

        score = -2*maximizing + 1
        best_move = None

        for i in range(self.size):
            for j in range(self.size):
                if board.cells[i][j] == 0:
                    board.cells[i][j] = self.get_num() * (1-2*(depth % 2))
                    if maximizing:
                        new_score = self.solve(board, False, depth + 1)
                        if new_score > score or best_move is None:
                            best_move = (i, j)
                            score = new_score
                    else:
                        new_score = self.solve(board, True, depth + 1)
                        if new_score < score or best_move is None:
                            best_move = (i, j)
                            score = new_score
                    board.cells[i][j] = 0
                    if score == 2*maximizing-1:
                        break
        AiInterface.states[board.to_string()] = score
        if depth == 0:
            return best_move
        return score

    def __init__(self, size, amount, plr_id):
        """
        :param size: the size of the board
        :param amount: the amount of marks for the game to end.
        """
        super().__init__(size, amount, plr_id)
