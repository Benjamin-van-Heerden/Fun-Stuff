def sum_non_negative(n, accumulator=0):
    """
    tail recursive function for summing all the non negative integers up to n
    
    :param n: integer
    :param accumulator: store of the sum, making the function tail recursive
    :return: sum of all the numbers up to n
    """
    if n == 1:
        return accumulator + 1
    else:
        return sum_non_negative(n - 1, accumulator + n)


assert sum_non_negative(4) == 10
assert sum_non_negative(10) == 55
