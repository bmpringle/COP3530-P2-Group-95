import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import pandas
from algorithms import historical_roi_algorithm
from dp_algorithm import dp_budget_algorithm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        return

    selected_algorithm = listbox.get(listbox.curselection()[0])

    label = notebook.nametowidget(".!notebook.dataset.dataset_path")

    path = label.cget("text")

    data = None
    try:
        data = pandas.read_csv(path)
    except:
        messagebox.showinfo(
            title="Data Loading Failure",
            message="Could not load the dataset selected. Is this a csv file with the correct columns and rows?",
        )
        return

    results = None
    if selected_algorithm == "Historical ROI Algorithm":
        results = historical_roi_algorithm(data)
    elif selected_algorithm == "DP Budget Allocation":
        results = dp_budget_algorithm(data)

    if not isinstance(results, pandas.DataFrame):
        return

    notebook.nametowidget(".!notebook.algorithm").results = results
    notebook.tab(".!notebook.results_table", state="normal")
    notebook.tab(".!notebook.results_graph", state="normal")


def on_notebook_tab_changed(event):
    if event.widget.select() == ".!notebook.results_graph":
        frame_alg = event.widget.nametowidget(".!notebook.algorithm")
        frame_graph = event.widget.nametowidget(".!notebook.results_graph")

        results = frame_alg.results
        if "State" not in results or "ROI" not in results:
            return

        figurer, axiser = plt.subplots(layout="tight", dpi=100, figsize=(8, 5))
        axiser.set_title("Top 5 States for Investment by ROI")

        columns = list(results.columns)
        columns.remove("State")
        results = results.sort_values(by="ROI")
        results[:5].plot.bar(x="State", y=columns, ax=axiser)

        for container in axiser.containers:
            axiser.bar_label(container, fmt="%.3f")

        canvaser = FigureCanvasTkAgg(figurer, master=frame_graph)
        canvaser.draw()
        canvaser.get_tk_widget().pack()
