from tkinter import simpledialog

import numpy as np
import pandas as pd


def historical_roi_algorithm(data) -> pd.DataFrame | None:
    investment_budget = simpledialog.askfloat(
        "Investment Budget",
        "What is your investment budget for generating power? (In USD)",
    )
    cost_to_build = simpledialog.askfloat(
        "Cost Per MWh",
        "What is the cost for you to build generating capcity per MWh? (In USD / MWh)",
    )
    cost_to_generate = simpledialog.askfloat(
        "Cost to Generate", "At what cost will you produce power? (In USD / MWh)"
    )

    if not investment_budget or not cost_to_generate or not cost_to_build:
        return None

    if cost_to_generate <= 0 or investment_budget <= 0 or cost_to_build <= 0:
        return None

    state_list = data["Utility.State"].unique()

    state_list = state_list.dropna()

    electricity_sold_list = []
    for state in state_list:
        electricity_sold_list.append(
            data[data["Utility.State"] == state]["Uses.Total"].sum()
        )
    sales_per_state = pd.DataFrame([electricity_sold_list], columns=state_list)

    electricity_price_list = []
    for state in state_list:
        revenue = (
            data[data["Utility.State"] == state]["Retail.Total.Revenue"] * 1000
        )  # In thousands of USD.
        sales = data[data["Utility.State"] == state]["Retail.Total.Sales"]
        electricity_price_list.append((revenue / sales).mean())
    avg_price_per_state = pd.DataFrame([electricity_price_list], columns=state_list)

    total_capacity = investment_budget / cost_to_build

    margin_per_state = avg_price_per_state - cost_to_generate
    profit_per_state = margin_per_state * total_capacity
    market_percent = total_capacity / (sales_per_state + total_capacity) * 100
    roi_per_year = profit_per_state / investment_budget * 100
    years_to_payback = investment_budget / profit_per_state

    results_names = [
        "Margin",
        "Market %",
        "ROI",
        "Years to Payback on Investment",
    ]

    results = pd.concat(
        [
            df.T
            for df in [
                margin_per_state,
                market_percent,
                roi_per_year,
                years_to_payback,
            ]
        ],
        axis=1,
    )
    results.columns = results_names
    results["State"] = state_list
    return results
