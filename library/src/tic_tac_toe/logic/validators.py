from __future__ import annotations

import re
from typing import TYPE_CHECKING

from tic_tac_toe.logic.exceptions import InvalidGameState, InvalidMove

if TYPE_CHECKING:  # i.e. when package import, but False at runtime
    from tic_tac_toe.game.players import Player
    from tic_tac_toe.logic.models import GameState, Grid, Mark


def validate_grid(grid: Grid) -> None:
    if not re.match(pattern='[XO ]{9}', string=grid.cells):
        raise ValueError('Grid must contain Os, Xs or spaces.')


def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)


def validate_number_of_marks(grid: Grid) -> None:
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState('Wrong numbers of Xs and Os.')


def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count > grid.o_count:
        if starting_mark == 'O':
            raise InvalidGameState('Wrong starting mark.')
    if grid.x_count < grid.o_count:
        if starting_mark == 'X':
            raise InvalidGameState('Wrong starting mark.')
    return None


def validate_winner(grid: Grid, starting_mark: Mark, winner_mark: Mark | None) -> None:
    if winner_mark == 'X':
        if starting_mark == 'X':
            if grid.x_count <= grid.o_count:
                raise InvalidGameState('Wrong number of X.')
        else:
            if grid.x_count > grid.o_count:
                raise InvalidGameState('Wrong number of X.')
    if winner_mark == 'O':
        if starting_mark == 'O':
            if grid.x_count >= grid.o_count:
                raise InvalidGameState('Wrong number of O.')
        else:
            if grid.x_count < grid.o_count:
                raise InvalidGameState('Wrong number of X.')


def validate_move(game_state: GameState, move_index: int) -> None:
    if game_state.grid.cells[move_index] != " ":
        raise InvalidMove('The move is not possible.')


def validate_players(player1: Player, player2: Player):
    if player1.mark is player2.mark:
        raise ValueError('Players must have different marks.')
