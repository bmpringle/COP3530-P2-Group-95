from tkinter import messagebox, simpledialog

import pandas as pd

from data_processing import build_options, state_metrics
from dp_allocation import allocate

STEP = 10  # investment step, $ millions


def dp_budget_algorithm(data) -> pd.DataFrame | None:
    """Split one budget across states to maximize total profit (dynamic programming)."""
    investment_budget = simpledialog.askfloat(
        "Investment Budget",
        "What is your investment budget for generating power? (In USD)",
    )

    if not investment_budget or investment_budget <= 0:
        return None

    rows = data.fillna("").to_dict("records")
    options = build_options(state_metrics(rows), step=STEP)

    # Spending past the largest option in every state is pointless, so cap the budget.
    max_spend = sum(opts[-1][0] for opts in options.values())
    budget = min(investment_budget / 1e6, max_spend)  # in $ millions

    _, plan = allocate(options, budget, STEP)
    if not plan:
        messagebox.showinfo(
            title="No Profitable Investment",
            message="No profitable investment fits this budget. Try at least $10 million.",
        )
        return None

    states = list(plan)
    invested = [plan[s] for s in states]
    profit = [dict(options[s])[plan[s]] for s in states]

    return pd.DataFrame(
        {
            "State": states,
            "Invested ($M)": invested,
            "Profit ($M)": profit,
            "ROI": [p / c * 100 for p, c in zip(profit, invested)],  # % over 20 years
        }
    )
