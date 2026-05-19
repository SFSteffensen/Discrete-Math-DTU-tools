#import "@local/dtu-template:0.6.3":*

// pmod: LaTeX-style "parenthesized mod" notation: a ≡ b (mod m)
#let pmod(m) = $space (mod #m)$

// Small circle for marking answers
#let mark-circle = box(width: 0.8em, height: 0.8em, stroke: 0.5pt + black, radius: 50%)
#let mark-circle-filled = box(width: 0.8em, height: 0.8em, stroke: 0.5pt + black, fill: black, radius: 50%)

// Answer option with circle (empty = not selected, filled = correct answer)
#let ans(body, correct: false) = grid(
  columns: (auto, 1fr),
  column-gutter: 0.5em,
  align: (center, left),
  if correct { mark-circle-filled } else { mark-circle },
  body,
)

// Shorthand for marking correct answer
#let correct(body) = ans(body, correct: true)

#show: dtu-note.with(
  course: "01017",
  course-name: "Discrete Mathematics",
  title: "Facitliste E25 - Exam Answer Key",
  date: datetime(year: 2025, month: 12, day: 11),
  author: "Validated with SymPy",
  semester: "2025 Fall",
)

= E25 Exam Discrete Mathematics

Der anvendes en scoringsalgoritme, som er baseret på "One correct answer"

- Der er altid præcist ét korrekt svar
- Studerende kan kun vælge ét svar per spørgsmål
- Hvert rigtigt svar giver 1 point
- Hvert forkert svar giver 0 point (der benyttes IKKE negative point)

#pagebreak()

== Question 1

If $p,q$ are prime numbers such that $100 < p < q$, then the number of positive integers less than $p q$ which are relatively prime to $p q$ is:

#correct[$p q - p - q + 1$]
#ans[$p q - q + 1$]
#ans[$p q - p - q - 1$]
#ans[$p q - p - q$]
#ans[$p q - 1$]
#ans[None of these]

#pagebreak()
== Question 2

The number $(4^100 mod 6)^100 mod 10$ equals

#ans[$3$]
#correct[$6$]
#ans[$2$]
#ans[None of these]
#ans[$5$]
#ans[$1$]
#ans[$4$]

#pagebreak()
== Question 3

Consider the set of all $99$ positive integers not exceeding $99$.

*Vælg de rigtige svarmuligheder*

#table(
  columns: (1fr, 0.2fr, 0.2fr, 0.2fr, 0.2fr, 0.4fr, 0.2fr, 0.5fr, 0.4fr),
  align: (left, center, center, center, center, center, center, center, center),
  [*Sub-question*],
  [$binom(99, 50)$],
  [$2^98$],
  [$2^97$],
  [$2^49$],
  [None],
  [$2^50$],
  [$binom(99, 50) binom(99, 49)$],
  [$binom(99, 49)^2$],
  [How many subsets have an odd number of odd numbers and an even number of even numbers?],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [How many subsets have an odd number of even numbers and an even number of odd numbers?],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [How many subsets have $49$ elements?],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [How many subsets have an odd number of odd numbers?],
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 4

Consider the following system of congruences:

$
  x &equiv 1 #pmod(2) \
  x &equiv 1 #pmod(5) \
  x &equiv 7 #pmod(9)
$

Indicate the set of all solutions to the above system of congruences.

#ans[None of these]
#ans[${90 + 7k | k in ZZ}$]
#ans[${1 + 2k | k in ZZ} union {1 + 5k | k in ZZ} union {7 + 9k | k in ZZ}$]
#ans[${9 + 90k | k in ZZ}$]
#correct[${61 + 90k | k in ZZ}$]
#ans[${7 + 90k | k in ZZ}$]
#pagebreak()
== Question 5

Find a greatest common divisor of the polynomials $x^3 - 1$ and $x^3 + 2x^2 + 2x + 1$

#ans[$x + 1$]
#ans[$1$]
#ans[$x - 1$]
#correct[$x^2 + x + 1$]
#ans[$x^2 + x - 1$]
#ans[None of these]
#ans[$x^2 - x + 1$]
#ans[$x^2 - x - 1$]
#pagebreak()
== Question 6

Recall that $NN$ is the set of natural numbers, in other words the set of nonnegative integers. For all $n in NN$ define $f(n) = sum^n_(k=0) k dot k! = 0 dot 0! + 1 dot 1! + dots + n dot n!$. It is possible to prove by induction that $f(n) = (n+1)! - 1$ holds for all nonnegative integers $n$.

By choosing 4 of the following 8 text fragments and putting them in the correct order, a proof by induction for the above statement can be created.

*A.* To prove the induction step, we assume that $f(n+1) = ((n+1)+1)!$ holds for some $n in NN$. We will now prove that under this assumption, $f(n) = (n+1)!-1$

*B.* To prove the induction step we assume that $f(n) = (n+1)!-1$ holds for some $n in NN$. We will now prove that under this assumption, $f(n+1) = ((n+1)+1)!-1$ holds for all $n in NN$.

*C.* To prove the induction step, we assume that $f(n) = (n+1)! - 1$ for all $n in NN$. We now prove that $f(n+1) = ((n+1)+1)! -1$

*D.* The statement now follows from the principle of mathematical induction.

*E.* We prove the statement by induction. The base case is $n = 1$. For $n=1$, we see that $f(1) = sum^1_(k=0)k dot k! = 0 dot 0! + 1 dot 1! = 0 dot 1 + 1 dot 1 = 1$ and also that $(n+1)! -1 = (1+1)!-1 = 2!-1 = 2-1 =1$. This proves the base case.

*F.* We prove the statement by induction. The base case is $n=0$. For $n=0$, we see that $f(0) = sum^0_(k=0) k dot k! = 0 dot 0! = 0 dot 1 = 0$ and also that $(n+1)! -1 = (0+1)!-1 = 1!-1 = 1-1 =0$. This proves the base case.

*G.* We have that $
  f(n) &= sum^n_(k=0) k dot k! \
       &= (sum^(n+1)_(k=0) k dot k! ) - (n+1)(n+1)! \
       &= f(n+1) - (n+1)(n+1)! \
       &= ((n+1)+1)! - 1 - (n+1)(n+1)! "By the induction hypothesis" \
       &= (n+2)! -(n+1)(n+1)!-1 \
       &= (n+2)(n+1)!-(n+1)(n+1)!-1 \
       &= (n+2 - (n+1))(n+1)!-1 \
       &= (n+1)! -1
$ which is what we wanted to prove. This concludes the induction step.

*H.* We have that $
  f(n+1) &= sum^(n+1)_(k=0) k dot k! \
         &= (sum^n_(k=0) k dot k!) + (n+1)(n+1)! \
         &= f(n)+(n+1)(n+1)! \
         &= (n+1)!-1+(n+1)(n+1)! "By the induction hypothesis" \
         &= (n+1)(n+1)!+(n+1)!-1 \
         &= [(n+1)+1](n+1)!-1 \
         &= (n+2)! - 1 = ((n+1)+1)!-1
$ which is what we wanted to prove. This concludes the induction step.

*Select the fragments in order:*

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center, center, center, center),
  [],
  [A],
  [B],
  [C],
  [D],
  [E],
  [F],
  [G],
  [H],
  [1st fragment],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  [2nd fragment],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [3rd fragment],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  [4th fragment],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 7

For all $n in NN$ define $a_n$ recursively as follows:

$a_0 = 2, a_1 = 3, a_n = cases(a_(n-1) + n "if" n "is even", a_(n-1) + 2a_(n-2) "if" n "is odd")$

Compute $a_5$.

#correct[$37$]
#ans[$38$]
#ans[$35$]
#ans[$40$]
#ans[None of these]
#ans[$36$]
#ans[$39$]
#pagebreak()
== Question 8

We wish to construct a bipartite graph with bipartition $(V_1, V_2)$ such that $|V_1| = 4, |V_2| = 5$. (Note that a bipartite graph has no loops, but it may contain multiple edges.)

*Vælg de rigtige svarmuligheder*

#table(
  columns: (6),
  align: (left, center, center, center, center, center),
  [],
  [Exists w/o multiple edges],
  [Exists only with multiple edges],
  [Does not exist, but will if we increase a degree in $V_1$],
  [Does not exist, but will if we increase a degree in $V_2$],
  [None of these],
  [If degrees in $V_1$ are $1,2,2,2$ and degrees in $V_2$ are $1,2,2,2,2$, then],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  [If degrees in $V_1$ are $5,5,5,5$ and degrees in $V_2$ are $4,4,4,4,4$, then],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [If degrees in $V_1$ are $4,4,4,4$ and degrees in $V_2$ are $5,5,5,5,5$, then],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 9

The formula $binom(m+n, r) = sum^r_(k=a) binom(m, r-k) binom(n, k)$ is true for all integers $m,n,r$ satisfying $0 < m < r < n$ if we let the summation start with:

#ans[$a = n$]
#ans[$a = r$]
#ans[None of these]
#ans[$a = n - r$]
#ans[$a = m$]
#correct[$a = r - m$]
#pagebreak()
== Question 10

Let $A = {0,1,2,4}, B = {0,1,3,5}$, and $C = {0,2,3,6}$. If the universal set $U = {0,1,2,3,4,5,6,7}$, then which of the following is equal to $((A inter B) backslash C) union ((B inter C) backslash A) union ((C inter A) backslash B)$?

#ans[${0,1,2,3}$]
#ans[All of these sets]
#ans[$emptyset$]
#ans[${4,5,6}$]
#ans[None of these]
#ans[${0,4,5,6}$]
#correct[${1,2,3}$]
#pagebreak()
== Question 11

Consider the statement "for every positive rational number $x$ there are positive integers $a$ and $b$ such that $x = a/b$ and $gcd(a, b) = 1$." Which of the following statements in predicate logic is equivalent to this if we let $G(a,b)$ denote the statement "$a$ and $b$ are relatively prime"?

#ans[It is not possible to translate the statement into predicate logic.]
#correct[$forall x in QQ^+ exists a in ZZ^+ exists b in ZZ^+ (x = a/b and G(a,b))$]
#ans[$forall x in QQ^+ exists a in ZZ^+ exists b in ZZ^+ (G(a,b) -> x = a/b)$]
#ans[$forall x in QQ^+ forall a in ZZ^+ forall b in ZZ^+ (x = a/b and G(a,b))$]
#ans[$forall x in QQ^+ exists a in ZZ^+ exists b in ZZ^+ (x = a/b -> G(a,b))$]
#pagebreak()
== Question 12

Given a universal set $U$, which of the following is equal to the set $A inter overline((B backslash C))$?

#ans[None of these]
#ans[$A inter B inter overline(C)$]
#ans[$(A union B) inter (A union overline(C))$]
#correct[$(A inter overline(B)) union (A inter C)$]
#ans[$A inter overline(B) inter C$]
#ans[$A inter (C backslash B)$]
#pagebreak()
== Question 13

The empty set is an element of which of the following sets?

#ans[${{emptyset}}$]
#ans[None of these]
#ans[$emptyset$]
#ans[${x in RR : x < x}$]
#correct[${emptyset}$]
#ans[All of these sets]
#pagebreak()
== Question 14

Which of the following are tautologies?

#ans[$(p -> q) or (not q -> not p)$]
#ans[None of these]
#ans[$p <-> q$]
#ans[All of these]
#correct[$(not p or not q) -> (not (p and q))$]
#ans[$(p or q or r) and (p or not q or not r)$]
#pagebreak()
== Question 15

Consider all possible seatings of $3n$ people around two tables, one with $n$ seats and one with $2n$ seats. Find the number of seatings when:

*Vælg de rigtige svarmuligheder*

#table(
  columns: (10),
  align: (left, center, center, center, center, center, center, center, center, center),
  [],
  [$((3n)!)/(2(n!))$],
  [$((3n)!)/(4(n!))$],
  [$((3n)!)/(4n)$],
  [$2 binom(3n, n)$],
  [$((3n)!)/(2n^2)$],
  [$((3n)!)/(4n^2)$],
  [$((3n)!)/(8n^2)$],
  [$4 binom(3n, n)$],
  [None],
  [Two seatings are the same when each person has the same left and right neighbor.],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [Two seatings are the same when each person has the same neighbors (we do not care about right or left).],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 16

For each of the following, determine whether it is surjective/injective, or not a well defined function. Recall that $NN$ is the set of natural numbers, in other words the set of nonnegative integers.

*Vælg de rigtige svarmuligheder*

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center),
  [*Function*],
  [*Not well defined*],
  [*well defined but neither Neither*],
  [*Surjective*],
  [*Injective*],
  [*Both*],
  [$f: RR -> ZZ$ given by $f(x) = 2 floor(x/2)$],
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  [$f: RR -> {x in RR : x >= 0}$ given by $f(x) = sqrt(x^2)$],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  [$f: NN -> NN$ given by $f(x) = 2x + 7$],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  [$f: NN -> NN$ given by $f(x) = x - x^2$],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [$f: RR -> RR$ given by $f(x) = cases(x "if" x in QQ, -x "if" x in.not QQ)$],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
)
#pagebreak()
== Question 17

Consider all permutations of ABCDE.

*Vælg de rigtige svarmuligheder*

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center, center, center),
  [*Constraint*],
  [$12$],
  [$24$],
  [$36$],
  [$48$],
  [$50$],
  [$64$],
  [None],
  [Contain none of AB, BC, CD],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  [Contain ACE (as subsequence)],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  [Contain precisely one of AB, CD],
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 18

For each relation on the set of four distinct elements ${a, b, c, d}$ below, decide which property it has.

*Vælg de rigtige svarmuligheder*

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center, center, center),
  [*Relation*],
  [Hasse],
  [Partial],
  [Total],
  [Well],
  [None],
  [Tot. not part.],
  [Equiv.],
  [${(a,a),(a,b),(a,c),(a,d)}$],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  [${(a,b),(b,c),(c,d)}$],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [${(a,a),(b,b),(c,c),(d,d),(a,d),(d,a)}$],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  [${(a,a),(b,b),(c,c),(d,d),(d,c)}$],
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [${(a,a),(b,b),(c,c),(d,d),(a,b),(a,c),(a,d),(b,c),(b,d),(c,d)}$],
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 19

Which of the following is a recursively defined function for the number of ways to tile an $n times 2$ board using $2 times 1$ tiles?

#correct[$f(0) = 1, f(1) = 1, f(n) = f(n - 1) + f(n - 2)$ for $n >= 2$]
#ans[$f(0) = 0, f(1) = 1, f(n) = 2f(n - 2)$ for $n >= 2$]
#ans[$f(0) = 1, f(1) = 1, f(n) = 2f(n - 2)$ for $n >= 2$]
#ans[$f(0) = 1, f(1) = 1, f(n) = f(n - 1)f(n - 2)$ for $n >= 2$]
#ans[All of these]
#ans[$f(0) = 0, f(1) = 1, f(n) = f(n - 1) + f(n - 2)$ for $n >= 2$]
#ans[None of these]
#pagebreak()
== Question 20

Find the coefficient of $x^15 y^20$ in the polynomials below.

*Vælg de rigtige svarmuligheder*

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, center, center, center, center, center),
  [*Polynomial*],
  [$-binom(10, 5) 2^5$],
  [$binom(10, 5) 2^15$],
  [$-binom(10, 5) 2^15$],
  [$0$],
  [None],
  [$-binom(10, 5) 2^10$],
  [$-binom(10, 3) 2^5$],
  [$(2x^3 - y^4)^10$],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [$(1 - 2x^3 y^4)^10$],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  [$(x^3 - 2y^4)^10$],
  mark-circle-filled,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
  mark-circle,
)
#pagebreak()
== Question 21

Which of the following is equivalent to the statement "$a$ and $b$ are relatively prime"? The domain for each statement is the set of all positive integers.

#ans[None of these three are equivalent to the statement.]
#ans[$not (exists c (c divides a and c divides b and c > 1))$ is equivalent to the statement, and the other two are not.]
#ans[$forall c (not (c divides a) or not (c divides b) or (c <= 1))$ is equivalent to the statement, and the other two are not.]
#correct[All of these three are equivalent to the statement.]
#ans[$forall c ((c divides a and c divides b) -> (c <= 1))$ is equivalent to the statement, and the other two are not.]
