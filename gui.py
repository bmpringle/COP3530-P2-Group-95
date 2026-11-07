import os
from tkinter import ttk
import tkinter as tk
import numpy as np
currentValue = 'N/A'
#Change data format once we're certain of how to input it.
numRows = 4
numCols = 2
input = [('N/A', 'N/A'), ('N/A', 'N/A'), ('N/A', 'N/A'), ('N/A', 'N/A')]

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
    tabMaster.add(tab3, text='Analyze Results')
    #Continue setup.
    tabMaster.pack(expand=1, fill='both')
    for i in range(numRows):
        for j in range(numCols):
            enterer = tk.Entry(tab3, width=20, fg='black', font=('Arial', 16, 'bold'))
            enterer.grid(row=i, column=j)
            enterer.insert(tk.END, input[i][j])



