import json
import sys
from functools import partial
from importlib import resources
from typing import Dict, List

from tic_tac_toe.logic.models import GameState, Grid, Mark, Move

THIS_MODULE = sys.modules[__name__]


def minimax(move: Move, maximizer: Mark, choose_highest_score: bool = False) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    return (max if choose_highest_score else min)(
        minimax(next_move, maximizer, not choose_highest_score)
        for next_move in move.after_state.possible_moves
    )


def find_best_move(
    game_state: GameState,
    minimax_version: str = 'minimax',
) -> Move | None:
    minimax_func = getattr(THIS_MODULE, minimax_version)
    maximizer = game_state.current_mark
    bound_minimax = partial(minimax_func, maximizer=maximizer)
    print(f'{game_state.possible_moves=}')
    return max(game_state.possible_moves, key=bound_minimax)


def heuristic(
    move: Move, maximizer: Mark, choose_highest_score: bool = False, n_steps: int = 3
) -> int:
    if move.after_state.game_over or n_steps == 0:
        return move.after_state.evaluate_score(maximizer, heuristic=True)
    return (max if choose_highest_score else min)(
        heuristic(next_move, maximizer, not choose_highest_score, n_steps - 1)
        for next_move in move.after_state.possible_moves
    )


def pruning(
    move: Move, maximizer: Mark, choose_highest_score: bool = False, alpha: int = -1, beta: int = 1
) -> int:
    """
    Implementation of alpha-beta pruning for minimax algorithm optimization:
    alpha represents the minimum score that the maximizer is ensured,
    beta represents the maximum score that the minimizer is ensured,
    an optimum is found if alpha > beta.
    """
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    scores = []
    for next_move in move.after_state.possible_moves:
        scores.append(
            score := pruning(next_move, maximizer, not choose_highest_score, alpha, beta)
        )
        if choose_highest_score:
            alpha = max(alpha, score)
        else:
            beta = min(beta, score)
        if alpha > beta:
            break
    return (max if choose_highest_score else min)(scores)


class MinimaxSerializer:
    DEFAULT_FILENAME = 'precomputed_minimax.json'
    ScoreType = List[int]

    @staticmethod
    def scan_tree(scores: Dict[str, ScoreType], game_state: GameState) -> None:
        for move in game_state.possible_moves:
            scores[MinimaxSerializer.key(move)] = [
                minimax(move, Mark('X')),
                minimax(move, Mark('O')),
            ]
            MinimaxSerializer.scan_tree(scores, move.after_state)

    @staticmethod
    def precompute_scores() -> Dict[str, ScoreType]:
        scores = {}
        MinimaxSerializer.scan_tree(scores, GameState(Grid(), starting_mark=Mark('X')))
        MinimaxSerializer.scan_tree(scores, GameState(Grid(), starting_mark=Mark('O')))
        return scores

    @staticmethod
    def key(move: Move) -> str:
        return move.before_state.grid.cells + move.after_state.grid.cells

    @staticmethod
    def load(filename: str = DEFAULT_FILENAME):
        with resources.open_text(__package__, filename) as file:
            return json.load(file)

    @staticmethod
    def dump(filename: str = DEFAULT_FILENAME):
        with open(filename, mode='w') as file:
            json.dump(MinimaxSerializer.precompute_scores(), file)


def precomputed(
    move: Move,
    maximizer: Mark,
    choose_highest_score: bool = False,
    filename: str = 'precomputed_minimax.json',
) -> int:
    scores = MinimaxSerializer.load(filename)
    if move.after_state.game_over:
        return scores[MinimaxSerializer.key(move)]
    for next_move in move.after_state.possible_moves:
        scores[MinimaxSerializer.key(next_move)][0 if maximizer == 'X' else 1]
    return (max if choose_highest_score else min)(scores)


def find_best_move_precomputed(game_state: GameState) -> Move | None:
    scores = MinimaxSerializer.load()
    maximizer: Mark = game_state.current_mark
    return max(
        game_state.possible_moves,
        key=lambda move: scores[MinimaxSerializer.key(move)][0 if maximizer == 'X' else 1],
    )
