# Task 9.1 - Task 1
# Write your own version of zip function using generator function (with yield operator).
# We expect it to have 2 parameters with iterables and it must produce corresponding pairs.
# This code should work with it:
# it1 = [1,2,3]
# it2 = (x**2 for x in it1)
# for row in my_zip(it1, it2):
#     print(row)

from collections.abc import Iterator

# inputs to this function are either iterables or iterators
def my_zip(it1, it2):
    length = len(it1)
    if not isinstance(it1, Iterator):
        iter1 = iter(it1)
    else:
        iter1 = it1
    if not isinstance(it2, Iterator):
        iter2 = iter(it2)
    else:
        iter2 = it2
    for i in range(length):
        yield (next(iter1), next(iter2))


it1 = [1, 2, 3]
it2 = (x ** 2 for x in it1)

it3 = (1, 2, 3, 4)
it4 = (x ** 2 for x in it3)

for row in my_zip(it1, it2):
    print(row)

for row in my_zip(it3, it4):
    print(row)

# Task 9.1 - task 2
# Write merge function. It will receive two iterables and produce one with alternating elements:
# item 1 from iterable 1
# item 1 from iterable 2
# item 2 from iterable 1
# item 2 from iterable 2
#
# It should stop when any of two iterables is finished.
# Implementation should be based on next and yield calls.

def alternate(it1, it2):
    length1 = len(it1)
    length2 = len(it2)
    if length1 <= length2:
        length = length1
    else:
        length = length2
    iter1 = iter(it1)
    iter2 = iter(it2)
    for i in range(length * 2):
        if i % 2 == 0:
            yield next(iter1)
        else:
            yield next(iter2)


it1 = [x for x in range(20)]
it2 = [x for x in range(10)]

for item in alternate(it1, it2):
    print(item)
