import csv
from copy import deepcopy as copy
import string

def open_puzzle(csv_file):
    with open(csv_file, 'r') as sudoku_csv:
        grid = []
        puzzle_rendering = []
        for row in sudoku_csv:
            row = row.strip()
            if row:
                puzzle_rendering.append([row.replace(",", " ")])
            for item in row:
                if item in string.digits:
                    grid.append(item)

        print "The puzzle you opened looks like this:"
        draw(puzzle_rendering)
        return grid

# Function for returning cross products - used for making indices for the 
# squares and for adding indices to the list of units
def cross(A, B):
    return ["%s%s" % (a, b) for a in A for b in B]

digits = [1,2,3,4,5,6,7,8,9]
rows = ['A','B','C','D','E','F','G','H','I']
columns = digits

# creates an array containing key strings for all of the squares from A1, B1.. to I9.
squares = cross(rows, columns)

# computes an array representing all of the units (rows, column and boxes)
# as arrays of the key strings of the squares they contain
unitlist = ([cross(rows, [column]) for column in columns] +
            [cross([row], columns) for row in rows] +
            [cross(box_row, [box_column]) for box_row in (['A','B','C'],['D','E','F'],['G','H','I']) 
            for box_column in ([1,2,3],[4,5,6],[7,8,9])])

# creates a dictionary that matches each square with its corresponding units in the unit list
units = dict((square, [unit for unit in unitlist if square in unit]) for square in squares)
# creates a dictionary that matches each square with its corresponding peers in the unit list
peers = dict((square, (set(sum(units[square],[]))-set([square]))) for square in squares)

def create_grid(grid):
    values = [int(value) for value in grid if value in string.digits]
    # returns a dictionary with squares as keys, and the possible digits for the squares as values
    return dict(zip(squares, values))

def parse_grid(grid):
    values = dict((square, copy(digits)) for square in squares)
    game_grid = create_grid(grid)
    for square, digit in game_grid.items():
        if digit != 0 and not assign(values, square, digit):
            # returns false if we fail to assign a valid digit to the particular square
            return False
    # returns values remaining after heuristic processing
    return values


def assign(values, square, digit):
    '''Tries to eliminate all digits but one from the square's possible values,
    and removes the last remaining digit from the square's peers.
    Returns false if a contradiction is discovered (the same digit is
    contained in a peer, which is not possible by game rules).'''
    iterate_values = copy(values[square])
    try:
        iterate_values.remove(digit)
    except:
        print "Your puzzle seems to be broken!"
        return False

    if all(eliminate(values, square, next_digit) for next_digit in iterate_values):
        return values
    else:
        return False

def eliminate(values, square, digit):
    ''' eliminates the digit from the square's possible values, and goes on
    to make changes to the peers if there is less than 2 values remaining
    or if there are less than 2 possible places for the digit.
    Returns the heuristically processed values if everything works, or returns
    false if a contradiction is discovered.'''
    if digit not in values[square]:
        # The digit was already eliminated earlier
        return values
    values[square].remove(digit)
    # If no digits remain in the square - contradiction
    if not values[square]:
        return False
    # If the square is reduced to one last value, then that value cannot be contained in its peers.
    # Eliminate that value from the peers.
    elif len(values[square]) == 1:
        last_digit = values[square][0]
        if not all(eliminate(values, peer_square, last_digit) for peer_square in peers[square]):
            return False
    # Calls the naked twins strategy if two digits remain
    elif len(values[square]) == 2:
        naked_twins(square, values)
    # If only one possible place for the digit remains inside a unit, it must belong to that square.
    for unit in units[square]:
        digit_places = [unit_square for unit_square in unit if digit in values[unit_square]]
        # if no possible places remain for the digit - contradiction
        if not digit_places:
            return False
        elif len(digit_places) == 1:
            if not assign(values, digit_places[0], digit):
                return False
    return values

def naked_twins(square, values):
    '''A function with the naked twins strategy: If two squares within the same unit contain only
    the same two digits, both digits can be eliminated from all the other squares in that unit.'''
    for unit in units[square]:
        # Searches for peers from the same unit
        for peer in set(unit).intersection(set(peers[square])):
            # If an item in the unit contains the same values as the square (but is not the square itself),
            # a naked pair is identified and those values are removed from all other items in the unit.
            if not set(values[peer]).difference(set(values[square])):
                digit1 = values[square][0]
                digit2 = values[square][1]
                for item in set(unit).difference(set([square, peer])):
                    # If the item is not in the naked twins pair, remove the naked twins' values
                    if digit1 in values[item]:
                        values[item].remove(digit1)
                    if digit2 in values[item]:
                        values[item].remove(digit2)

def search(values):
    '''Uses recursive search, naked twins and constraint propagation
    to try all possible values one square at the time.'''
    if values is False:
        return False
    if all(len(values[square]) == 1 for square in squares):
        return values
    # If puzzle is not solved or a contradiction has not been discovered, search
    # through the square with the fewest possible remaining values
    length, square = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    finish = solution(search(assign(copy(values), square, digit)) for digit in values[square])
    return finish

def solution(sequence):
    # Checks for a working layout for the puzzle if such exists
    for solution in sequence:
        if solution: return solution
    return False

def render(values):
    output_filename = (filename.split('.')[0]) + "_solution.csv"
    output_file = open(output_filename, 'wb')
    solution_writer = csv.writer (output_file)

    split_array = lambda array, n=9: [array[i:i+n] for i in range(0, len(array), n)]
    results_array = split_array([values[item][0] for item in squares])

    for row in results_array:
        solution_writer.writerow(row)

    print "This is your solution. It has been stored in a file called %s" % output_filename
    
    draw(results_array)
    output_file.close()

def draw(sudoku_grid):
    for row in sudoku_grid:
        print "|",
        for item in row:
            print item,
        print "|"

def run(csv_file):
    if csv_file.lower().endswith(('.csv', '.txt')):
        try: 
            puzzle = open_puzzle(csv_file)
            render(search(parse_grid(puzzle)))
        except IOError, error:
            print error[1]
    else:
        print "You need the puzzle in a .txt or .csv file!"

filename = raw_input("Please enter then name of the .txt/.csv file containing the sudoku puzzle.\n>> ")

if __name__ == "__main__":
    run(filename)