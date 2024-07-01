def solve(matrix):
    """
    The function receives a 2D list (matrix) as input and returns another 2D list as output.
    
    The function solves the problem by reflecting the input matrix along its 
    horizontal axis and appending it to the original matrix. Reflecting a 
    matrix along its horizontal axis results in swapping the rows from top 
    to bottom.
    
    Here's how it works:
    1. The function first reflects the input matrix along its horizontal axis. 
    This is done by simply reversing the list of lists, i.e., matrix[::-1]. 
    The result of this operation is a new matrix that is a mirror image of 
    the input matrix.
    2. Then it appends the mirrored matrix to the original matrix:

    Args:
    - matrix: A 2D list of integers. It's guaranteed that this matrix is 
    a square matrix.

    Returns:
    - A 2D list of integers. The returned matrix is always a perfect rectangle.
    """
    reflected_matrix = matrix[::-1]
    return matrix + reflected_matrix