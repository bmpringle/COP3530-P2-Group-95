from data_processing import build_options, load_rows, state_metrics
from dp_allocation import allocate

STEP = 10  # investment step, $ millions


def get_results(algorithm, csv_path, budget=500):
    """Return (table, categories, values) for the GUI. Algorithm 4 is the DP budget allocation.

    table:      {"columns": [...], "rows": [[...], ...]}  (rows is a 2D array)
    categories: list of state names, one per bar group
    values:     {"property name": [ints, same order as categories]}
    """
    if algorithm != 4:
        raise ValueError(f"Algorithm {algorithm} is not available yet")

    options = build_options(state_metrics(load_rows(csv_path)), step=STEP)
    total, plan = allocate(options, budget, STEP)
    states = sorted(plan, key=lambda s: -plan[s])  # biggest investment first

    def profit(s):
        return dict(options[s])[plan[s]]

    table = {
        "columns": ["State", "Invested ($M)", "Profit ($M)", "ROI per $"],
        "rows": [[s, plan[s], round(profit(s), 1), round(profit(s) / plan[s], 2)] for s in states],
    }
    categories = states
    values = {
        "Invested ($M)": [int(plan[s]) for s in states],
        "Profit ($M)": [round(profit(s)) for s in states],
    }
    return table, categories, values
