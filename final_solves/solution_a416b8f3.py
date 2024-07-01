import numpy as np

def solve(matrix):
    matrix_np = np.array(matrix)
    result = np.hstack((matrix_np, matrix_np))
    return result.tolist()