"""
@Author - Adam Pinkos
@File - gui.py
@Date - 11/18/2025
@Brief - Simple GUI that lets you scroll or search for a team name,
         and get a predicted output.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

CBB25_PATH = "cbb25.csv"   # <-- change path if needed


# TeamSelector 
class TeamSelector(ttk.Frame):

    def __init__(self, master, teams, title = "Team", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.all_teams = sorted(teams)
        self.filtered_teams = self.all_teams.copy()
        self.selected_team = None

        # Title label
        self.title_label = ttk.Label(
            self, text=title, font=("Times New Roman", 11, "bold")
        )
        self.title_label.pack(anchor="w", pady=(0, 2))

        # Search box
        search_frame = ttk.Frame(self)
        search_frame.pack(fill = "x", pady=(0, 4))

        ttk.Label(search_frame, text = "Search:").pack(side = "left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable = self.search_var)
        self.search_entry.pack(side = "left", fill = "x", expand = True, padx = (5, 0))

        self.search_var.trace_add("write", self.update_filter)

        # Listbox
        self.listbox = tk.Listbox(self, height = 12)
        self.listbox.pack(fill = "both", expand = True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Load teams into listbox
        self.update_listbox()

    def update_filter(self, *args):
        query = self.search_var.get().lower()
        self.filtered_teams = [
            t for t in self.all_teams if query in t.lower()
        ]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for t in self.filtered_teams:
            self.listbox.insert(tk.END, t)

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        self.selected_team = self.filtered_teams[index]

    def get_team(self):
        return self.selected_team






# main
class PredictionApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("College Hoops Predictor")
        self.geometry("750x450")



        # load teams
        try:
            df = pd.read_csv(CBB25_PATH)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {CBB25_PATH}.")
            raise SystemExit


        # Adjust column 
        if "team" in df.columns:
            self.teams = sorted(df["team"].unique())
        elif "Team" in df.columns:
            self.teams = sorted(df["Team"].unique())
        else:
            messagebox.showerror("Error", "CSV missing 'team' column.")
            raise SystemExit

        self.create_widgets()





    def create_widgets(self):

        # Header
        header = ttk.Label(
            self,
            text = "College Hoops Predictor",
            font = ("Times New Roman", 20, "bold"),
        )
        header.pack(pady = 10)



        # Team selectors frame
        selector_frame = ttk.Frame(self)
        selector_frame.pack(fill = "x", expand = True, padx = 15)


        # Left Team 1
        self.team1_selector = TeamSelector(selector_frame, self.teams, "Team 1")
        self.team1_selector.pack(side = "left", fill = "both", expand = True, padx = 10)

        # Right Team 2
        self.team2_selector = TeamSelector(selector_frame, self.teams, "Team 2")
        self.team2_selector.pack(side = "left", fill = "both", expand = True, padx = 10)

        # Predict button
        predict_btn = ttk.Button(self, text = "Predict Winner", command = self.predict)
        predict_btn.pack(pady = 15)

        # Result label
        self.result_label = ttk.Label(
            self, text = "Pick two teams to start.", font  = ("Times New Roman", 14)
        )
        self.result_label.pack()

        # Footer: teams loaded
        count_label = ttk.Label(self, text=f"Teams loaded: {len(self.teams)}")
        count_label.pack(pady = 5)

   
    def predict(self):
        team1 = self.team1_selector.get_team()
        team2 = self.team2_selector.get_team()

        if not team1 or not team2:
            messagebox.showwarning("Missing Teams", "Please select two teams.")
            return

        if team1 == team2:
            messagebox.showwarning("Error", "Pick two different teams.")
            return
        






        # Placeholder prediction logic
        winner = team1 if len(team1) > len(team2) else team2

        self.result_label.config(
            text=f"Predicted Winner: {winner}",
            foreground="blue"
        )




# Run
if __name__ == "__main__":
    app = PredictionApp()
    app.mainloop()
