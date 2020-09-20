import argparse
from ai_interface import AiInterface
from player_interface import PlayerInterface

parser = argparse.ArgumentParser(description='Play a game Tic Tac Toe')
parser.add_argument('size', type=int, help='The size of the board (allowed values: [1,5])', choices=list(range(1, 6)))
parser.add_argument('amount', type=int, choices=list(range(1, 6)),
                    help='The amount of marks needed to win the game (allowed values: [1,5])')
parser.add_argument('P1', type=str, help='"p" for a real player, and "c" for computer', choices=['p', 'c'])
parser.add_argument('P2', type=str, help='"p" for a real player, and "c" for computer', choices=['p', 'c'])
args = parser.parse_args()
if args.amount > args.size:
    parser.error('Error: amount should not exceed size.')

if args.P1 == 'p':
    P1 = PlayerInterface(args.size, args.amount, 1)
else:
    P1 = AiInterface(args.size, args.amount, 1)

if args.P2 == 'p':
    P2 = PlayerInterface(args.size, args.amount, 2)
else:
    P2 = AiInterface(args.size, args.amount, 2)

while PlayerInterface.current.terminated() == 0:
    P1.make_a_move()
    PlayerInterface.current.print_state()
    if PlayerInterface.current.terminated() != 0:
        break
    P2.make_a_move()
    PlayerInterface.current.print_state()

t = PlayerInterface.current.terminated()
if t == 2:
    print("It's a tie!")
else:
    print(f'Player {1 if t == 1 else 2} wins!')
