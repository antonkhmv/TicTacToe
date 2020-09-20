from board import Board


class PlayerInterface:
    """
    A class responsible for keeping track of the board,
    registering the moves the player makes and
    """
    current = None

    def get_num(self):
        return -2 * self.id + 1

    def __init__(self, size, amount, plr_id):
        """
        :param size: the size of the board
        :param amount: the amount of marks for the game to end.
        """
        self.id = plr_id-1
        self.size = size
        self.amount = amount

        PlayerInterface.current = Board(size, amount)

    def make_a_move(self):
        while True:
            s = input(f'Player {self.id+1}, Enter a position on the board: ').split()
            if not all(map(lambda c: c.isdigit(), s)):
                print('Error: format error.')
                continue
            if not len(s) == 2:
                print('Error: you need to enter two numbers to set a mark.')
                continue
            x, y = map(int, s)
            if self.current.set_request(x, y, self.id):
                break
            print('Error: cell already filled or out of bounds.')
