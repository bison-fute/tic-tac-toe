import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-x', help='Specify the x argument')
parser.add_argument('-y', dest='var_y', help='Specify the y argument')

args = parser.parse_args()
print(args.x, args.var_y, sep=' | ')
