import os
import tkinter as tk
from functools import partial
from tkinter import ttk

import matplotlib.pyplot as plt
from events import (
    browse_for_dataset,
    run_selected_algorithm,
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

currentValue = "N/A"

# Change data format once we're certain of how to input it.

# For table.
numRows = 4
numCols = 2
labelsSide = ["element1", "element2", "element3", "element4"]
labelsTop = ["element1", "element2"]
input = [("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A")]
# For bar graph.
categories = ["a1", "a2", "a3", "a4", "a5", "e6", "e5,", "e4"]
values = {
    "Type 1": (10, 20, 50, 60, 60, 60, 60, 50),
    "Type 2": (5, 30, 60, 50, 50, 50, 50, 50),
    "Type 3": (2, 56, 43, 40, 40, 40, 40, 40),
}
title = "Example Title"

algorithms = ["Algorithm 1", "Algorithm 2", "Algorithm 3", "Algorithm 4"]


def setup_dataset_tab(notebook: ttk.Notebook):
    # Setup dataset tab GUI.
    frame = tk.Frame(notebook, name="dataset")
    notebook.add(frame, text="Select Dataset")

    label = tk.Label(frame, name="dataset_path", text="Dataset Not Selected")
    button = tk.Button(
        frame,
        text="Choose Dataset",
        command=lambda: browse_for_dataset(notebook, label),
    )

    button.grid(row=0, column=0)
    label.grid(row=0, column=1)


def setup_algorithm_tab(notebook: ttk.Notebook):
    frame = tk.Frame(notebook, name="algorithm")
    notebook.add(frame, text="Select Algorithm", state="disabled")

    header = tk.Label(frame, text="Available Algorithms", anchor="w")

    lister = tk.Listbox(frame)

    # TODO: Insert Algorithm Names Here
    lister.insert(tk.END, "Historical ROI Algorithm")

    button = tk.Button(
        frame,
        text="Run Selected Algorithm",
        command=lambda: run_selected_algorithm(notebook, lister),
    )

    header.grid(row=0, column=0)
    lister.grid(row=1, column=0)
    button.grid(row=0, column=1)


def setup_table_results_tab(notebook: ttk.Notebook):
    tab3 = tk.Frame(notebook, name="results_table")
    notebook.add(tab3, text="Results (Table)", state="disabled")
    for i in range(numRows + 1):
        for j in range(numCols + 1):
            if i == 0 and j == 0:
                continue
            if i == 0:
                labeler = tk.Entry(
                    tab3, width=20, fg="black", font=("Arial", 16, "bold")
                )
                labeler.grid(row=i, column=j)
                labeler.insert(tk.END, labelsTop[j - 1])
                continue
            if j == 0:
                labeler = tk.Entry(
                    tab3, width=20, fg="black", font=("Arial", 16, "bold")
                )
                labeler.grid(row=i, column=j)
                labeler.insert(tk.END, labelsSide[i - 1])
                continue
            enterer = tk.Entry(tab3, width=20, fg="black", font=("Arial", 16, "bold"))
            enterer.grid(row=i, column=j)
            enterer.insert(tk.END, input[i - 1][j - 1])


def setup_graph_results_tab(notebook: ttk.Notebook):
    tab4 = tk.Frame(notebook, name="results_graph")
    notebook.add(tab4, text="Results (Graph)", state="disabled")

    colors = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE"]
    figurer, axiser = plt.subplots(layout="tight")
    figurer.dpi = 100
    figurer.figsize = (20, 20)
    res = axiser.grouped_bar(values, tick_labels=categories, group_spacing=1)
    for container in res.bar_containers:
        axiser.bar_label(container, padding=3)

    # Add some text for labels, title, etc.
    axiser.set_ylabel("Dollars, USD")
    axiser.set_title(title)
    axiser.legend(loc="upper left", ncols=3)
    canvaser = FigureCanvasTkAgg(figurer, master=tab4)
    widgeter = canvaser.get_tk_widget()
    widgeter.grid(column=0, row=numRows + 1)
    canvaser.draw()


def setup_gui_and_events(window: tk.Tk):
    notebook = ttk.Notebook(window)

    setup_dataset_tab(notebook)
    setup_algorithm_tab(notebook)
    setup_table_results_tab(notebook)
    setup_graph_results_tab(notebook)

    notebook.pack(expand=1, fill="both")
