
import csv
from dataclasses import dataclass

import numpy as np

# The 50 U.S. states. The dataset also contains DC, territories and a blank
# state row, which the issue's "rank all 50 states" requirement excludes.
STATES_50 = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
    "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
}


ELASTICITY = -0.5            # demand elasticity: more supply pushes the price down
MARGINAL_COST_FRACTION = 0.6  # cost to generate, as a fraction of the national avg price
CAPEX_PER_MWH_YEAR = 1000.0   # dollars of investment per extra MWh/year of capacity
HORIZON_YEARS = 20            # years of profit counted against the investment
STEP_MILLIONS = 10            # investment option granularity, $ millions
MAX_OPTIONS = 20              # options per state: $10M, $20M, ... $200M


@dataclass
class StateMetrics:
    state: str
    utilities: int
    customers: float            # residential customers
    revenue_k: float            # residential revenue, thousands of dollars
    sales_mwh: float            # residential sales, MWh
    summer_peak_mw: float
    annual_bill: float          # dollars per residential customer per year
    price_per_mwh: float        # dollars per MWh
    peak_per_customer_kw: float  # demand proxy


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def state_metrics(rows):
    """Aggregate utility rows into one StateMetrics per state (50 states only)."""
    acc = {}
    for r in rows:
        s = r["Utility.State"].strip()
        if s not in STATES_50:
            continue
        a = acc.setdefault(s, [0, 0.0, 0.0, 0.0, 0.0])
        a[0] += 1
        a[1] += _num(r["Retail.Residential.Customers"])
        a[2] += _num(r["Retail.Residential.Revenue"])
        a[3] += _num(r["Retail.Residential.Sales"])
        a[4] += _num(r["Demand.Summer Peak"])

    out = {}
    for s, (n, cust, rev, sales, peak) in acc.items():
        if cust <= 0 or sales <= 0:
            continue
        out[s] = StateMetrics(
            state=s,
            utilities=n,
            customers=cust,
            revenue_k=rev,
            sales_mwh=sales,
            summer_peak_mw=peak,
            annual_bill=rev * 1000 / cust,   # the proposal's formula
            price_per_mwh=rev * 1000 / sales,
            peak_per_customer_kw=peak * 1000 / cust,
        )
    return out


def national_price(metrics):
    rev = sum(m.revenue_k for m in metrics.values())
    sales = sum(m.sales_mwh for m in metrics.values())
    return rev * 1000 / sales


# ---------------------------------------------------------------------------
# Investment options (input to the DP algorithm, issue #7)
# ---------------------------------------------------------------------------
def option_profit(m, invest_millions, nat_price):
    """Net profit (dollars) over HORIZON_YEARS of investing `invest_millions` in a state.

    Extra capacity adds supply, which lowers the state's price (elasticity), so
    each additional dollar earns less: profit grows but ROI per dollar falls.
    """
    invest = invest_millions * 1e6
    extra_mwh = invest / CAPEX_PER_MWH_YEAR
    new_price = m.price_per_mwh * (1 + extra_mwh / m.sales_mwh) ** (1 / ELASTICITY)
    margin = new_price - MARGINAL_COST_FRACTION * nat_price
    return extra_mwh * margin * HORIZON_YEARS - invest


def build_options(metrics, step=STEP_MILLIONS, n_options=MAX_OPTIONS):
    """Return {state: [(cost_millions, profit_millions), ...]} - one list per state."""
    nat = national_price(metrics)
    options = {}
    for s, m in metrics.items():
        options[s] = [
            (k * step, option_profit(m, k * step, nat) / 1e6)
            for k in range(1, n_options + 1)
        ]
    return options


def roi_ranking(options):
    """Rank states by best ROI per dollar, and find where ROI per dollar stops improving.

    Returns rows: (state, best_roi, invest_at_best_roi_millions, profit_there_millions,
    efficient_limit_millions). ROI per dollar is highest at the smallest investment
    because of diminishing returns, so `efficient_limit` is the cutoff the issue asks
    for: the largest investment whose last step still adds profit (marginal ROI > 0).
    """
    rows = []
    for s, opts in options.items():
        best = max(opts, key=lambda o: o[1] / o[0])
        limit = max(opts, key=lambda o: o[1])[0]
        rows.append((s, best[1] / best[0], best[0], best[1], limit))
    rows.sort(key=lambda r: -r[1])
    return rows


# ---------------------------------------------------------------------------
# Tables and graphs for the GUI (issue #3): 2 tables + 2 graphs
# ---------------------------------------------------------------------------
def table_bill_ranking(metrics, top=10):
    ranked = sorted(metrics.values(), key=lambda m: -m.annual_bill)[:top]
    return {
        "title": f"Top {top} states by residential electricity bill",
        "columns": ["Rank", "State", "Annual bill ($)", "Price ($/MWh)", "Customers"],
        "rows": [
            [i + 1, m.state, round(m.annual_bill), round(m.price_per_mwh, 1), int(m.customers)]
            for i, m in enumerate(ranked)
        ],
    }


def table_roi_ranking(options, top=10):
    ranked = roi_ranking(options)[:top]
    return {
        "title": f"Top {top} states by investment ROI",
        "columns": ["Rank", "State", "ROI per $ (best)", "Invest at best ROI ($M)",
                    "Profit there ($M)", "Efficient limit ($M)"],
        "rows": [
            [i + 1, s, round(roi, 2), inv, round(profit, 1), limit]
            for i, (s, roi, inv, profit, limit) in enumerate(ranked)
        ],
    }


def graph_bill_by_state(metrics, top=15):
    ranked = sorted(metrics.values(), key=lambda m: -m.annual_bill)[:top]
    return {
        "title": f"Annual residential bill, top {top} states",
        "kind": "bar",
        "x_label": "State",
        "y_label": "Annual bill per customer ($)",
        "x": [m.state for m in ranked],
        "y": np.array([m.annual_bill for m in ranked]),
    }


def graph_diminishing_returns(options, state):
    opts = options[state]
    return {
        "title": f"{state}: profit vs. investment",
        "kind": "line",
        "x_label": "Investment ($M)",
        "y_label": "Net profit over horizon ($M)",
        "x": np.array([c for c, _ in opts]),
        "y": np.array([p for _, p in opts]),
    }


def build_all(path):
    metrics = state_metrics(load_rows(path))
    options = build_options(metrics)
    best_state = roi_ranking(options)[0][0]
    return {
        "metrics": metrics,
        "options": options,
        "tables": [table_bill_ranking(metrics), table_roi_ranking(options)],
        "graphs": [graph_bill_by_state(metrics), graph_diminishing_returns(options, best_state)],
    }
