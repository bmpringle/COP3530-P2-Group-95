import tkinter as tk

from gui import setup_gui_and_events


# Create the window, setup GUI and events, and call tkinter main loop.
def main():
    window = tk.Tk(
        screenName=" Project 2 - Electric Utility Optimizer",
        baseName=" Project 2 - Electric Utility Optimizer",
        className=" Project 2 - Electric Utility Optimizer",
    )
    setup_gui_and_events(window)
    window.mainloop()


# Only run main if this is the file being run.
if __name__ == "__main__":
    main()
