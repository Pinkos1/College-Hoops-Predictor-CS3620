

"""
@Author - Adam Pinkos
@File - gui.py
@Date - 11/27/2025
@Brief - GUI w
"""

import tkinter as tk
from tkinter import ttk, messagebox

from team_logic import load_team_list
from prediction import MatchupPredictor
from prediction_explainer import build_breakdown_text


# Team selector 
class TeamSelector(ttk.Frame):

    def __init__(self, master, teams, title = "Team", *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)

        self.all_teams = sorted(teams)
        self.filtered_teams = self.all_teams[:]
        self.selected_team = None

        self.title_label = ttk.Label(
            self, text=title, font=("Times New Roman", 11, "bold")
        )
        self.title_label.pack(anchor = "w", pady = (0, 2))

        search_frame = ttk.Frame(self)
        search_frame.pack(fill = "x", pady = (0, 4))

        ttk.Label(search_frame, text = "Search:").pack(side = "left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable = self.search_var)
        self.search_entry.pack(side = "left", fill = "x", expand = True, padx = (5, 0))
        self.search_var.trace_add("write", self.update_filter)

        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill = "both", expand = True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.update_listbox()

    def update_filter(self, *args):
        q = self.search_var.get().lower()
        self.filtered_teams = [t for t in self.all_teams if q in t.lower()]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for t in self.filtered_teams:
            self.listbox.insert(tk.END, t)

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        idx = self.listbox.curselection()[0]
        self.selected_team = self.filtered_teams[idx]

    def get_team(self):
        return self.selected_team


# Main 
# Prediction portion
class PredictionApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("College Hoops Predictor")
        self.geometry("900x650")

        try:
            self.teams = load_team_list()
        except Exception as e:
            messagebox.showerror("Error loading teams", str(e))
            self.destroy()
            return

        try:
            self.predictor = MatchupPredictor()
        except Exception as e:
            messagebox.showerror("Error loading prediction model", str(e))
            self.destroy()
            return

        self.create_widgets()



# small parts that are in the gui
    def create_widgets(self):

        # Notebook with 2 tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill = "both", expand = True)
 
        # Tab 1 Predictor
        self.predictor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.predictor_tab, text = "Predictor")

        # Tab 2 Stat Glossary
        self.glossary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.glossary_tab, text = "Stat Glossary")

        # Build contents of each tab
        self._build_predictor_tab()
        self._build_glossary_tab()

        

    # predictor tab
    def _build_predictor_tab(self):
        header = ttk.Label(self.predictor_tab,
                           text="College Hoops Predictor",
                           font=("Times New Roman", 20, "bold"))
        header.pack(pady=10)

        selector_frame = ttk.Frame(self.predictor_tab)
        selector_frame.pack(fill = "x", expand = False, padx = 15)

        self.team1_selector = TeamSelector(selector_frame, self.teams, "Team 1")
        self.team1_selector.pack(side = "left", fill = "both", expand = True, padx = 10)

        self.team2_selector = TeamSelector(selector_frame, self.teams, "Team 2")
        self.team2_selector.pack(side = "left", fill = "both", expand = True, padx = 10)

        self.predict_button = ttk.Button(self.predictor_tab,
                                         text = "Predict Winner",
                                         command = self.predict)
        self.predict_button.pack(pady=15)





        # Scroll wheel and part that shows the stats
        scroll_frame = ttk.Frame(self.predictor_tab)
        scroll_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)

        self.canvas = tk.Canvas(scroll_frame)
        self.canvas.pack(side = "left", fill = "both", expand = True)

        scrollbar = ttk.Scrollbar(scroll_frame, orient = "vertical",
                                  command=self.canvas.yview)
        scrollbar.pack(side = "right", fill = "y")

        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        )



        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window = self.inner_frame, anchor = "nw")

        self.result_label = ttk.Label(self.inner_frame,
                                      text="Pick two teams to start.",
                                      font=("Times New Roman", 14))
        self.result_label.pack(anchor = "w", pady = (0, 10))

        self.breakdown_label = ttk.Label(self.inner_frame,
                                         text = "",
                                         font = ("Courier New", 10),
                                         justify = "left")
        self.breakdown_label.pack(anchor = "w")

        teams_loaded_text = f"Teams loaded: {len(self.teams)}"
        self.count_label = ttk.Label(self.predictor_tab, text = teams_loaded_text)
        self.count_label.pack(pady = 5)






    # The glossary tab that shows and describes what the data means
    def _build_glossary_tab(self):


        # use text to allow multi-line formatting
        txt = tk.Text(self.glossary_tab, wrap = "word", height = 25)
        txt.pack(fill = "both", expand = True, padx = 10, pady = 10)

        glossary = """
STAT GLOSSARY  (Team 1 is the left side in the predictor tab)

Rating stats used in the model
------------------------------
ADJOE      = Adjusted offensive efficiency.
             Estimated points scored per 100 possessions vs an average D1 defense.
             Higher ADJOE  → better offense.

ADJDE      = Adjusted defensive efficiency.
             Estimated points allowed per 100 possessions vs an average D1 offense.
             Lower ADJDE  → better defense.

BARTHAG    = Power rating (Barthag win probability vs an average D1 team).
             Value between 0 and 1.
             Higher BARTHAG → stronger overall team.

RANK       = Overall ranking number (1 is best).
             Lower RANK    → stronger team.
             The model uses (opponent_rank - team_rank), so a big positive number
             favors Team 1.

rating_diff = rating_team - rating_opponent from ncaa_wp_matrix_2025.csv.
              Positive rating_diff → Team 1 is rated higher.

tempo      = ADJ_T in cbb25.csv.
             Estimated possessions per game.
             Higher tempo → more total points.

Model difference features (Team 1 - Team 2)
------------------------------------------
offense_diff = ADJOE_team1 - ADJOE_team2
               Positive → Team 1 has better offense.

defense_diff = ADJDE_team2 - ADJDE_team1
               Positive → Team 1 has better defense (allows fewer points).

barthag_diff = BARTHAG_team1 - BARTHAG_team2
               Positive → Team 1 stronger power rating.

rank_diff    = RANK_team2 - RANK_team1
               Positive → Team 1 has better (lower) rank.

rating_diff  = rating_team1 - rating_team2
               Positive → Team 1 higher rating in ncaa_wp_matrix_2025.csv.

Margin components (points, + favors Team 1)
-------------------------------------------
margin_off_def = points added from offense_diff + defense_diff
margin_barth   = points added from barthag_diff
margin_rank    = points added from rank_diff
margin_rating  = points added from rating_diff
location_edge  = home/away points (H = +3.5, V = -3.5, N = 0)

Final numbers
-------------
raw_margin        = sum of all margin components (Team 1 minus Team 2)
final_margin_cap  = raw_margin after capping at ±30

baseline_total    = base total points from league + team scoring averages
tempo_total       = baseline_total adjusted by average tempo of both teams
final_total_pts   = tempo_total after clamping to a reasonable range

Win probability (not shown here)
--------------------------------
The model converts final_margin_cap into a win probability using
a logistic curve. Larger positive margin → higher win chance for Team 1.
"""

        txt.insert("1.0", glossary)
        txt.configure(state = "disabled")  # make it read only



    # predict
    def predict(self):
        t1 = self.team1_selector.get_team()
        t2 = self.team2_selector.get_team()

        if not t1 or not t2:
            messagebox.showwarning("Missing Teams", "Please select two teams.")
            return

        if t1 == t2:
            messagebox.showwarning("Error", "Pick two different teams.")
            return

        try:
            pred = self.predictor.predict_matchup(t1, t2, location = "N")
        except Exception as e:
            messagebox.showerror("Prediction error", str(e))
            return

        score_text = f"{pred['team']} {pred['team_score']} - {pred['opponent_score']} {pred['opponent']}"
        prob_text = f"(Win prob {pred['win_prob']*100:.1f}% for {pred['team']})"

        self.result_label.config(text = score_text + "  " + prob_text,
                                 foreground = "blue")

        breakdown_text = build_breakdown_text(pred)
        self.breakdown_label.config(text=breakdown_text)



if __name__ == "__main__":
    app = PredictionApp()
    app.mainloop()
