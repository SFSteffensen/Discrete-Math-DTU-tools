from discrete_tools import *
from sympy import Poly, symbols

# should print: {61 + 90k | k ∈ ℤ}
print(congruences_system_solver([[1, 2], [1, 5], [7, 9]]))

# "For all $n in NN$ define $a_m$ recursively as follows: $a_0 = 2$, $a_1 = 3$, $a_n = cases(a_(n-1) + n, quad "if n is even", a_(n-1) + 2a_(n-2), quad "if n is odd")$ what is $a_5$?" 
a0 = 2
a1 = 3
# example:
def a(n):
    if n == 0:
        return a0
    elif n == 1:
        return a1
    elif n % 2 == 0:  # n is even
        return a(n-1) + n
    else:  # n is odd
        return a(n-1) + 2*a(n-2)

print(a(5))  # This will compute a_5, should be 37.

