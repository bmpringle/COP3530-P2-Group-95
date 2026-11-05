from tkinter import ttk
import tkinter as tk

def setup_gui_and_events(window: tk):
    #Creates the main 'master' window.
    window.title("Menu") #TBD - Make a better name for this.
    tabMaster = ttk.Notebook(window)
    #Sets up our tabs.
    #First tab.
    tab1 = tk.Frame(tabMaster)
    tabMaster.add(tab1, text='Select Dataset')
    tk.Label(tab1, text="Search Dataset For: ").grid(row=0, column=0)
    entry1 = tk.Entry(tab1)
    entry1.grid(row=0, column=1)
    #Second tab.
    tab2 = tk.Frame(tabMaster)
    tabMaster.add(tab2, text='Select Algorithm')
    #Third tab.
    tab3 = tk.Frame(tabMaster)
    tabMaster.add(tab3, text='Results')
    #Continue setup.
    tabMaster.pack(expand=1, fill='both')


