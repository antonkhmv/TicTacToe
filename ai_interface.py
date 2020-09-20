from player_interface import PlayerInterface


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
        print(f'Player {self.id + 1} makes a move')
        if self.size > 3 and all(map(lambda x: x == '.', PlayerInterface.current.to_string())):
            best_move = [0, 0]
        else:
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

        score = 0
        best_score = (-2 * maximizing + 1) * 1000000
        best_move = None
        bestest_move = None  # makes sure the ai chooses a winning move
        bestestest_move = None  # makes sure the ai does not choose a losing move

        for i in range(self.size):
            for j in range(self.size):
                # if current cell is empty
                if board.cells[i][j] == 0:
                    # set it to the opposite of the current mark
                    board.cells[i][j] = -self.get_num() * (1 - 2 * (depth % 2))
                    # check for guaranteed losses
                    if board.terminated() == -self.get_num():
                        bestestest_move = (i, j)
                    # set this cell to the current mark
                    board.cells[i][j] = self.get_num() * (1 - 2 * (depth % 2))
                    if maximizing:
                        # maximize the score
                        new_score = self.solve(board, False, depth + 1)
                        if new_score > best_score or best_move is None:
                            best_move = (i, j)
                            best_score = new_score
                        if board.terminated() == self.get_num():
                            bestest_move = (i, j)
                    else:
                        # minimize the score
                        new_score = self.solve(board, True, depth + 1)
                        if new_score < best_score or best_move is None:
                            best_move = (i, j)
                            best_score = new_score
                    score += new_score
                    board.cells[i][j] = 0
        if bestestest_move is not None:
            bestest_move = bestestest_move
        if bestest_move is not None:
            best_move = bestest_move
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
