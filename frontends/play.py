from console.players import ConsolePlayer
from console.renderers import ConsoleRenderer
from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.game.players import RandomComputerPlayer
from tic_tac_toe.logic.models import Mark

player1 = ConsolePlayer(Mark('X'))
player2 = RandomComputerPlayer(Mark('O'))

game = TicTacToe(player1, player2, renderer=ConsoleRenderer())
game.play()
