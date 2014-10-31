import csv
from sys import argv

def open_puzzle(csv_file):
    with open(csv_file, 'r') as puzzle:
        grid = puzzle.read()
        puzzle.close()
        return grid

#a function for returning cross products - useful for making indices for the squares
def cross(A, B):
    return [a+b for a in A for b in B]

digits   = [1,2,3,4,5,6,7,8,9]
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
    values = [item for item in grid if item in digits or item == '0']
    assert (len(values) == 81), "Your puzzle contains empty values!"
    #creates a dictionary with squares as keys, containing their corresponding values
    print dict(zip(squares, values)) 
    return dict(zip(squares, values)) 

def parse_grid(grid):
    # 
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((square, digits) for square in squares)
    for square, digit in create_grid(grid).items():
        if digit in digits and not assign(values, square, digit):
            return False ## (Fail if we can't assign d to square s.)
    print values
    return values


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
        return False ## Contradiction: no place for this value
    elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
        if not assign(values, dplaces[0], d):
            return False
    return values


def run():
    csv_file = raw_input("Please enter then name of the .txt/.csv file containing the sudoku puzzle.\n>>")
    if csv_file.lower().endswith(('.csv', '.txt')):
        try: 
            puzzle = open_puzzle(csv_file)
            print puzzle
            parse_grid(puzzle)
        except IOError, e: 
            print e[1]
    else:
        print "You'll need the puzzle in a .txt or .csv file to run the sudoku solver!"

run()