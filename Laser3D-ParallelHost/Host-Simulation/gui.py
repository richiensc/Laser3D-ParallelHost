# Host-Simulation/gui.py
import tkinter as tk
from src.gui_app import LaserScannerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = LaserScannerGUI(root)
    root.mainloop()