import tkinter as tk
from tkinter import filedialog, ttk

import pandas
from algorithms import historical_roi_algorithm


def browse_for_dataset(notebook: ttk.Notebook, label: tk.Label):
    file = filedialog.askopenfilename(
        title="Select Dataset", filetypes=[("CSV files", "*.csv")]
    )
    if file:
        label.config(text=file)
        notebook.tab(".!notebook.algorithm", state="normal")
        notebook.tab(".!notebook.results_table", state="disabled")
        notebook.tab(".!notebook.results_graph", state="disabled")
    else:
        label.config(text="Dataset Not Selected")
        notebook.tab(".!notebook.algorithm", state="disabled")
        notebook.tab(".!notebook.results_table", state="disabled")
        notebook.tab(".!notebook.results_graph", state="disabled")


def run_selected_algorithm(notebook, listbox):
    if len(listbox.curselection()) == 0:
        return  # TODO: Throw msg that we need to select an alg.

    selected_algorithm = listbox.get(listbox.curselection()[0])

    label = notebook.nametowidget(".!notebook.dataset.dataset_path")

    path = label.cget("text")

    data = None
    try:
        data = pandas.read_csv(path)
    except:
        return  # TODO: Throw msg that dataset could not be loaded.

    results = None
    if selected_algorithm == "Historical ROI Algorithm":
        results = historical_roi_algorithm(data)

    if results == None:
        return  # TODO: Throw msg that algorithm failed.

    # TODO: set results to be displayed in tabs
    notebook.tab(".!notebook.results_table", state="normal")
    notebook.tab(".!notebook.results_graph", state="normal")
