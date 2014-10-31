import csv
from copy import deepcopy as copy

def open_puzzle(csv_file):
    sudoku_reader = csv.reader(open(csv_file, 'r'))
    grid = [int(item) for row in sudoku_reader for item in row if item not in ("", "\n") and int(item) in digits or item == '0']
    return grid

#a function for returning cross products - used for making indices for the squares and for adding indices to the list of units
def cross(A, B):
    if not type(B) is list:
        B = [B]
    if not type(A) is list:
        A = [A]
    return [str(a)+str(b) for a in A for b in B]

digits   = [1,2,3,4,5,6,7,8,9]
rows     = ['A','B','C','D','E','F','G','H','I']
columns  = digits

#creates an array containing key strings for all of the squares from A1, B1.. to I9.
squares  = cross(rows, columns)

#computes an array representing all of the units (rows, column and boxes)
# as arrays of the key strings of the squares they contain
unitlist = ([cross(rows, column) for column in columns] +
            [cross(row, columns) for row in rows] +
            [cross(box_row, box_column) for box_row in (['A','B','C'],['D','E','F'],['G','H','I']) for box_column in ([1,2,3],[4,5,6],[7,8,9])])

#creates a dictionary that matches each square with its corresponding units in the unit list
units = dict((square, [unit for unit in unitlist if square in unit]) for square in squares)
#creates a dictionary that matches each square with its corresponding peers in the unit list
peers = dict((square, (set(sum(units[square],[]))-set([square]))) for square in squares)


def create_grid(grid):
    values = [item for item in grid if item in digits or item == 0]
    #returns a dictionary with squares as keys, and the possible digits for the squares as values
    return dict(zip(squares, values))

def parse_grid(grid):
    values = dict((square, copy(digits)) for square in squares)
    game_grid = create_grid(grid)
    for square, digit in game_grid.items():
        if digit in digits and not assign(values, square, digit):
            # returns false if we fail to assign a valid digit to the particular square
            return False
    # returns values remaining after heuristic processing
    print values
    return values


def assign(values, square, digit):
    # Tries to eliminate all digits but one from the square's possible values,
    # and if possible, remove the last remaining digit from the square's peers.
    # Returns false if a contradiction is discovered (the same digit must be
    # contained in another peer, which is not possible by game rules).
    other_values = copy(values[square])
    try:
        other_values.remove(digit)
    except:
        print "Your puzzle seems to be broken!"
        return False

    if all(eliminate(values, square, next_digit) for next_digit in other_values):
        return values
    else:
        print "Contradiction discovered, failed to assign."
        return False

def eliminate(values, square, digit):
    # eliminates the digit from the square's possible values, and goes on
    # to make changes to the peers if there is less than 2 values remaining
    # or if there are less than 2 possible places for the digit.
    # Returns the heuristically processed values if everything works, or returns
    # false if a contradiction is discovered.
    if digit not in values[square]:
        # the digit was already eliminated earlier
        return values

    values[square].remove(digit)

    # If the square is reduced to one last value, then that value cannot be contained
    # in its peers. Eliminate that value from the peers.
    if len(values[square]) == 0:
        print "Contradiction discovered - removed the last value!"
        return False
    elif len(values[square]) == 1:
        last_digit = values[square][0]
        if not all(eliminate(values, peer_square, last_digit) for peer_square in peers[square]):
            return False
    # If only one possible place for the digit remains inside a unit, it must belong to that square.
    for unit in units[square]:
        digit_places = [unit_square for unit_square in unit if digit in values[unit_square]]
        if len(digit_places) == 0:
            print "Contradiction - I found no place for this value!"
            return False
        elif len(digit_places) == 1:
            if not assign(values, digit_places[0], digit):
                return False
    return values


def run():
    csv_file = raw_input("Please enter then name of the .txt/.csv file containing the sudoku puzzle.\n>> ")
    if csv_file.lower().endswith(('.csv', '.txt')):
        try: 
            puzzle = open_puzzle(csv_file)
            parse_grid(puzzle)
        except IOError, error:
            print error[1]
    else:
        print "You need the puzzle in a .txt or .csv file!"

run()