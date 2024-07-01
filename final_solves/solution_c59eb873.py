import numpy as np

def solve(input_matrix):
    # convert input to numpy array
    a = np.array(input_matrix)
    # repeat the elements in both row and column twice to create the output
    a = np.repeat(a, 2, axis=0)
    a = np.repeat(a, 2, axis=1)
    return a.tolist()