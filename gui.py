import os
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
currentValue = 'N/A'

#Change data format once we're certain of how to input it.

#For table.
numRows = 4
numCols = 2
labelsSide = ['element1', 'element2', 'element3', 'element4']
labelsTop = ['element1', 'element2']
input = [('N/A', 'N/A'), ('N/A', 'N/A'), ('N/A', 'N/A'), ('N/A', 'N/A')]
#For bar graph.
categories = ['a1', 'a2', 'a3', 'a4', 'a5', 'e6', 'e5,', 'e4']
values = {
    'Type 1': (10, 20, 50, 60, 60, 60, 60, 50),
    'Type 2': (5, 30, 60, 50, 50, 50, 50, 50),
    'Type 3': (2, 56, 43, 40, 40, 40, 40, 40),
}
title = 'Example Title'

algorithms = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3', 'Algorithm 4']
def setup_gui_and_events(window: tk):
    #Creates the main 'master' window.
    window.title("Menu") #TBD - Make a better name for this.
    tabMaster = ttk.Notebook(window)
    #Sets up our tabs.
    #First tab.
    tab1 = tk.Frame(tabMaster)
    tabMaster.add(tab1, text='Select Dataset')
    tk.Label(tab1, text="Current Filepath: ").grid(row=0, column=0)
    currentPathVar = tk.StringVar()
    currentPathVar.set(os.path.expanduser('~'))
    currentPath = (tk.Entry(tab1, textvariable=currentPathVar))
    currentPath.grid(row=0, column=1)
    #Second tab.
    tab2 = tk.Frame(tabMaster)
    tabMaster.add(tab2, text='Select Algorithm')
    header = tk.Label(tab2, text="Available Algorithms", anchor="w")
    header.pack(fill=tk.X, padx=25, pady=(10, 0))
    scroller = tk.Scrollbar(tab2)
    scroller.pack(side=tk.RIGHT, fill=tk.Y)
    lister = tk.Listbox(tab2, yscrollcommand=scroller.set)
    for algorithm in algorithms:
        lister.insert(tk.END, algorithm)
    lister.pack(side=tk.LEFT, fill=tk.BOTH)
    scroller.config(command=lister.yview)
    #Third tab.
    tab3 = tk.Frame(tabMaster)
    tabMaster.add(tab3, text='Results As Table')
    for i in range(numRows + 1):
        for j in range(numCols + 1):
            if i == 0 and j == 0:
                continue
            if i == 0:
                labeler = tk.Entry(tab3, width=20, fg='black', font=('Arial', 16, 'bold'))
                labeler.grid(row=i, column=j)
                labeler.insert(tk.END, labelsTop[j-1])
                continue
            if j == 0:
                labeler = tk.Entry(tab3, width=20, fg='black', font=('Arial', 16, 'bold'))
                labeler.grid(row=i, column=j)
                labeler.insert(tk.END, labelsSide[i-1])
                continue
            enterer = tk.Entry(tab3, width=20, fg='black', font=('Arial', 16, 'bold'))
            enterer.grid(row=i, column=j)
            enterer.insert(tk.END, input[i - 1][j - 1])
    #Fourth tab.
    tab4 = tk.Frame(tabMaster)
    tabMaster.add(tab4, text='Results As Graph')

    colors = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE']
    figurer, axiser = plt.subplots(layout='tight')
    figurer.dpi = 100;
    figurer.figsize = (20, 20)
    res = axiser.grouped_bar(values, tick_labels=categories, group_spacing=1)
    for container in res.bar_containers:
        axiser.bar_label(container, padding=3)

    # Add some text for labels, title, etc.
    axiser.set_ylabel('Dollars, USD')
    axiser.set_title(title)
    axiser.legend(loc='upper left', ncols=3)
    canvaser = FigureCanvasTkAgg(figurer, master=tab4)
    widgeter = canvaser.get_tk_widget()
    widgeter.grid(column=0, row=numRows+1)
    canvaser.draw()
    #Continue setup.
    tabMaster.pack(expand=1, fill='both')



