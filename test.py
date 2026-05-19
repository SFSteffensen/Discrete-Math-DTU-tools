# Run with:  python -m pytest test.py -v
from math import comb, factorial

import pytest
import sympy as sp
from sympy import Poly, expand, symbols

from discrete_tools import (
    bipartite_degree_check,
    check_totient_options,
    classify_function_finite,
    classify_linear_function_descriptor,
    classify_relation,
    coefficient_matches_options,
    coefficient_of_monomial,
    congruences_system_solver,
    count_permutations_subsequence,
    count_permutations_with_constraints,
    derangements_count,
    divide_with_remainder,
    empty_set_option_truths,
    evaluate_set_expression,
    find_equivalent_set_options,
    get_combinations,
    get_derangements,
    get_permutations,
    get_r_combinations,
    get_r_permutations,
    hypercube_edges,
    hypercube_info,
    hypercube_vertices,
    is_antisymmetric,
    is_equivalence_relation,
    is_irreflexive,
    is_partial_order,
    is_prime,
    is_reflexive,
    is_symmetric,
    is_transitive,
    lcm,
    match_answers,
    minimum_selections_for_sum,
    polynomial_extended_gcd,
    polynomial_gcd,
    primes_below,
    recursive_piecewise_value,
    seating_count_two_tables,
    subset_count_size,
    subset_parity_counts_1_to_n,
    tautology_checker,
    totient_prime_product,
)

x, y = symbols("x y")


# Number theory
def test_is_prime_small():
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(7)
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(9)


def test_is_prime_larger():
    assert is_prime(101)
    assert is_prime(103)
    assert not is_prime(100)
    assert not is_prime(102)


def test_primes_below():
    assert primes_below(10) == [2, 3, 5, 7]
    assert primes_below(2) == []
    assert 97 in primes_below(100)
    assert 100 not in primes_below(100)


def test_lcm():
    assert lcm(4, 6) == 12
    assert lcm(3, 5) == 15
    assert lcm(12, 18) == 36
    assert lcm(7, 1) == 7


def test_totient_prime_product():
    assert totient_prime_product(101, 103) == 100 * 102


def test_totient_prime_product_invalid():
    with pytest.raises(ValueError):
        totient_prime_product(4, 6)
    with pytest.raises(ValueError):
        totient_prime_product(5, 3)  # p > q


def test_check_totient_options():
    result = check_totient_options(["p*q - p - q + 1", "p*q - 1", "p*q - p - q - 1"])
    assert result["p*q - p - q + 1"] is True
    assert result["p*q - 1"] is False
    assert result["p*q - p - q - 1"] is False


def test_divide_with_remainder(capsys):
    q, r = divide_with_remainder(17, 5)
    assert q == 3 and r == 2
    q2, r2 = divide_with_remainder(100, 7)
    assert q2 == 14 and r2 == 2


# Chinese Remainder Theorem
def test_crt_exam_q4(capsys):
    # x ≡ 1 (mod 2), x ≡ 1 (mod 5), x ≡ 7 (mod 9)  ->  {61 + 90k}
    x0, m = congruences_system_solver([[1, 2], [1, 5], [7, 9]])
    assert x0 == 61
    assert m == 90


def test_crt_satisfies_all_congruences(capsys):
    system = [[1, 2], [1, 5], [7, 9]]
    x0, _ = congruences_system_solver(system)
    for a, n in system:
        assert x0 % n == a


def test_crt_two_congruences(capsys):
    # x ≡ 3 (mod 5), x ≡ 1 (mod 7)
    x0, m = congruences_system_solver([[3, 5], [1, 7]])
    assert m == 35
    assert x0 % 5 == 3
    assert x0 % 7 == 1


# Polynomial operations
def test_polynomial_gcd_exam_q5():
    p1 = Poly(x**3 - 1, x)
    p2 = Poly(x**3 + 2 * x**2 + 2 * x + 1, x)
    g = polynomial_gcd(p1, p2)
    assert g == Poly(x**2 + x + 1, x, domain="QQ")


def test_polynomial_gcd_coprime():
    p1 = Poly(x + 1, x)
    p2 = Poly(x + 2, x)
    g = polynomial_gcd(p1, p2)
    assert g.degree() == 0  # gcd = monic constant


def test_polynomial_extended_gcd_bezout():
    p1 = Poly(x**3 - 1, x)
    p2 = Poly(x**3 + 2 * x**2 + 2 * x + 1, x)
    g, s, t = polynomial_extended_gcd(p1, p2)
    # s*p1 + t*p2 = gcd
    lhs = sp.expand(s.as_expr() * p1.as_expr() + t.as_expr() * p2.as_expr())
    assert lhs == sp.expand(g.as_expr())
    assert g == Poly(x**2 + x + 1, x, domain="QQ")


# Recursive sequences
def test_recursive_piecewise_exam_q7():
    result = recursive_piecewise_value(
        n=5,
        initial_values={0: 2, 1: 3},
        even_rule=lambda n, a: a(n - 1) + n,
        odd_rule=lambda n, a: a(n - 1) + 2 * a(n - 2),
    )
    assert result == 37


def test_recursive_piecewise_base_cases():
    def even(n, a):
        return a(n - 1) + n

    def odd(n, a):
        return a(n - 1) + 2 * a(n - 2)

    assert recursive_piecewise_value(0, {0: 2, 1: 3}, even, odd) == 2
    assert recursive_piecewise_value(1, {0: 2, 1: 3}, even, odd) == 3


def test_recursive_piecewise_invalid():
    with pytest.raises(ValueError):
        recursive_piecewise_value(
            -1, {0: 1}, lambda n, a: a(n - 1), lambda n, a: a(n - 1)
        )


# Combinatorics -- subsets and parity
def test_subset_count_size():
    assert subset_count_size(5, 2) == 10
    assert subset_count_size(99, 49) == comb(99, 49)


def test_subset_parity_counts_n99():
    # {1, ..., 99}: 49 even numbers, 50 odd numbers
    counts = subset_parity_counts_1_to_n(99)
    assert counts["odd_even_and_even_odd"] == 2**97
    assert counts["odd_odd_and_even_even"] == 2**97
    assert counts["odd_odd"] == 2**98


# Derangements
def test_derangements_count_known_values():
    expected = {0: 1, 1: 0, 2: 1, 3: 2, 4: 9, 5: 44}
    for n, d in expected.items():
        assert derangements_count(n) == d, f"D({n}) expected {d}"


def test_get_derangements_abc():
    d = get_derangements("ABC")
    assert len(d) == 2
    assert set(d) == {"BCA", "CAB"}


def test_get_derangements_no_fixed_points():
    items = "ABCD"
    for perm in get_derangements(items):
        for c, orig in zip(perm, items, strict=True):
            assert c != orig


# Permutations and combinations
def test_get_permutations_count():
    assert len(get_permutations("ABCDE")) == 120


def test_get_r_permutations():
    assert len(get_r_permutations("ABCD", 2)) == 12  # P(4,2)


def test_get_r_combinations():
    assert len(get_r_combinations("ABCD", 2)) == 6  # C(4,2)


def test_get_combinations_all_nonempty():
    # 2^3 - 1 = 7 non-empty subsets of a 3-element set
    assert len(get_combinations("ABC")) == 7


# Permutation constraint counting  (exam Q17)
def test_count_no_adjacent_pairs():
    # None of AB, BC, CD as contiguous substrings
    # I-E: 120 - (24+24+24) + (6+6+6) - 2 = 56 -> 120 - 56 = 64
    count = count_permutations_with_constraints(
        "ABCDE", must_not_contain_any=["AB", "BC", "CD"]
    )
    assert count == 64


def test_count_exactly_one_of():
    # Exactly one of AB, CD: |AB| + |CD| - 2|AB&CD| = 24+24-12 = 36
    count = count_permutations_with_constraints("ABCDE", exactly_one_of=["AB", "CD"])
    assert count == 36


def test_count_must_contain_all():
    # AB as a contiguous block -> 4! = 24
    count = count_permutations_with_constraints("ABCDE", must_contain_all=["AB"])
    assert count == 24


def test_count_subsequence_ace():
    # A, C, E in relative order (non-contiguous): 5!/3! = 20
    count = count_permutations_subsequence("ABCDE", "ACE")
    assert count == 20


# Pigeonhole
def test_minimum_selections_for_sum():
    # Numbers 1-9, target sum 10: pairs (1,9),(2,8),(3,7),(4,6), singleton 5 -> 4+1+1=6
    assert minimum_selections_for_sum(list(range(1, 10)), 10) == 6


def test_minimum_selections_no_pair():
    assert minimum_selections_for_sum([1, 2, 3], 10) is None


# Logic / tautology checker
def test_tautology_contrapositive():
    assert tautology_checker("(p => q) <=> (not q => not p)")["is_tautology"] is True


def test_tautology_implication_as_disjunction():
    assert tautology_checker("(p => q) <=> (not p or q)")["is_tautology"] is True


def test_tautology_demorgan_exam_q14():
    assert (
        tautology_checker("(not p or not q) => (not (p and q))")["is_tautology"] is True
    )


def test_not_tautology_biconditional():
    assert tautology_checker("p <=> q")["is_tautology"] is False


def test_tautology_table_row_count():
    # 2 variables -> 4 rows in truth table
    result = tautology_checker("p or q")
    assert len(result["truth_table"]) == 4


# Set expressions
def test_set_expression_exam_q10():
    U = set(range(8))
    sets = {"A": {0, 1, 2, 4}, "B": {0, 1, 3, 5}, "C": {0, 2, 3, 6}, "U": U}
    expr = (
        "(A inter B) without C union (B inter C) without A union (C inter A) without B"
    )
    assert evaluate_set_expression(expr, sets, U) == {1, 2, 3}


def test_set_expression_demorgan_exam_q12():
    U = set(range(10))
    sets = {"A": {0, 2, 4, 6, 8}, "B": {1, 2, 3, 4, 5}, "C": {3, 4, 5, 6, 7}, "U": U}
    lhs = evaluate_set_expression("A inter ~(B without C)", sets, U)
    rhs = evaluate_set_expression("(A inter ~B) union (A inter C)", sets, U)
    assert lhs == rhs


def test_find_equivalent_set_options():
    U = set(range(10))
    sets = {"A": {0, 2, 4, 6, 8}, "B": {1, 2, 3, 4, 5}, "C": {3, 4, 5, 6, 7}, "U": U}
    options = ["(A inter ~B) union (A inter C)", "A inter ~B inter C"]
    matches = find_equivalent_set_options("A inter ~(B without C)", options, sets, U)
    assert "(A inter ~B) union (A inter C)" in matches
    assert "A inter ~B inter C" not in matches


def test_empty_set_option_truths():
    t = empty_set_option_truths()
    assert t["{∅}"] is True
    assert t["∅"] is False
    assert t["{{∅}}"] is False
    assert t["{x ∈ ℝ : x < x}"] is False


# match_answers helper
def test_match_answers_numeric():
    assert match_answers(6, ["5", "6", "7", "None of these"]) == ["6"]


def test_match_answers_falls_back_to_none_of_these():
    assert match_answers(6, ["5", "None of these"]) == ["None of these"]


# Function classification
def test_classify_function_finite_injective_only():
    r = classify_function_finite(range(0, 10), range(0, 30), lambda n: 2 * n + 7)
    assert r["injective"] is True
    assert r["surjective"] is False
    assert r["classification"] == "Injective but not surjective"


def test_classify_function_finite_bijective():
    r = classify_function_finite(range(5), range(5), lambda n: (n + 1) % 5)
    assert r["injective"] is True
    assert r["surjective"] is True


def test_classify_function_finite_not_well_defined():
    # f: {0..4} -> {0,1,2}, f(x)=x^2  -- f(2)=4 is outside codomain
    r = classify_function_finite(range(5), range(3), lambda n: n**2)
    assert r["well_defined"] is False


def test_classify_linear_function_descriptor_injective():
    r = classify_linear_function_descriptor("f: NN -> NN, f(x) = 2x + 7")
    assert r["injective"] is True
    assert r["surjective"] is False
    assert r["classification"] == "Injective but not surjective"


def test_classify_linear_function_descriptor_invalid():
    with pytest.raises(ValueError):
        classify_linear_function_descriptor("not a valid descriptor")


# Relations
def test_relation_divisibility_is_partial_order():
    S = {1, 2, 3, 4}
    R = {(a, b) for a in S for b in S if b % a == 0}
    assert is_reflexive(S, R)
    assert is_antisymmetric(R)
    assert is_transitive(R)
    assert not is_symmetric(R)
    assert is_partial_order(S, R)
    assert not is_equivalence_relation(S, R)


def test_relation_mod2_is_equivalence():
    S = {1, 2, 3, 4}
    R = {(a, b) for a in S for b in S if (a - b) % 2 == 0}
    assert is_reflexive(S, R)
    assert is_symmetric(R)
    assert is_transitive(R)
    assert is_equivalence_relation(S, R)
    # (1,3) and (3,1) both in R with 1 != 3
    assert not is_antisymmetric(R)


def test_classify_relation_well_order():
    S = {"a", "b", "c", "d"}
    R = {
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
        ("d", "d"),
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("b", "c"),
        ("b", "d"),
        ("c", "d"),
    }
    c = classify_relation(S, R)
    assert "Well order" in c["classification"]


def test_classify_relation_equivalence():
    S = {"a", "b", "c", "d"}
    R = {("a", "a"), ("b", "b"), ("c", "c"), ("d", "d"), ("a", "d"), ("d", "a")}
    c = classify_relation(S, R)
    assert "Equivalence relation" in c["classification"]


def test_is_irreflexive():
    S = {1, 2, 3}
    R = {(1, 2), (2, 3), (1, 3)}
    assert is_irreflexive(S, R)
    assert not is_reflexive(S, R)


# Hypercube / graph theory
def test_hypercube_info_q3():
    info = hypercube_info(3)
    assert info["vertices"] == 8
    assert info["edges"] == 12
    assert info["degree"] == 3
    assert info["bipartite"] is True
    assert info["hamiltonian"] is True
    assert info["edge_count_check"] is True


def test_hypercube_vertex_and_edge_counts():
    for n in range(1, 6):
        assert len(hypercube_vertices(n)) == 2**n
        assert len(hypercube_edges(n)) == n * 2 ** (n - 1)


def test_hypercube_q1():
    info = hypercube_info(1)
    assert info["vertices"] == 2
    assert info["edges"] == 1


# Bipartite degree sequences  (exam Q8)
def test_bipartite_exists_without_multi_edges():
    r = bipartite_degree_check([5, 5, 5, 5], [4, 4, 4, 4, 4])
    assert r["classification"] == "Exists without multiple edges"


def test_bipartite_increase_v1_case1():
    # sum(V1)=7 < sum(V2)=9
    r = bipartite_degree_check([1, 2, 2, 2], [1, 2, 2, 2, 2])
    assert (
        r["classification"] == "Does not exist, but will if we increase a degree in V1"
    )


def test_bipartite_increase_v1_case2():
    # sum(V1)=16 < sum(V2)=25
    r = bipartite_degree_check([4, 4, 4, 4], [5, 5, 5, 5, 5])
    assert (
        r["classification"] == "Does not exist, but will if we increase a degree in V1"
    )


def test_bipartite_increase_v2():
    # sum(V1)=20 > sum(V2)=10
    r = bipartite_degree_check([5, 5, 5, 5], [2, 2, 2, 2, 2])
    assert (
        r["classification"] == "Does not exist, but will if we increase a degree in V2"
    )


# Monomial coefficient extraction  (exam Q20)
def test_coefficient_of_monomial_exam_q20():
    # (2x^3 - y^4)^10: term with x^15*y^20 comes from k=5, giving -C(10,5)*2^5
    poly = expand((2 * x**3 - y**4) ** 10)
    coeff = coefficient_of_monomial(poly, {"x": 15, "y": 20})
    assert coeff == -comb(10, 5) * 2**5  # -8064


def test_coefficient_matches_options():
    poly = expand((2 * x**3 - y**4) ** 10)
    options = ["-binomial(10,5)*2**5", "binomial(10,5)*2**5", "0"]
    matches = coefficient_matches_options(poly, {"x": 15, "y": 20}, options)
    assert "-binomial(10,5)*2**5" in matches
    assert "binomial(10,5)*2**5" not in matches
    assert "0" not in matches


# Circular seating  (exam Q15)
def test_seating_two_tables_with_lr_distinction():
    n = 3
    expected = sp.Rational(factorial(3 * n), 2 * n**2)
    assert seating_count_two_tables(n, distinguish_left_right=True) == expected


def test_seating_two_tables_no_lr_distinction():
    n = 3
    expected = sp.Rational(factorial(3 * n), 8 * n**2)
    assert seating_count_two_tables(n, distinguish_left_right=False) == expected


def test_seating_invalid_n():
    with pytest.raises(ValueError):
        seating_count_two_tables(0)
