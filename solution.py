assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # this first technique go through every unit searching for boxes with two
    # possible values and then look if it has a twin
    # I believe this technique is less efficiente than the second one

    # for unit in unitlist:
    #     for box in unit:
    #         # find box with 2 possible values
    #         if len(values[box]) == 2:
    #             # search the unit for a twin box
    #             twins_boxes = [twin for twin in unit if values[box] == values[twin]]
    #             if len(twins_boxes) == 2:
    #                 # case twins were found, remove twins' values from other boxes in the unit
    #                 for square in unit:
    #                     if square not in twins_boxes:
    #                         # remove twins values step
    #                         for digit in values[twins_boxes[0]]:
    #                             assign_value(values, square, values[square].replace(digit, ''))

    # This second technique looks in the intire board for boxes with only 2 possible values
    # then it goes directly to the units those boxes belongs and search for twins

    # get all boxes with 2 possible values
    boxes_2 = [box for box in values if len(values[box]) == 2]
    for box in boxes_2:
        # go through units that each box belongs to
        for unit in units[box]:
            # look for twins in the unit
            twins = [s for s in unit if values[s] == values[box]]
            if len(twins) == 2:
                # case twins were found, remove twins' values from other boxes in the unit
                for square in unit:
                    if square not in twins:
                        for digit in values[box]:
                            values = assign_value(values, square, values[square].replace(digit, ''))
    return values


rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#add the principal diagonals as units in the board
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],
    ['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    reduced_sudoku = reduce_puzzle(values)
    if reduced_sudoku == False:
        return False
    if all(len(reduced_sudoku[s]) == 1 for s in reduced_sudoku):
        return reduced_sudoku
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_values = [box for box in reduced_sudoku if len(reduced_sudoku[box]) > 1]
    best_box = unsolved_values[0]
    for box in unsolved_values:
        if len(reduced_sudoku[box]) < len(reduced_sudoku[best_box]):
            best_box = box
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in reduced_sudoku[best_box]:
        new_sudoku = reduced_sudoku.copy()
        new_sudoku = assign_value(new_sudoku, best_box, digit)
        resolved_sudoku = search(new_sudoku)
        if resolved_sudoku:
            return resolved_sudoku

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
