from tic_tac_toe.game.engine import TicTacToe

from .args import parse_args
from .renderers import ConsoleRenderer


def main():
    player1, player2, starting_mark = parse_args()
    renderer = ConsoleRenderer()

    game = TicTacToe(player1, player2, renderer)
    game.play(starting_mark)
