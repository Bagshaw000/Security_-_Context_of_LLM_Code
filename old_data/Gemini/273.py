0.82 \cdot 0.9 + P_{2}(0) \cdot 0.1 = 0.82 \cdot 0.9 + (0.1 \cdot 0.9) \cdot 0.1 = 0.738 + 0.009 = 0.747$.
        - Pick $\{0.1, 0.1\}$: $P(1)=0.1 \cdot 0.9 + 0.9 \cdot 0.1 = 0.18$.
        So $\{0.9\}$ is better than $\{0.1, 0.1\}$.
        The $n$ largest probabilities are always the best candidates to form the set.

    *   Wait, what if $n=1$ and coins are $\{0.6, 0.6, 0.6\}$?
        - Pick $\{0.6\}$: $P(1)=0.6$.
        - Pick $\{0.6, 0.6\}$: $P(1)=2 \cdot 0.6 \cdot 0.4 = 0.48$.
        - Pick $\{0.6, 0.6, 0.6\}$: $P(1)=3 \cdot 0.6 \cdot 0.4^2 = 3 \cdot 0.6 \cdot 0.16 = 0.288$.
        Here, the best is