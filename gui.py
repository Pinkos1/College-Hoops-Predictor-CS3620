
"""
@Author - Adam Pinkos
@File - gui.py
@Date - 11/18/2025
@Brief - Simple gui that you can select two colleges and receive a predicted score outcome. Even if the college never play each other

"""

import tkinter as tk
from tkinter import ttk, messagebox

# Picked random colleges as placeholers before I insert data into the program 
TEAMS = [
    "Alabama", "Akron", "Gonzaga", "Duke",
    "Kansas", "Kentucky", "Purdue", "UConn"
]


class PredictionApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window size
        self.title("College Basketball Matchup Predictor")
        self.geometry("450x450")
        self.resizable(True, True)

        # Build GUI 
        self.create_widgets()