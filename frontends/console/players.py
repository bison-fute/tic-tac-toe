import re

from tic_tac_toe.game.players import Player
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Move


class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                index = grid_to_index(input(f'{self.mark}\'s move: ').strip())
            except ValueError:
                print('Give the coordinate in the format of A1 or 1A.')
            else:
                try:
                    return game_state.make_move_to(index)
                except InvalidMove:
                    print('That cell is already occupied.')
        return None


def grid_to_index(grid: str) -> int:
    if re.match(pattern='[abcABC][123]', string=grid):
        col, row = grid
    elif re.match(pattern='[123][abcABC]', string=grid):
        row, col = grid
    else:
        raise InvalidMove('Invalid  grid coordinates.')
    return 3 * (int(row) - 1) + ord(col.upper()) - ord('A')
