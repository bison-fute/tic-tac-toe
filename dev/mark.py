from tic_tac_toe.logic.models import Mark

for mark in Mark:
    print(mark.value, type(mark.value), mark, sep=' | ')
