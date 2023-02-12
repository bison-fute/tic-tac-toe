import re

s = 'XOO XO OO '

match = re.finditer(pattern='O', string=s)
if match is not None:
    print(type(match))
