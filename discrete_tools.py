import math
import re
from collections.abc import Callable, Iterable, Sequence
from functools import cache, reduce
from itertools import combinations, permutations, product
from math import factorial

import sympy as sp
from sympy import Poly, symbols
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


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
    print(f"{{{x} + {m}k | k ∈ ℤ}}")
    return x, m


def polynomial_gcd(poly1, poly2, show_steps=False):
    p1 = Poly(poly1)
    p2 = Poly(poly2, *p1.gens)
    g = sp.gcd(p1, p2).monic()
    if show_steps:
        print(f"gcd({p1.as_expr()}, {p2.as_expr()}) = {g.as_expr()}")
    return g


def polynomial_extended_gcd(poly1, poly2, show_steps=False):
    p1 = Poly(poly1)
    p2 = Poly(poly2, *p1.gens)
    s, t, g = sp.gcdex(p1, p2)
    s, t, g = Poly(s, *p1.gens), Poly(t, *p1.gens), Poly(g, *p1.gens)
    lc = g.LC()
    if lc != 1:
        g = g.monic()
        s = Poly(s.as_expr() / lc, *p1.gens)
        t = Poly(t.as_expr() / lc, *p1.gens)
    if show_steps:
        print(f"gcd = {g.as_expr()}")
        print(
            f"Bezout: ({s.as_expr()})*({p1.as_expr()}) + ({t.as_expr()})*({p2.as_expr()})"
        )
    return g, s, t


def recursive_piecewise_value(
    n: int,
    initial_values: dict[int, int],
    even_rule: Callable[[int, Callable[[int], int]], int],
    odd_rule: Callable[[int, Callable[[int], int]], int],
):
    if n < 0:
        raise ValueError("n must be non-negative.")
    missing_base = [
        k
        for k in range(min(initial_values), max(initial_values) + 1)
        if k not in initial_values
    ]
    if missing_base:
        raise ValueError(f"Base values are not contiguous. Missing: {missing_base}")

    @cache
    def a(k: int) -> int:
        if k in initial_values:
            return initial_values[k]
        if k % 2 == 0:
            return even_rule(k, a)
        return odd_rule(k, a)

    return a(n)


def subset_count_size(n: int, k: int) -> int:
    return math.comb(n, k)


def subset_parity_counts_1_to_n(n: int) -> dict[str, int]:
    evens = n // 2
    odds = n - evens

    odd_even_and_even_odd = (
        0 if evens == 0 or odds == 0 else (2 ** (evens - 1)) * (2 ** (odds - 1))
    )
    odd_odd_and_even_even = (
        0 if odds == 0 or evens == 0 else (2 ** (odds - 1)) * (2 ** (evens - 1))
    )
    odd_odd = 0 if odds == 0 else (2**evens) * (2 ** (odds - 1))

    return {
        "odd_even_and_even_odd": odd_even_and_even_odd,
        "odd_odd_and_even_even": odd_odd_and_even_even,
        "odd_odd": odd_odd,
    }


def circular_arrangements(n: int, labeled: bool = False, directed: bool = True) -> int:
    """
    Count distinct circular seating arrangements for n people at ONE table.

    Args:
        n:        number of people
        labeled:  True if seats are distinguishable (fixed/numbered chairs)
                  False if only relative order matters (floating table)
        directed: True  if left/right neighbors are distinct (CW != CCW)
                  False if mirror images are the same arrangement

    Formulas:
        labeled=True,  directed=True  → n!
        labeled=True,  directed=False → n! / 2
        labeled=False, directed=True  → (n-1)!
        labeled=False, directed=False → (n-1)! / 2
    """
    base = factorial(n) if labeled else factorial(n - 1)
    return base // 2 if not directed else base


def circular_arrangements_multi_table(
    n: int,
    tables: list[int],
    labeled: bool = False,
    directed: bool = True,
) -> int:
    """
    Count distinct ways to seat n people across multiple circular tables.

    Steps:
        1. Partition n people into groups of sizes given by `tables`
           using the multinomial coefficient: n! / (t1! * t2! * ... * tk!)
        2. Arrange each group circularly: multiply circular_arrangements(ti, ...)

    Args:
        n:        total number of people
        tables:   list of table sizes, e.g. [6, 6, 8] for three tables
                  (must sum to n)
        labeled:  passed to circular_arrangements (seat labels)
        directed: passed to circular_arrangements (L/R distinction)

    Returns:
        Total number of distinct seating arrangements.

    Examples:
        # 20 people, two tables of 10 (standard circular, directed)
        >>> circular_arrangements_multi_table(20, [10, 10])
        # = C(20,10) * 9! * 9!

        # 20 people, four tables of 5
        >>> circular_arrangements_multi_table(20, [5, 5, 5, 5])
        # = 20! / (5!^4) * (4!)^4
    """
    if sum(tables) != n:
        raise ValueError(f"Table sizes {tables} sum to {sum(tables)}, expected {n}.")

    # Step 1: multinomial — ways to partition n people into the groups
    multinomial = factorial(n)
    for t in tables:
        multinomial //= factorial(t)

    # Step 2: circular arrangements within each table
    circular = reduce(
        lambda acc, t: acc * circular_arrangements(t, labeled, directed),
        tables,
        1,
    )

    return multinomial * circular


def circular_arrangements_table(n: int) -> dict:
    """All four single-table arrangement counts for n people."""
    return {
        "labeled_directed": circular_arrangements(n, labeled=True, directed=True),
        "labeled_undirected": circular_arrangements(n, labeled=True, directed=False),
        "unlabeled_directed": circular_arrangements(n, labeled=False, directed=True),
        "unlabeled_undirected": circular_arrangements(n, labeled=False, directed=False),
    }


def circular_arrangements_multi_table_table(n: int, tables: list[int]) -> dict:
    """All four arrangement counts for n people across multiple tables."""
    return {
        "labeled_directed": circular_arrangements_multi_table(
            n, tables, labeled=True, directed=True
        ),
        "labeled_undirected": circular_arrangements_multi_table(
            n, tables, labeled=True, directed=False
        ),
        "unlabeled_directed": circular_arrangements_multi_table(
            n, tables, labeled=False, directed=True
        ),
        "unlabeled_undirected": circular_arrangements_multi_table(
            n, tables, labeled=False, directed=False
        ),
    }


def match_answers(correct_value, options: Sequence[str]) -> list[str]:
    p, q = symbols("p q")
    matched = []
    for option in options:
        if option.strip().lower() == "none of these":
            continue
        try:
            if sp.simplify(sp.sympify(option) - correct_value) == 0:
                matched.append(option)
        except Exception:
            continue
    if not matched and any(opt.strip().lower() == "none of these" for opt in options):
        return ["None of these"]
    return matched


def classify_function_finite(
    domain: Iterable, codomain: Iterable, func: Callable
) -> dict[str, object]:
    domain = list(domain)
    codomain = list(codomain)

    images = {}
    for x in domain:
        y = func(x)
        images[x] = y
        if y not in codomain:
            return {
                "well_defined": False,
                "injective": None,
                "surjective": None,
                "classification": "not well defined",
                "counterexample": (x, y),
            }

    values = list(images.values())
    injective = len(set(values)) == len(values)
    surjective = set(values) == set(codomain)

    if injective and surjective:
        cls = "Both surjective and injective"
    elif injective:
        cls = "Injective but not surjective"
    elif surjective:
        cls = "Surjective but not injective"
    else:
        cls = "Well defined but neither surjective nor injective"

    return {
        "well_defined": True,
        "injective": injective,
        "surjective": surjective,
        "classification": cls,
        "mapping": images,
    }


def _normalize_number_set_name(name: str) -> str:
    name = (
        name.strip()
        .replace("ℕ", "N")
        .replace("ℤ", "Z")
        .replace("ℚ", "Q")
        .replace("ℝ", "R")
    )
    name = name.upper()
    aliases = {"NN": "N", "ZZ": "Z", "QQ": "Q", "RR": "R"}
    return aliases.get(name, name)


def classify_linear_function_descriptor(descriptor: str) -> dict[str, object]:
    pattern = re.compile(
        r"f\s*:\s*([A-Za-zℕℤℚℝ]+)\s*[-–>]+\s*([A-Za-zℕℤℚℝ]+).*?f\s*\(\s*x\s*\)\s*=\s*(.+)$",
        re.IGNORECASE,
    )
    m = pattern.search(descriptor.strip())
    if not m:
        raise ValueError(
            "Could not parse descriptor. Use format like: f: NN -> NN, f(x)=2x+7"
        )

    domain = _normalize_number_set_name(m.group(1))
    codomain = _normalize_number_set_name(m.group(2))
    expr_str = m.group(3).replace("^", "**")
    x = symbols("x")
    transformations = standard_transformations + (implicit_multiplication_application,)
    expr = parse_expr(expr_str, local_dict={"x": x}, transformations=transformations)
    linear = sp.Poly(sp.expand(expr), x)
    if linear.degree() > 1:
        raise ValueError(
            "This helper currently supports linear functions only: f(x)=ax+b"
        )

    a = sp.simplify(linear.coeffs()[0] if linear.degree() == 1 else 0)
    b = sp.simplify(linear.nth(0))
    a_int = bool(a.is_integer)
    b_int = bool(b.is_integer)

    well_defined = True
    if domain == "N" and codomain == "N":
        well_defined = a_int and b_int and a >= 0 and b >= 0
    elif domain == "N" and codomain in ("Z",) or domain == "Z" and codomain in ("Z",):
        well_defined = a_int and b_int
    elif domain == "Z" and codomain == "N":
        well_defined = a == 0 and b_int and b >= 0
    elif domain == "R" and codomain == "Z":
        well_defined = a == 0 and b_int
    elif domain == "R" and codomain == "Q":
        well_defined = a == 0 and b.is_rational
    elif domain in ("R", "Q") and codomain in ("R", "Q"):
        well_defined = True

    if not well_defined:
        return {
            "well_defined": False,
            "injective": None,
            "surjective": None,
            "classification": "not well defined",
            "domain": domain,
            "codomain": codomain,
            "expression": sp.expand(expr),
        }

    injective = bool(a != 0)
    if domain == "N" and codomain == "N":
        surjective = bool(a == 1 and b == 0)
    elif domain == "Z" and codomain == "Z":
        surjective = bool(abs(a) == 1)
    elif domain == "R" and codomain == "R" or domain == "Q" and codomain == "Q":
        surjective = bool(a != 0)
    else:
        surjective = False

    if injective and surjective:
        cls = "Both surjective and injective"
    elif injective:
        cls = "Injective but not surjective"
    elif surjective:
        cls = "Surjective but not injective"
    else:
        cls = "Well defined but neither surjective nor injective"

    return {
        "well_defined": True,
        "injective": injective,
        "surjective": surjective,
        "classification": cls,
        "domain": domain,
        "codomain": codomain,
        "expression": sp.expand(expr),
    }


class _LogicParser:
    _token_pattern = re.compile(
        r"\s*(<=>|↔|=>|->|→|\(|\)|¬|!|not\b|and\b|or\b|∧|∨|[A-Za-z_][A-Za-z0-9_]*)"
    )

    def __init__(self, expression: str):
        self.tokens = self._tokenize(expression)
        self.pos = 0

    def _tokenize(self, expression: str):
        tokens = []
        i = 0
        while i < len(expression):
            m = self._token_pattern.match(expression, i)
            if not m:
                raise ValueError(f"Invalid token near: {expression[i : i + 15]}")
            token = m.group(1)
            if token and not token.isspace():
                tokens.append(token)
            i = m.end()
        return tokens

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _eat(self, token=None):
        cur = self._peek()
        if cur is None:
            return None
        if token is not None and cur != token:
            raise ValueError(f"Expected {token}, got {cur}")
        self.pos += 1
        return cur

    def parse(self):
        node = self._parse_equiv()
        if self._peek() is not None:
            raise ValueError(f"Unexpected token: {self._peek()}")
        return node

    def _parse_equiv(self):
        node = self._parse_impl()
        while self._peek() in ("<=>", "↔"):
            op = self._eat()
            rhs = self._parse_impl()
            node = (op, node, rhs)
        return node

    def _parse_impl(self):
        node = self._parse_or()
        if self._peek() in ("=>", "->", "→"):
            op = self._eat()
            rhs = self._parse_impl()
            return (op, node, rhs)
        return node

    def _parse_or(self):
        node = self._parse_and()
        while self._peek() in ("or", "∨"):
            op = self._eat()
            rhs = self._parse_and()
            node = (op, node, rhs)
        return node

    def _parse_and(self):
        node = self._parse_not()
        while self._peek() in ("and", "∧"):
            op = self._eat()
            rhs = self._parse_not()
            node = (op, node, rhs)
        return node

    def _parse_not(self):
        if self._peek() in ("not", "¬", "!"):
            op = self._eat()
            return (op, self._parse_not())
        return self._parse_primary()

    def _parse_primary(self):
        token = self._peek()
        if token == "(":
            self._eat("(")
            node = self._parse_equiv()
            self._eat(")")
            return node
        if token is None:
            raise ValueError("Unexpected end of expression.")
        if re.match(r"[A-Za-z_][A-Za-z0-9_]*$", token):
            self._eat()
            return ("var", token)
        raise ValueError(f"Unexpected token: {token}")


def _logic_variables(ast_node) -> set[str]:
    if ast_node[0] == "var":
        return {ast_node[1]}
    if ast_node[0] in ("not", "¬", "!"):
        return _logic_variables(ast_node[1])
    if len(ast_node) == 3:
        return _logic_variables(ast_node[1]) | _logic_variables(ast_node[2])
    return set()


def _logic_eval(ast_node, valuation: dict[str, bool]) -> bool:
    op = ast_node[0]
    if op == "var":
        return valuation[ast_node[1]]
    if op in ("not", "¬", "!"):
        return not _logic_eval(ast_node[1], valuation)
    if op in ("and", "∧"):
        return _logic_eval(ast_node[1], valuation) and _logic_eval(
            ast_node[2], valuation
        )
    if op in ("or", "∨"):
        return _logic_eval(ast_node[1], valuation) or _logic_eval(
            ast_node[2], valuation
        )
    if op in ("=>", "->", "→"):
        return (not _logic_eval(ast_node[1], valuation)) or _logic_eval(
            ast_node[2], valuation
        )
    if op in ("<=>", "↔"):
        return _logic_eval(ast_node[1], valuation) == _logic_eval(
            ast_node[2], valuation
        )
    raise ValueError(f"Unknown operator: {op}")


def tautology_checker(expression: str) -> dict[str, object]:
    parser = _LogicParser(expression)
    ast = parser.parse()
    vars_sorted = sorted(_logic_variables(ast))

    table = []
    all_true = True
    for values in product([False, True], repeat=len(vars_sorted)):
        valuation = dict(zip(vars_sorted, values, strict=True))
        result = _logic_eval(ast, valuation)
        table.append({"valuation": valuation, "result": result})
        if not result:
            all_true = False

    return {
        "variables": vars_sorted,
        "is_tautology": all_true,
        "truth_table": table,
    }


def get_permutations(items: str | Sequence[str]) -> list[str]:
    return ["".join(p) for p in permutations(items)]


# ---------------------------------------------------------------------------
# Derangements
# ---------------------------------------------------------------------------


def derangements_count(n: int) -> int:
    """D(n): number of derangements of n elements. D(n) = n! * Σ (-1)^k/k! for k=0..n"""
    return round(
        math.factorial(n) * sum((-1) ** k / math.factorial(k) for k in range(n + 1))
    )


def get_derangements(items: str | Sequence[str]) -> list[str]:
    """All permutations of items where no element stays in its original position."""
    items = list(items)
    return [
        "".join(p)
        for p in permutations(items)
        if all(p[i] != items[i] for i in range(len(items)))
    ]


# ---------------------------------------------------------------------------
# N-cubes (hypercube graphs Q_n)
# ---------------------------------------------------------------------------


def hypercube_vertices(n: int) -> list[str]:
    """Vertices of Q_n: all binary strings of length n."""
    return ["".join(str(b) for b in bits) for bits in product([0, 1], repeat=n)]


def hypercube_edges(n: int) -> list[tuple[str, str]]:
    """Edges of Q_n: pairs of binary strings differing in exactly one bit."""
    verts = hypercube_vertices(n)
    return [
        (u, v)
        for i, u in enumerate(verts)
        for v in verts[i + 1 :]
        if sum(a != b for a, b in zip(u, v, strict=True)) == 1
    ]


def hypercube_info(n: int) -> dict[str, object]:
    """Stats about Q_n: vertex count, edge count, degree, Hamilton cycle existence."""
    verts = hypercube_vertices(n)
    edges = hypercube_edges(n)
    return {
        "n": n,
        "vertices": 2**n,
        "edges": n * 2 ** (n - 1),
        "degree": n,  # every vertex has degree n (n-regular)
        "bipartite": True,  # Q_n is always bipartite
        "hamiltonian": n >= 1,  # Q_n has a Hamilton cycle for n >= 1 (Gray code)
        "vertex_list": verts,
        "edge_count_check": len(edges) == n * 2 ** (n - 1),
    }


def divide_with_remainder(a: int, b: int) -> tuple[int, int]:
    """Returns (quotient, remainder) for a ÷ b and prints a human-readable line."""
    q, r = divmod(a, b)
    print(f"{a} = {q}·{b} + {r}   (remainder {r})")
    return q, r


def get_r_permutations(items: str | Sequence[str], r: int) -> list[str]:
    """All r-permutations of items (order matters, no repetition)."""
    return ["".join(p) for p in permutations(items, r)]


def get_combinations(items: str | Sequence[str]) -> list[str]:
    """All non-empty subsets of items (all sizes, order does not matter)."""
    result = []
    for r in range(1, len(items) + 1):
        result.extend("".join(c) for c in combinations(items, r))
    return result


def get_r_combinations(items: str | Sequence[str], r: int) -> list[str]:
    """All r-combinations of items (order does not matter)."""
    return ["".join(c) for c in combinations(items, r)]


def minimum_selections_for_sum(numbers: Sequence[int], target_sum: int) -> int | None:
    """
     Minimum items to draw (worst case) to guarantee a pair summing to target_sum.
    Returns None if no such pair exists in numbers.
    Pigeonhole: worst case = draw all singletons + 1 from each pair + 1 more.
    """
    num_set = set(numbers)
    can_pair = {
        a for a in numbers if (target_sum - a) in num_set and a != target_sum - a
    }
    if not can_pair:
        return None
    num_pairs = len(can_pair) // 2
    safe = [x for x in numbers if x not in can_pair]
    return len(safe) + num_pairs + 1


def pigeonhole_min(k, guarantee_per_box):
    """Minimum objects needed so some box has >= guarantee_per_box objects."""
    return k * (guarantee_per_box - 1) + 1


def halls_min_degree(n_left: int, n_right: int, required_matching: int) -> int:
    """
    Find the minimum degree (edges per left node) so that Hall's marriage
    condition holds for every subset of `required_matching` left nodes.

    Args:
        n_left:            number of left nodes (e.g. 10 computers)
        n_right:           number of right nodes (e.g. 5 printers)
        required_matching: the subset size that must reach ALL right nodes (e.g. 5)

    Returns:
        Minimum degree per left node satisfying Hall's condition.

    Example:
        >>> halls_min_degree(10, 5, 5)
        3
    """
    left = list(range(n_left))
    right = list(range(n_right))

    for degree in range(1, n_right + 1):
        # Round-robin assignment: left node i gets printers [i*d % n_right, ...]
        adj = {
            u: [right[(u * degree + k) % n_right] for k in range(degree)] for u in left
        }

        if _check_hall(left, adj, required_matching):
            return degree * n_left

    raise ValueError("No valid degree found — check your parameters.")


def _check_hall(left: list, adj: dict, required_matching: int) -> bool:
    """
    Verify Hall's condition: for every subset S of left nodes with |S| <= required_matching,
    |N(S)| >= |S|.
    """
    for size in range(1, required_matching + 1):
        for subset in combinations(left, size):
            neighbors = {p for u in subset for p in adj[u]}
            if len(neighbors) < len(subset):
                return False
    return True


def count_permutations_subsequence(items: str | Sequence[str], subsequence: str) -> int:
    """Count permutations containing `subsequence` as a (non-contiguous) subsequence."""

    def has_subseq(perm: str, sub: str) -> bool:
        it = iter(perm)
        return all(c in it for c in sub)

    return sum(1 for p in get_permutations(items) if has_subseq(p, subsequence))


def count_permutations_with_constraints(
    items: str | Sequence[str],
    must_contain_any: Sequence[str] | None = None,
    must_contain_all: Sequence[str] | None = None,
    must_not_contain_any: Sequence[str] | None = None,
    exactly_one_of: Sequence[str] | None = None,
) -> int:
    perms = get_permutations(items)
    count = 0
    for perm in perms:
        if must_contain_any and not any(pat in perm for pat in must_contain_any):
            continue
        if must_contain_all and not all(pat in perm for pat in must_contain_all):
            continue
        if must_not_contain_any and any(pat in perm for pat in must_not_contain_any):
            continue
        if exactly_one_of and sum(1 for pat in exactly_one_of if pat in perm) != 1:
            continue
        count += 1
    return count


class _SetExprParser:
    _tok = re.compile(
        r"\s*(\(|\)|~|\\|∪|∩|union\b|inter\b|without\b|overline\b|[A-Za-z_][A-Za-z0-9_]*)"
    )

    def __init__(self, expression: str):
        self.tokens = self._tokenize(expression)
        self.pos = 0

    def _tokenize(self, expression: str):
        tokens = []
        i = 0
        while i < len(expression):
            m = self._tok.match(expression, i)
            if not m:
                raise ValueError(f"Invalid set token near: {expression[i : i + 15]}")
            tokens.append(m.group(1))
            i = m.end()
        return tokens

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _eat(self, expected=None):
        token = self._peek()
        if token is None:
            return None
        if expected and token != expected:
            raise ValueError(f"Expected {expected}, got {token}")
        self.pos += 1
        return token

    def parse(self):
        node = self._parse_union()
        if self._peek() is not None:
            raise ValueError(f"Unexpected token: {self._peek()}")
        return node

    def _parse_union(self):
        node = self._parse_inter()
        while self._peek() in ("union", "∪"):
            op = self._eat()
            rhs = self._parse_inter()
            node = (op, node, rhs)
        return node

    def _parse_inter(self):
        node = self._parse_unary()
        while self._peek() in ("inter", "∩", "without", "\\"):
            op = self._eat()
            rhs = self._parse_unary()
            node = (op, node, rhs)
        return node

    def _parse_unary(self):
        if self._peek() in ("~", "overline"):
            op = self._eat()
            return (op, self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self):
        token = self._peek()
        if token == "(":
            self._eat("(")
            node = self._parse_union()
            self._eat(")")
            return node
        if token is None:
            raise ValueError("Unexpected end of set expression.")
        if re.match(r"[A-Za-z_][A-Za-z0-9_]*$", token):
            self._eat()
            return ("var", token)
        raise ValueError(f"Unexpected token: {token}")


def _set_eval(ast_node, sets: dict[str, set], universal_set: set):
    op = ast_node[0]
    if op == "var":
        if ast_node[1] not in sets:
            raise KeyError(f"Unknown set name: {ast_node[1]}")
        return set(sets[ast_node[1]])
    if op in ("~", "overline"):
        return set(universal_set) - _set_eval(ast_node[1], sets, universal_set)
    if op in ("union", "∪"):
        return _set_eval(ast_node[1], sets, universal_set) | _set_eval(
            ast_node[2], sets, universal_set
        )
    if op in ("inter", "∩"):
        return _set_eval(ast_node[1], sets, universal_set) & _set_eval(
            ast_node[2], sets, universal_set
        )
    if op in ("without", "\\"):
        return _set_eval(ast_node[1], sets, universal_set) - _set_eval(
            ast_node[2], sets, universal_set
        )
    raise ValueError(f"Unknown set op: {op}")


def evaluate_set_expression(
    expression: str, sets: dict[str, set], universal_set: set
) -> set:
    ast = _SetExprParser(expression).parse()
    return _set_eval(ast, sets, set(universal_set))


def find_equivalent_set_options(
    target_expression: str,
    option_expressions: Sequence[str],
    sets: dict[str, set],
    universal_set: set,
) -> list[str]:
    target = evaluate_set_expression(target_expression, sets, universal_set)
    return [
        option
        for option in option_expressions
        if evaluate_set_expression(option, sets, universal_set) == target
    ]


def seating_count_two_tables(n: int, distinguish_left_right=False) -> int:
    if n <= 0:
        raise ValueError("n must be positive.")
    numerator = math.factorial(3 * n)
    denominator = 2 * n * n if distinguish_left_right else 8 * n * n
    return sp.Rational(numerator, denominator)


def totient_prime_product(p: int, q: int) -> int:
    if not sp.isprime(p) or not sp.isprime(q) or not (p < q):
        raise ValueError("Require primes p < q.")
    return (p - 1) * (q - 1)


def check_totient_options(option_expressions: Sequence[str]) -> dict[str, bool]:
    p, q = symbols("p q")
    target = p * q - p - q + 1
    out = {}
    for expr in option_expressions:
        out[expr] = sp.simplify(sp.sympify(expr) - target) == 0
    return out


def coefficient_of_monomial(expression, powers: dict[str, int]) -> sp.Expr:
    powers = {str(k): v for k, v in powers.items()}
    symbol_names = sorted(powers.keys())
    syms = symbols(" ".join(symbol_names))
    if not isinstance(syms, tuple):
        syms = (syms,)
    poly = Poly(sp.expand(expression), *syms)
    monom = tuple(powers[name] for name in symbol_names)
    return poly.coeff_monomial(monom)


def coefficient_matches_options(
    expression, powers: dict[str, int], options: Sequence[str]
) -> list[str]:
    coeff = coefficient_of_monomial(expression, powers)
    matches = []
    for option in options:
        try:
            if sp.simplify(sp.sympify(option) - coeff) == 0:
                matches.append(option)
        except Exception:
            continue
    return matches


def empty_set_option_truths() -> dict[str, bool]:
    empty = frozenset()
    option_set_with_empty = {empty}
    option_builder_empty = {x for x in []}
    option_set_with_set_with_empty = {frozenset({empty})}

    return {
        "{∅}": empty in option_set_with_empty,
        "{x ∈ ℝ : x < x}": empty in option_builder_empty,
        "{{∅}}": empty in option_set_with_set_with_empty,
        "∅": empty in set(),
    }


PolynomialGCD = polynomial_gcd
PolynomialExtendedGCD = polynomial_extended_gcd


# ---------------------------------------------------------------------------
# Number Theory basics
# ---------------------------------------------------------------------------


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def primes_below(n: int) -> list[int]:
    return [i for i in range(2, n) if is_prime(i)]


def lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


def extended_euclidean_table(a: int, b: int):
    """
    Extended Euclidean algorithm for integers, displayed as a readable table.

    Columns:
      step      — iteration index
      quotient  — floor(r_{k-2} / r_{k-1}), blank for first two rows
      remainder — current remainder r_k  (last non-zero = GCD)
      s (coeff of a)  — Bézout coefficient: remainder = s*a + t*b
      t (coeff of b)

    The GCD is the last non-zero value in the 'remainder' column.
    Prints: gcd(a, b) = result = s*a + t*b
    """
    import polars as pl

    r_prev, s_prev, t_prev = a, 1, 0
    r_curr, s_curr, t_curr = b, 0, 1
    rows = [
        {
            "step": 0,
            "quotient": None,
            "remainder": r_prev,
            f"s (×{a})": s_prev,
            f"t (×{b})": t_prev,
        },
        {
            "step": 1,
            "quotient": None,
            "remainder": r_curr,
            f"s (×{a})": s_curr,
            f"t (×{b})": t_curr,
        },
    ]
    k = 1
    while r_curr != 0:
        q = r_prev // r_curr
        r_next = r_prev % r_curr
        s_next = s_prev - q * s_curr
        t_next = t_prev - q * t_curr
        k += 1
        rows.append(
            {
                "step": k,
                "quotient": q,
                "remainder": r_next,
                f"s (×{a})": None if r_next == 0 else s_next,
                f"t (×{b})": None if r_next == 0 else t_next,
            }
        )
        r_prev, s_prev, t_prev = r_curr, s_curr, t_curr
        r_curr, s_curr, t_curr = r_next, s_next, t_next

    gcd_val, s_coeff, t_coeff = r_prev, s_prev, t_prev
    print(f"  gcd({a}, {b}) = {gcd_val}")
    print(f"  Bézout: {gcd_val} = ({s_coeff})·{a} + ({t_coeff})·{b}")
    print("  ↑ last non-zero in 'remainder' column")
    return pl.DataFrame(rows)


def polynomial_extended_euclidean_table(poly1, poly2):
    """
    Extended Euclidean algorithm for polynomials, displayed as a readable table.

    Columns:
      step      — iteration index
      quotient  — polynomial quotient at this step, blank for first two rows
      remainder — current remainder polynomial  (last non-zero = monic GCD)
      s (coeff of f)  — Bézout coefficient
      t (coeff of g)

    The GCD is the last non-zero value in the 'remainder' column (made monic).
    Prints: gcd = ..., Bézout identity.
    """
    import polars as pl
    from sympy import Poly, div

    p1 = Poly(poly1).set_domain("QQ")
    p2 = Poly(poly2, *p1.gens).set_domain("QQ")
    f_label = str(p1.as_expr())
    g_label = str(p2.as_expr())

    r_prev, s_prev, t_prev = (
        p1,
        Poly(1, *p1.gens, domain="QQ"),
        Poly(0, *p1.gens, domain="QQ"),
    )
    r_curr, s_curr, t_curr = (
        p2,
        Poly(0, *p1.gens, domain="QQ"),
        Poly(1, *p1.gens, domain="QQ"),
    )

    rows = [
        {
            "step": 0,
            "quotient": None,
            "remainder": str(r_prev.as_expr()),
            "s (×f)": str(s_prev.as_expr()),
            "t (×g)": str(t_prev.as_expr()),
        },
        {
            "step": 1,
            "quotient": None,
            "remainder": str(r_curr.as_expr()),
            "s (×f)": str(s_curr.as_expr()),
            "t (×g)": str(t_curr.as_expr()),
        },
    ]
    k = 1
    while not r_curr.is_zero:
        q, r_next = div(r_prev, r_curr, *p1.gens, domain="QQ")
        q = Poly(q, *p1.gens, domain="QQ")
        r_next = Poly(r_next, *p1.gens, domain="QQ")
        s_next = s_prev - q * s_curr
        t_next = t_prev - q * t_curr
        k += 1
        rows.append(
            {
                "step": k,
                "quotient": str(q.as_expr()),
                "remainder": str(r_next.as_expr()),
                "s (×f)": None if r_next.is_zero else str(s_next.as_expr()),
                "t (×g)": None if r_next.is_zero else str(t_next.as_expr()),
            }
        )
        r_prev, s_prev, t_prev = r_curr, s_curr, t_curr
        r_curr, s_curr, t_curr = r_next, s_next, t_next

    gcd_poly = r_prev.monic()
    lc = r_prev.LC()
    s_monic = Poly(s_prev.as_expr() / lc, *p1.gens, domain="QQ")
    t_monic = Poly(t_prev.as_expr() / lc, *p1.gens, domain="QQ")
    print(f"  gcd = {gcd_poly.as_expr()}")
    print(
        f"  Bézout: ({s_monic.as_expr()})·({f_label}) + ({t_monic.as_expr()})·({g_label})"
    )
    print("  ↑ last non-zero in 'remainder' column (made monic)")
    return pl.DataFrame(rows)


# ---------------------------------------------------------------------------
# Relations
# ---------------------------------------------------------------------------


def is_reflexive(S: set, R: set) -> bool:
    return all((x, x) in R for x in S)


def is_irreflexive(S: set, R: set) -> bool:
    return not any((x, x) in R for x in S)


def is_symmetric(R: set) -> bool:
    return all((b, a) in R for a, b in R)


def is_antisymmetric(R: set) -> bool:
    return all((b, a) not in R for a, b in R if a != b)


def is_transitive(R: set) -> bool:
    return all((a, d) in R for a, b in R for c, d in R if b == c)


def is_equivalence_relation(S: set, R: set) -> bool:
    return is_reflexive(S, R) and is_symmetric(R) and is_transitive(R)


def is_partial_order(S: set, R: set) -> bool:
    return is_reflexive(S, R) and is_antisymmetric(R) and is_transitive(R)


def is_total_order(S: set, R: set) -> bool:
    if not is_partial_order(S, R):
        return False
    return all((a, b) in R or (b, a) in R for a in S for b in S)


def is_well_order(S: set, R: set) -> bool:
    """Finite total order is always a well order."""
    return is_total_order(S, R)


def is_covering_relation(S: set, R: set) -> bool:
    """Hasse diagram edges: irreflexive + antisymmetric, and transitive closure gives a partial order."""
    if not is_irreflexive(S, R):
        return False
    if not is_antisymmetric(R):
        return False
    # Build transitive closure and check it forms a strict partial order
    tc = set(R)
    for _ in range(len(S)):
        tc = tc | {(a, c) for a, b in tc for x, c in tc if b == x}
    # tc should be irreflexive (no cycles) and antisymmetric
    return is_irreflexive(S, tc) and is_antisymmetric(tc)


def classify_relation(S: set, R: set) -> dict[str, object]:
    refl = is_reflexive(S, R)
    irrefl = is_irreflexive(S, R)
    sym = is_symmetric(R)
    antisym = is_antisymmetric(R)
    trans = is_transitive(R)

    equiv = refl and sym and trans
    partial = refl and antisym and trans
    total = partial and all((a, b) in R or (b, a) in R for a in S for b in S)
    well = total  # finite sets: every total order is a well order
    covering = is_covering_relation(S, R)

    labels = []
    if covering:
        labels.append("Hasse / covering relation")
    if well:
        labels.append("Well order")
    elif total:
        labels.append("Total order")
    elif partial:
        labels.append("Partial order")
    if equiv:
        labels.append("Equivalence relation")
    if not labels:
        labels.append("None of the above")

    return {
        "reflexive": refl,
        "irreflexive": irrefl,
        "symmetric": sym,
        "antisymmetric": antisym,
        "transitive": trans,
        "classification": labels,
    }


# ---------------------------------------------------------------------------
# Bipartite graphs
# ---------------------------------------------------------------------------


def _gale_ryser(d1: list[int], d2: list[int]) -> bool:
    """True if a simple bipartite graph with degree sequences d1 (|V1|) and d2 (|V2|) exists."""
    if sum(d1) != sum(d2):
        return False
    d1 = sorted(d1, reverse=True)
    d2 = sorted(d2, reverse=True)
    n2 = len(d2)
    for k in range(1, len(d1) + 1):
        lhs = sum(d1[:k])
        rhs = sum(min(d2[j], k) for j in range(n2))
        if lhs > rhs:
            return False
    return True


def complete_graph_edges(n: int) -> int:
    """Number of edges in the complete graph K_n."""
    return n * (n - 1) // 2


def inclusion_exclusion_uniform(n_sets: int, intersection_sizes: list[int]) -> int:
    """
    Inclusion-exclusion where every k-way intersection has the same size.

    intersection_sizes[0] = size of each individual set
    intersection_sizes[1] = size of each pairwise intersection
    intersection_sizes[2] = size of each triple intersection
    ...

    Example (Q6): 4 sets, |A|=200, |A∩B|=50, |A∩B∩C|=25, |all 4|=5
        inclusion_exclusion_uniform(4, [200, 50, 25, 5])
    """
    from math import comb

    total = 0
    for k, size in enumerate(intersection_sizes, start=1):
        total += ((-1) ** (k + 1)) * comb(n_sets, k) * size
    return total


def bipartite_degree_check(
    v1_degrees: list[int], v2_degrees: list[int]
) -> dict[str, object]:
    """
    Classify whether a bipartite graph with the given degree sequences exists.
    Returns classification string matching the exam answer options.
    """
    n1, n2 = len(v1_degrees), len(v2_degrees)
    s1, s2 = sum(v1_degrees), sum(v2_degrees)

    # Check bounds for simple graph
    v1_exceeds = any(d > n2 for d in v1_degrees)
    v2_exceeds = any(d > n1 for d in v2_degrees)

    simple_possible = (s1 == s2) and not v1_exceeds and not v2_exceeds
    if simple_possible:
        simple_possible = _gale_ryser(v1_degrees, v2_degrees)

    multi_possible = s1 == s2  # with multi-edges any equal-sum sequence works

    if simple_possible:
        classification = "Exists without multiple edges"
    elif multi_possible:
        classification = "Exists only with multiple edges"
    elif s1 < s2:
        classification = "Does not exist, but will if we increase a degree in V1"
    elif s1 > s2:
        classification = "Does not exist, but will if we increase a degree in V2"
    else:
        classification = "None of these"

    return {
        "sum_V1": s1,
        "sum_V2": s2,
        "v1_degree_exceeds_V2": v1_exceeds,
        "v2_degree_exceeds_V1": v2_exceeds,
        "classification": classification,
    }
