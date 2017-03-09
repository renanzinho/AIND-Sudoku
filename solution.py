assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for box in values:                                          #each box
        for peer in peers[box]:                                      #each peer
            if values[peer] == values[box] and len(values[peer])<3:                     #if the box already exist in a peer
                for x in range(0,3):                            #which units is the twin in
                    if peer in units[box][x]:                   #if twin is in the unit
                        for i in units[box][x]:                 #eliminate the twins
                            if i not in (peer,box) and len(i)>1:
                                values[i] = [j for j in values[i] if j not in values[box]]
                                values[i] = "".join(values[i])
    return values




def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [r+c for r in A for c in B]

# Create the grid
r = "ABCDEFGHI"
c = "123456789"
boxes = cross(r,c)

row_units = [cross(rows, c) for rows in r]
column_units = [cross(r, cols) for cols in c]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
diagleft = []
diagright = []
for i in range(0,9):
    diagleft+=[r[i]+c[i]]
    diagright+=[r[i]+c[-i-1]]
for i in diagleft:                  #just add diagonals to peer and the program's going to solve by itself
    peers[i].update([u for u in diagleft if u != i])
for i in diagright:
    peers[i].update([u for u in diagright if u != i])


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    replace = "123456789"
    dic = dict(zip(boxes,grid))

    for i in dic:
        if dic[i] == ".":
            dic[i] = "123456789"

    return dic



def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    ## Copied from the utils
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for row in r:
        print(''.join(values[row+cols].center(width)+('|' if cols in '36' else '')
                      for cols in c))
        if row in 'CF': print(line)
    return

def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    sv = [box for box in boxes if len(values[box])==1]

    for box in sv:
        digit = values[box]
        for p in peers[box]:
            values[p] = values[p].replace(digit,"")

    return values



def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for i in unitlist:
        for d in c:
            docc = [box for box in i if d in values[box]]
            if len(docc)==1:
                values[docc[0]] = d

    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    stuck = False
    while not stuck:
        sv_before = len([box for box in values.keys() if len(values[box])==1])
        values = eliminate(values)
        values = only_choice(values)
        sv_after = len([box for box in values.keys() if len(values[box])==1])
        stuck = sv_after == sv_before

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    #Using depth-first search and propagation, create a search tree and solve the sudoku.
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    values = naked_twins(values)
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    return search(grid)

if __name__ == '__main__':
    display(solve('2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'))




    # display(solve(diag_sudoku_grid))

    # try:
    #     from visualize import visualize_assignments
    #     visualize_assignments(assignments)

    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
