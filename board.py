class Board:
    """
    A class that records the current state of the board
    """

    def __init__(self, size, amount):
        """
        initializes the class
        :param size: the size of the board
        :param amount: the amount of marks on
        the board need for a win
        """
        self.amount = amount
        self.size = size
        self.cells = [[0] * size for i in range(size)]

    chars = ['.', 'X', 'O']

    def set_request(self, x, y, t):
        """
        if a cell is not taken, then it occupies it with an appropriate value
        :return: bool (false if not successful)
        """
        t = -2 * t + 1
        if not (0 <= x < self.size) or not (0 <= y <= self.size):
            return False
        if self.cells[x][y] == 0:
            self.cells[x][y] = t
            return True
        return False

    def print_state(self):
        """
        Prints the board to the console
        :return: void
        """
        for i in range(self.size):
            print("".join([Board.chars[self.cells[i][j]] for j in range(self.size)]))

    def run_checks(self, checks):
        """
        Runs termination checks for a given cell
        """
        first = [True] * len(checks)
        second = [True] * len(checks)
        for x in range(self.amount):
            pairs = list(map(lambda f: f(x), checks))
            for k, p in enumerate(pairs):
                if self.cells[p[0]][p[1]] != 1:
                    first[k] = False
                if self.cells[p[0]][p[1]] != -1:
                    second[k] = False
        if any(first):
            return 1
        if any(second):
            return -1
        return None

    def to_string(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                s += Board.chars[self.cells[i][j]]
        return s

    def terminated(self):
        """
        Returns a number which indicates if the player making
        the current move has won or lost (1 - win, -1 - loss, 2 - tie,
        0 - not terminated)
        :return: int
        """
        for i in range(self.size - self.amount + 1):
            # check for both diagonals, (some) verticals and horizontals,
            for j in range(self.size - self.amount + 1):
                checks = [lambda x: (i + x, j),  # check verticals
                          lambda x: (i, j + x),  # check horizontals
                          lambda x: (i + x, j + x),  # check main diagonals
                          lambda x: (i + x, self.size - 1 - j - x)]  # check secondary diagonals
                res = self.run_checks(checks)
                if res is not None:
                    return res

            # second check for leftover verticals and horizontals
            for j in range(self.size - self.amount + 1, self.size):
                checks = [lambda x: (i + x, j),  # check leftover verticals
                          lambda x: (j, i + x)]  # check leftover horizontals
                res = self.run_checks(checks)
                if res is not None:
                    return res
        tie = True
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    tie = False
        if tie:
            return 2
        return 0
