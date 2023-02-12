import argparse
from typing import NamedTuple

from tic_tac_toe.game.players import (
    HeuristicComputerPlayer,
    MinimaxComputerPlayer,
    Player,
    PrecomputedComputerPlayer,
    PruningComputerPlayer,
    RandomComputerPlayer,
)
from tic_tac_toe.logic.models import Mark

from .players import ConsolePlayer

PLAYER_CLASSES = {
    'human': ConsolePlayer,
    'computer': RandomComputerPlayer,
    'minimax': MinimaxComputerPlayer,
    'heuristic': HeuristicComputerPlayer,
    'pruning': PruningComputerPlayer,
    'precomputed': PrecomputedComputerPlayer,
}


class Args(NamedTuple):
    player1: Player
    player2: Player
    starting_mark: Mark


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument('-X', dest='player_x')
    parser.add_argument('-O', dest='player_o')
    parser.add_argument(
        '-s', '--starting', dest='starting_mark', choices=Mark, type=Mark, default='X'
    )

    args = parser.parse_args()
    player1 = PLAYER_CLASSES[args.player_x](Mark('X'))
    player2 = PLAYER_CLASSES[args.player_o](Mark('O'))
    starting_mark = args.starting_mark

    if starting_mark == 'O':
        player1, player2 = player2, player1

    return Args(player1, player2, starting_mark)
