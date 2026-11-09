import os
import tkinter as tk
from functools import partial
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
from events import (
    browse_for_dataset,
    on_notebook_tab_changed,
    run_selected_algorithm,
)

currentValue = "N/A"

# Change data format once we're certain of how to input it.

# For table.
numRows = 4
numCols = 2
labelsSide = ["element1", "element2", "element3", "element4"]
labelsTop = ["element1", "element2"]
input = [("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A"), ("N/A", "N/A")]


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
    frame = tk.Frame(notebook, name="results_graph")
    notebook.add(frame, text="Results (Graph)", state="disabled")


def setup_gui_and_events(window: tk.Tk):
    notebook = ttk.Notebook(window)

    setup_dataset_tab(notebook)
    setup_algorithm_tab(notebook)
    setup_table_results_tab(notebook)
    setup_graph_results_tab(notebook)

    notebook.bind("<<NotebookTabChanged>>", on_notebook_tab_changed)

    notebook.pack(expand=1, fill="both")
