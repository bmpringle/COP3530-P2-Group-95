"""Checks the DP against brute force on small random instances."""

import itertools
import random

from dp_allocation import allocate


def brute_force(options, budget):
    states = sorted(options)
    best = 0.0
    # each state: pick no option (None) or one option
    for combo in itertools.product(*[[None] + options[s] for s in states]):
        cost = sum(c[0] for c in combo if c)
        if cost <= budget:
            best = max(best, sum(c[1] for c in combo if c))
    return best


def main():
    random.seed(1)
    for trial in range(300):
        n_states = random.randint(1, 5)
        options = {}
        for i in range(n_states):
            k = random.randint(1, 4)
            options[f"S{i}"] = [(10 * j, random.uniform(-5, 30)) for j in range(1, k + 1)]
        budget = 10 * random.randint(0, 12)
        dp_total, plan = allocate(options, budget, 10)
        bf = brute_force(options, budget)
        assert abs(dp_total - bf) < 1e-9, (trial, dp_total, bf)
        assert sum(plan.values()) <= budget
        recomputed = sum(dict(options[s])[c] for s, c in plan.items())
        assert abs(recomputed - dp_total) < 1e-9, "backtracking disagrees with dp value"
    print("OK: 300 random cases match brute force")


if __name__ == "__main__":
    main()
