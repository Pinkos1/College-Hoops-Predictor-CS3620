

"""
@Author - Adam Pinkos
@File - gui.py
@Date - 11/18/2025
@Brief - Simple GUI that lets you pick teams and get a prediction score
"""

import tkinter as tk
from tkinter import ttk, messagebox

from team_logic import load_team_list  


class TeamSelector(ttk.Frame):

    def __init__(self, master, teams, title="Team", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.all_teams = sorted(teams)
        self.filtered_teams = self.all_teams.copy()
        self.selected_team = None

        # Title label
        self.title_label = ttk.Label(self, text=title, font=("Times New Roman", 11, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 2))

        # Search label + entry
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=(0, 4))

        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=(4, 0), fill="x", expand=True)

        # Bind typing to update the list (no extra click needed)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Listbox with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, height=12, exportselection=False)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Populate the listbox
        self.update_listbox()

        # When user clicks an item, update selected team
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Also allow double-click / Enter to quickly choose
        self.listbox.bind("<Double-Button-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_select)

        # Selected label
        self.selected_var = tk.StringVar(value="Selected: (none)")
        self.selected_label = ttk.Label(self, textvariable=self.selected_var, font=("Arial", 9, "italic"))
        self.selected_label.pack(anchor="w", pady=(4, 0))

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for team in self.filtered_teams:
            self.listbox.insert(tk.END, team)

    def on_search(self, event=None):
        """Filter the list of teams based on what's typed."""
        query = self.search_var.get().strip().lower()
        if not query:
            self.filtered_teams = self.all_teams.copy()
        else:
            self.filtered_teams = [t for t in self.all_teams if query in t.lower()]
        self.update_listbox()

    def on_select(self, event=None):
        """Handle selection from the listbox."""
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if 0 <= index < len(self.filtered_teams):
            self.selected_team = self.filtered_teams[index]
            self.selected_var.set(f"Selected: {self.selected_team}")

    def get_selected_team(self):
        return self.selected_team


class PredictionApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load team list using external logic
        try:
            self.teams = load_team_list()
        except Exception as e:
            messagebox.showerror(
                "Error Loading Teams",
                f"Could not load team list.\n\n{e}\n\nUsing fallback teams."
            )
            self.teams = ["Alabama", "Akron", "Duke", "Gonzaga", "Kansas"]

        # Window setup
        self.title("College Basketball Matchup Predictor")
        self.geometry("700x450")
        self.resizable(True, True)

        # Build GUI
        self.create_widgets()

  




    def create_widgets(self):
        # Title
        ttk.Label(
            self,
            text="College Basketball Matchup Predictor",
            font=("Times New Roman", 16, "bold")
        ).pack(pady=15)

        # Info about team count
        ttk.Label(
            self,
            text=f"Teams loaded: {len(self.teams)}",
            font=("Arial", 9)
        ).pack(pady=(0, 10))

        # Main frame for selectors
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Two side-by-side selectors
        self.selector_a = TeamSelector(main_frame, self.teams, title="Team A")
        self.selector_a.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.selector_b = TeamSelector(main_frame, self.teams, title="Team B (Opponent)")
        self.selector_b.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Predict button
        ttk.Button(
            self,
            text="Predict Game",
            command=self.on_predict_click
        ).pack(pady=10)

        # Output label
        self.result_label = ttk.Label(
            self,
            text="Choose two teams to begin.",
            font=("Arial", 10),
            justify="center"
        )
        self.result_label.pack(pady=5)




    # Prediction Logic (placeholder for now)
    def on_predict_click(self):
        team_a = self.selector_a.get_selected_team()
        team_b = self.selector_b.get_selected_team()

        if not team_a or not team_b:
            messagebox.showwarning("Missing Choice", "Please select both teams.")
            return

        if team_a == team_b:
            messagebox.showwarning("Invalid Matchup", "Pick two different schools.")
            return

        # Simple placeholder prediction for now
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
