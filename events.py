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
        results[-5:].plot.bar(x="State", y=columns, ax=axiser)

        for container in axiser.containers:
            axiser.bar_label(container, fmt="%.3f")

        canvaser = FigureCanvasTkAgg(figurer, master=frame_graph)
        canvaser.draw()
        canvaser.get_tk_widget().pack()
    if event.widget.select() == ".!notebook.results_table":
        frame_alg = event.widget.nametowidget(".!notebook.algorithm")
        results = frame_alg.results

        frame_table = event.widget.nametowidget(".!notebook.results_table")

        # Create a canvas, a scrollbar for the canvas, link them together, and then create an inner view bound to the canvas for the table.
        # This allows the table to have vertical scrolling, otherwise there wouldn't be enough room for all the rows.
        canvas = tk.Canvas(frame_table)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.config(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind(
            "<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        for i in range(results.shape[0] + 1):
            for j in range(results.shape[1] + 1):
                if i == 0 and j == 0:
                    continue
                if i == 0:
                    labeler = tk.Entry(
                        inner_frame, width=20, fg="black", font=("Arial", 16, "bold")
                    )
                    labeler.grid(row=i, column=j)
                    labeler.insert(tk.END, results.columns[j - 1])
                    continue
                if j == 0:
                    labeler = tk.Entry(
                        inner_frame, width=20, fg="black", font=("Arial", 16, "bold")
                    )
                    labeler.grid(row=i, column=j)
                    labeler.insert(tk.END, f"{i}")
                    continue
                enterer = tk.Entry(
                    inner_frame, width=20, fg="black", font=("Arial", 16, "bold")
                )
                enterer.grid(row=i, column=j)
                enterer.insert(tk.END, results.iat[i - 1, j - 1])
