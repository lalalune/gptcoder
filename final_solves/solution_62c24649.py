def solve(input_grid):
    """
    Given a matrix (input_grid), this function transforms it into a new matrix 
    by doubling both its width and height through mirroring.

    The function works in two steps: 

    1. For each row in the input_grid, it appends that row in a reversed order,
       effectively mirroring the row and doubling its length.
       
    2. The derived matrix from the first step is then appended to itself in 
       a reversed order, effectively mirroring the entire matrix vertically 
       and doubling its height.

    Parameters:
    input_grid (List[List[int]]): An initial matrix represented as a list of lists. 
                                  Each sublist represents a row in the matrix.
                                  The elements of the matrix are integers.
                                  
    Returns: 
    output_grid (List[List[int]]): The transformed matrix, that doubles both its
                                   width and height by mirroring the input_matrix.

    This function will correctly transform a matrix for any valid input following the described logic,
    and it is not dependent on a specific amount of rows, columns or the existence of certain values (colors/IDs).
    """
    # Double the width of each row
    new_grid = [row + row[::-1] for row in input_grid]
    
    # Double the height of the matrix
    output_grid = new_grid + new_grid[::-1]

    return output_grid