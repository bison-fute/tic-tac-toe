import enum
import random
import re
from dataclasses import dataclass
from functools import cached_property
from typing import List

from tic_tac_toe.logic import validators
from tic_tac_toe.logic.exceptions import UnknownGameState

WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)


class Mark(str, enum.Enum):
    """
    Enumerate the players' marks.
    """

    NAUGHT = 'O'
    CROSS = 'X'

    @property
    def other(self) -> 'Mark':
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT


@dataclass(frozen=True)
class Grid:
    """
    Describes an immutable grid.
    Because the class is frozen, property can be cashed to make sure they are only called once.
    """

    cells: str = ' ' * 9

    def __post_init__(self):
        validators.validate_grid(self)

    @cached_property
    def x_count(self) -> int:
        return self.cells.count('X')

    @cached_property
    def o_count(self) -> int:
        return self.cells.count('O')

    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(' ')


@dataclass(frozen=True)
class Move:
    mark: Mark
    cell_index: int
    before_state: 'GameState'
    after_state: 'GameState'


@dataclass(frozen=True)
class GameState:

    grid: Grid
    starting_mark: Mark = Mark('X')

    def __post_init__(self):
        validators.validate_game_state(self)

    @cached_property
    def current_mark(self):
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other

    @cached_property
    def not_started(self) -> bool:
        return self.grid.empty_count == 9

    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie

    @cached_property
    def tie(self) -> bool:
        return self.grid.empty_count == 0 and self.winner is None

    @cached_property
    def winner(self) -> Mark | None:
        for winning_pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(
                    pattern=winning_pattern.replace('?', mark.value), string=self.grid.cells
                ):
                    return mark
        return None

    @cached_property
    def winning_cells(self) -> List[int]:
        for winning_pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(
                    pattern=winning_pattern.replace('?', mark),
                    string=self.grid.cells,
                ):
                    return [
                        match.start()
                        for match in re.finditer(
                            pattern=r'\?',
                            string=winning_pattern,
                        )
                    ]
        return []

    @cached_property
    def possible_moves(self) -> List[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(pattern=' ', string=self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves

    def make_move_to(self, index: int) -> Move | None:
        validators.validate_move(self, index)
        next_index = index + 1
        new_cells = (
            self.grid.cells[:index] + self.current_mark.value + self.grid.cells[next_index:]
        )
        return Move(
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=GameState(grid=Grid(new_cells), starting_mark=self.starting_mark),
        )

    def evaluate_score(self, mark: Mark, heuristic=False):
        if self.game_over:
            if self.tie:
                return 0
            elif self.winner is mark:
                return 1
            else:
                return -1
        elif heuristic:
            return -1
        raise UnknownGameState('The game is not over yet.')

    def make_random_move(self):
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None
