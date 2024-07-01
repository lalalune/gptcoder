def solve(input_matrix):
    output_matrix = input_matrix.copy()
    
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[0])):
            if i == 0 or i == len(input_matrix) - 1 or j == 0 or j == len(input_matrix[0]) - 1:
                output_matrix[i][j] = 8
    
    return output_matrix