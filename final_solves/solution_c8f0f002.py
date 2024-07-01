def solve(matrix):
    # Create output matrix by copying input
    output = matrix.copy()
    
    # For each cell in output matrix, replace '7' with '5'
    for i in range(len(output)):
        for j in range(len(output[0])):
            if output[i][j] == 7:
                output[i][j] = 5
                
    return output