
import sys

from data_processing import build_options, load_rows, roi_ranking, state_metrics


def allocate(options, budget, step):
    """Optimal allocation.

    options: {state: [(cost, profit), ...]} with every cost a multiple of `step`.
    budget:  total budget, same units as cost.
    Returns (total_profit, {state: cost invested}) with only invested states listed.
    """
    states = sorted(options)
    cap = int(budget // step)
    n = len(states)

    # dp[s][b]: best profit using the first s states with b budget units.
    dp = [[0.0] * (cap + 1) for _ in range(n + 1)]
    # choice[s][b]: index of the option taken for state s-1 at budget b, or -1 for none.
    choice = [[-1] * (cap + 1) for _ in range(n + 1)]

    for s in range(1, n + 1):
        opts = options[states[s - 1]]
        for b in range(cap + 1):
            best, pick = dp[s - 1][b], -1          # skip this state
            for k, (cost, profit) in enumerate(opts):
                units = int(round(cost / step))
                if units <= b:
                    cand = dp[s - 1][b - units] + profit
                    if cand > best:
                        best, pick = cand, k
            dp[s][b] = best
            choice[s][b] = pick

    # Backtrack to find how much goes into each state.
    plan = {}
    b = cap
    for s in range(n, 0, -1):
        k = choice[s][b]
        if k != -1:
            cost = options[states[s - 1]][k][0]
            plan[states[s - 1]] = cost
            b -= int(round(cost / step))
    return dp[n][cap], plan


def best_single_state(options, budget):
    """Best state to invest in alone: highest profit among options within the budget."""
    best = None
    for s, opts in options.items():
        for cost, profit in opts:
            if cost <= budget and (best is None or profit > best[2]):
                best = (s, cost, profit)
    return best


def run(path, budget=500.0, step=10):
    metrics = state_metrics(load_rows(path))
    options = build_options(metrics, step=step)
    total, plan = allocate(options, budget, step)
    return metrics, options, total, plan


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "electricity.csv"
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
    metrics, options, total, plan = run(csv_path, budget)
    print(f"Budget ${budget:.0f}M across {len(options)} states")
    print(f"Optimal total profit: ${total:.1f}M, invested ${sum(plan.values()):.0f}M")
    for s, cost in sorted(plan.items(), key=lambda kv: -kv[1]):
        profit = dict(options[s])[cost]
        print(f"  {s}: invest ${cost:.0f}M -> profit ${profit:.1f}M (ROI {profit / cost:.2f}/$)")
    s, cost, profit = best_single_state(options, budget)
    print(f"Best single state: {s}, invest ${cost:.0f}M, profit ${profit:.1f}M")
    print("Top 5 by ROI per dollar:", [(r[0], round(r[1], 2)) for r in roi_ranking(options)[:5]])
