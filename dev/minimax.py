from typing import List

from tic_tac_toe.logic.minimax import minimax
from tic_tac_toe.logic.models import GameState, Grid, Mark


def preview_cells(cells: str):
    print(cells[:3], cells[3:6], cells[6:9], sep='\n')


game_state = GameState(grid=Grid('XXO O X O'), starting_mark=Mark('X'))
for move in game_state.possible_moves:
    score = minimax(Mark('X'), move)
    print(f'{score=}')
    preview_cells(move.after_state.grid.cells)
    print('-' * 10)
