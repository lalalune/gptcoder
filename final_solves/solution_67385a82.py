def solve(input_grid):
    """
    The function 'solve' transforms the input grid according to the rules observed from the examples provided. 
    In the rules, each cell in the grid with the number 3 that is adjacent (horizontally or vertically) to a 
    cell with the number 3, gets replaced with the number 8. A cell with the number 3 that does not have any 
    adjacent cell with the number 3, remains 3 in the output grid. 
    
    The function works by iterating over each cell in the input grid, checks the cell and its neighbors, and 
    builds the output grid accordingly.

    Parameters:
    input_grid: A 2D list, represents input grid where each element of grid is an integer.

    Returns:
    output_grid: A transformed 2D list based on observed rules from examples. 

    """
    # Initialize the output grid with the same size as the input grid
    output_grid = [[0]*len(input_grid[0]) for _ in range(len(input_grid))]
    
    for i in range(len(input_grid)):
        for j in range(len(input_grid[0])):
            # If the current cell is 3 and it has a neighbor which is also 3,
            if input_grid[i][j] == 3 and (
                (i > 0 and input_grid[i-1][j] == 3) or  # check top neighbor
                (i < len(input_grid)-1 and input_grid[i+1][j] == 3) or  # check bottom neighbor
                (j > 0 and input_grid[i][j-1] == 3) or  # check left neighbor
                (j < len(input_grid[0])-1 and input_grid[i][j+1] == 3)  # check right neighbor
            ):
                output_grid[i][j] = 8
            else:
                output_grid[i][j] = input_grid[i][j]
    
    return output_grid