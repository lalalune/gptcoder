def solve(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[0 for i in range(m)] for j in range(n)]
    for i in range(n-1):
        result[i+1] = matrix[i]
    return result