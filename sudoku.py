import csv

def open_puzzle(csv_file):
    with open(csv_file, 'r') as puzzle:
        grid = puzzle.read()
        puzzle.close()
        return grid

#a function for returning cross products
def cross(A, B):
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits

#creates an array containing all of the squares from A1, B1.. to I9.
squares  = cross(rows, cols)

#computes an array representing all of the units (rows, column and boxes) as arrays of the squares they contain
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

#creates a dictionary that matches each square with its corresponding units in the unit list
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
#creates a dictionary that matches each square with its corresponding peers in the unit list
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in squares) 


def create_grid(grid):
    values = [c for c in grid if c in digits or c == '0']
    assert (len(values) == 81), "Your puzzle contains empty values!"
    #creates a dictionary with squares as keys, containing their corresponding values
    print dict(zip(squares, values)) 
    return dict(zip(squares, values)) 


puzzle = open_puzzle('sudoku.csv')
print puzzle

create_grid(puzzle)
#parse_grid(puzzle)