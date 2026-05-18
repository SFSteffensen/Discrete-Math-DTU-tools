import re
from itertools import permutations, product, chain, combinations
import math
import numpy as np
from sympy import mod_inverse

# Private helper: silent extended Euclidean algorithm.
# Returns (gcd, s, t) such that gcd = s*a + t*b.
def _min_gcd_congruences(a, b):
    rlist = [a, b]
    qlist = []
    while True:
        r1 = rlist[-2]
        r2 = rlist[-1]
        if r2 == 0:
            break
        new_r = r1 % r2
        qlist.append(r1 // r2)
        rlist.append(new_r)
    slist = [1, 0]
    tlist = [0, 1]
    for q in qlist:
        slist.append(slist[-2] - q * slist[-1])
        tlist.append(tlist[-2] - q * tlist[-1])
    return rlist[-2], slist[-2], tlist[-2]


# Solves a system of congruences x ≡ a_i (mod n_i) using CRT.
# Input: list of [a, n] pairs, e.g. [[1, 2], [1, 5], [7, 9]]
# Requires pairwise coprime moduli.
def congruences_system_solver(system):
    m = 1
    for cong in system:
        m *= cong[1]
    M_list = []
    for cong in system:
        M_list.append(m // cong[1])
    y_list = []
    for i in range(len(M_list)):
        r, s, t = _min_gcd_congruences(M_list[i], system[i][1])
        y_list.append(s)
    x = 0
    for i in range(len(M_list)):
        x += system[i][0] * M_list[i] * y_list[i]
    x = x % m
    print(f'{{{x} + {m}k | k ∈ ℤ}}')
    return x, m