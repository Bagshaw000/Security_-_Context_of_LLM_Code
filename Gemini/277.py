3, P(1) = 3(0.5)(0.5)^2 = 0.375$
    *   If $p_i$ are all $0.1$, then for $n=1$:
        *   $k=1, P(1) = 0.1$
        *   $k=2, P(1) = 2(0.1)(0.9) = 0.18$
        *   $k=10, P(1) = 10(0.1)(0.9)^9 = 0.387$
    *   So the subset size $k$ definitely matters.
    *   But the prompt says "Given a set of 2n coins... pick a set...". This usually implies the set you pick is a subset of the $2n$.
    *   I will write a solution that finds the optimal subset (of any size) to maximize $P(X=n)$.
    *   And I will use the "i largest and j smallest" theorem to narrow the search space.

    *   Theorem (Hill & Lion, 1980): The subset of size $m$ that maximizes $P(X=k)$ consists of $i$ probabilities $p_{(1)}, \dots, p_{(i)}$ and $m-i$ probabilities $p_{(n-m+i+1)}, \dots, p_{(n)}$. (i.e., the