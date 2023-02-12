import abc
import time

from tic_tac_toe.logic import minimax
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Mark, Move


class Player(metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark == game_state.current_mark:
            if move := self.get_move(game_state):  # Walrus operator
                return move.after_state
            raise InvalidMove('No more possible moves.')
        else:
            raise InvalidMove('It is the other player\'s turn.')

    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current's player's move in the give game state."""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark, delay_seconds: float = 0.3) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer's move in the given game state."""


class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.make_random_move()


class MinimaxComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.not_started:
            return game_state.make_random_move()
        else:
            return minimax.find_best_move(game_state)


class HeuristicComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.not_started:
            return game_state.make_random_move()
        else:
            return minimax.find_best_move(game_state, minimax_version='heuristic')


class PruningComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.not_started:
            return game_state.make_random_move()
        else:
            return minimax.find_best_move(game_state, minimax_version='pruning')


class PrecomputedComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.not_started:
            return game_state.make_random_move()
        else:
            return minimax.find_best_move_precomputed(game_state)
