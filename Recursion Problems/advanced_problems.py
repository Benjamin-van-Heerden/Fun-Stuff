def partition_objects(n, m):
    """
    function that counts the ways to partition n objects using parts up to n
    :param n: number of objects
    :param m: parts for partition
    :return: number of ways
    """
    if n == 0:
        # only one way to partition zero things
        return 1
    elif m == 0 or n < 0:
        # if we are not allowed to use any parts then we cannot construct a partition
        # it is also not sensible to try and partition a negative quantity of things
        return 0
    else:
        # if e.g. we partition 7 objects in 4 parts, at some point we will have to use
        # up all the parts of 3. hence partition_objects(m, n - 1) is a subset of
        # partition_objects(m, n). finally, the remaining partitions all use m itself as a
        # partition -> we subtract it and add the two values together.
        return partition_objects(n - m, m) + partition_objects(n, m - 1)


assert partition_objects(6, 4) == 9
assert partition_objects(5, 5) == 7
assert partition_objects(5, 2) == 3
assert partition_objects(5, 3) == 5
assert partition_objects(9, 5) == 23


def hanoi(m, start, end):
    global count
    if m == 0:
        return
    open_pole = set(["Pole 1", "Pole 2", "Pole 3"]).difference(set([start, end])).pop()

    hanoi(m - 1, start, open_pole)

    print(f"Move disc {m} from {start} to {end}")
    count += 1

    hanoi(m - 1, open_pole, end)


print("####")
count = 0
hanoi(3, "Pole 1", "Pole 3")
print(count)

print("####")
count = 0
hanoi(4, "Pole 1", "Pole 3")
print(count)

print("####")
count = 0
hanoi(5, "Pole 1", "Pole 3")
print(count)





