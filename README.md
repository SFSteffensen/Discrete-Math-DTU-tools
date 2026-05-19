# Discrete Math DTU Tools

Python tools for **01017 Discrete Mathematics** at DTU, with an accompanying Jupyter notebook.

`discrete_tools.py` is a self-contained library covering the topics examined in the course.
`notebook.ipynb` walks through every tool with worked examples, and includes a full solved
walkthrough of the **E25 exam** (all 21 questions).

---

## Quick start

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
jupyter lab notebook.ipynb
# or open in VS Code with the Jupyter extension
```

---

## What's included

### `discrete_tools.py`

| Topic | Functions |
|---|---|
| **Number theory** | `extended_euclidean_table`, `divide_with_remainder`, `is_prime`, `primes_below`, `lcm` |
| **Modular arithmetic** | `congruences_system_solver`, `totient_prime_product`, `check_totient_options` |
| **Polynomials** | `polynomial_gcd`, `polynomial_extended_gcd`, `polynomial_extended_euclidean_table` |
| **Combinatorics** | `get_permutations`, `get_r_permutations`, `get_r_combinations`, `get_combinations` |
| **Permutation constraints** | `count_permutations_subsequence`, `count_permutations_with_constraints` |
| **Derangements** | `derangements_count`, `get_derangements` |
| **Circular seating** | `seating_count_two_tables` |
| **Pigeonhole** | `minimum_selections_for_sum`, `subset_count_size`, `subset_parity_counts_1_to_n` |
| **Hypercube graphs** | `hypercube_vertices`, `hypercube_edges`, `hypercube_info` |
| **Relations** | `classify_relation`, `is_reflexive`, `is_symmetric`, `is_antisymmetric`, `is_transitive`, `is_equivalence_relation`, `is_partial_order`, `is_total_order`, `is_well_order`, `is_covering_relation` |
| **Functions** | `classify_function_finite`, `classify_linear_function_descriptor` |
| **Graph theory** | `bipartite_degree_check` |
| **Logic** | `tautology_checker` |
| **Set algebra** | `evaluate_set_expression`, `find_equivalent_set_options`, `empty_set_option_truths` |
| **Binomial / generating** | `coefficient_of_monomial`, `coefficient_matches_options`, `match_answers` |
| **Sequences** | `recursive_piecewise_value` |

### `notebook.ipynb`

- **Reference & Tools:** one section per topic above, with copy-paste templates
- **E25 Exam:** all 21 questions worked through programmatically, answers verified against the official answer key sheet.

---

## Dependencies

| Package | Purpose |
|---|---|
| `sympy` | Symbolic maths, GCD, polynomials, totient, binomial |
| `polars` | Pretty-printed EEA tables |
| `ipykernel` | Jupyter kernel |

No other installs needed beyond what `uv sync` pulls in.

---

## Releases

Tagged releases on GitHub include a cleaned `notebook_clean.ipynb` (no outputs or execution counts)
alongside `discrete_tools.py`, so you can download and run from scratch without any repo history.

```bash
# Cut a release from main
git tag v1.x.x
git push origin v1.x.x
```

---

## Topics covered

Number theory · Modular arithmetic · CRT · Polynomial GCD · Combinatorics · Derangements ·
Hypercube graphs · Inclusion-exclusion · Pigeonhole · Relations · Function classification ·
Tautologies · Set algebra · Induction · Circular seating · Binomial coefficients
