def unique_paths(n, m):
    """
    function that takes two inputs n and m and outputs the number of unique paths from the top left
    corner to the bottom right corner of a m x n grid. the constraint is that you can only move down or right
    one unit at a time
    :param n: vertical dimension (integer)
    :param m: horizontal dimension (integer)
    :return: number of unique paths
    """
    if m == 1 or n == 1:
        # only one path if it is just a row or column
        return 1
    # otherwise there are two ways to get to the final position -> go down one square or go right one square
    return unique_paths(n - 1, m) + unique_paths(n, m - 1)


assert unique_paths(1, 10) == 1
assert unique_paths(4, 14) == 560
assert unique_paths(10, 10) == 48620
