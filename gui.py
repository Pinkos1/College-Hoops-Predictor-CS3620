
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






    def create_widgets(self):

        # Title
        title_label = ttk.Label(
            self,
            text = "College Basketball Matchup Predictor",
            font = ("Times New Roman", 14, "bold")
        )
        title_label.pack(pady = 15)


        # Dropdown area
        form_frame = ttk.Frame(self)
        form_frame.pack(pady = 15)



        # First team dropdown
        team_a_label = ttk.Label(form_frame, text = "Pick a team:")
        team_a_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "e")

        self.team_a_var = tk.StringVar()
        self.team_a_combo = ttk.Combobox(
            form_frame,
            textvariable=self.team_a_var,
            values=TEAMS,
            state = "readonly",
            width=30
        )
        self.team_a_combo.grid(row=0, column=1, padx=5, pady=5)
        self.team_a_combo.current(0)




        # Second team dropdown 
        team_b_label = ttk.Label(form_frame, text="Select the opponent and generate predicted outcome:")
        team_b_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "e")

        self.team_b_var = tk.StringVar()
        self.team_b_combo = ttk.Combobox(
            form_frame,
            textvariable=self.team_b_var,
            values=TEAMS,
            state = "readonly",
            width = 30
        )
        self.team_b_combo.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.team_b_combo.current(1)

        # Predict button
        predict_button = ttk.Button(
            self,
            text = "Predict Game",
            command = self.on_predict_click
        )
        predict_button.pack(pady = 15)

        # Output label
        self.result_label = ttk.Label(
            self,
            text = "Choose two teams to begin.",
            font = ("Arial", 10)
        )
        self.result_label.pack(pady = 5)

    def on_predict_click(self):
        team_a = self.team_a_var.get()
        team_b = self.team_b_var.get()

        if team_a == team_b:
            messagebox.showwarning("Invalid Matchup", "Please select two different teams.")
            return

        # Random logic for now
        predicted_winner = team_a
        score_a = 75
        score_b = 68

        result_text = (
            f"Predicted winner: {predicted_winner}\n"
            f"Projected score: {team_a} {score_a} - {team_b} {score_b}"
        )

        self.result_label.config(text=result_text)
        messagebox.showinfo("Prediction", result_text)


if __name__ == "__main__":
    app = PredictionApp()
    app.mainloop()
