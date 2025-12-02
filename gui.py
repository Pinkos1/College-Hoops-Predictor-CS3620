"""
@Author - Adam Pinkos
@File - gui.py
@Date - 11/18/2025
@Brief - Simple GUI that lets you scroll or search for a team name,
         and get a predicted output (placeholder). Uses team_logic.py
         and file_loader.py for data loading.
"""




import tkinter as tk
from tkinter import ttk, messagebox

from team_logic import load_team_list
from file_loader import load_all_data




# This picks a team
class TeamSelector(ttk.Frame):

    def __init__(self, master, teams, title = "Team", *args, **kwargs):

        # call parent constructor
        ttk.Frame.__init__(self, master, *args, **kwargs)

        # store all the teams
        self.all_teams = sorted(teams)

        # show list
        self.filtered_teams = self.all_teams[:]

        # hold team
        self.selected_team = None


        # label  "Team 1" or "Team 2"
        self.title_label = ttk.Label(
            self,
            text = title,
            font = ("Times New Roman", 11, "bold")
        )
        self.title_label.pack(anchor="w", pady = (0, 2))





        # frame for the search label and box
        search_frame = ttk.Frame(self)
        search_frame.pack(fill = "x", pady = (0, 4))


        search_label = ttk.Label(search_frame, text = "Search:")
        search_label.pack(side = "left")



        # text variable and entry box for typing search text
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side = "left", fill = "x", expand = True, padx = (5, 0))



        self.search_var.trace_add("write", self.update_filter)  # when the text changes, update the list



        # listbox that shows the teams
        self.listbox = tk.Listbox(self, height  = 12)
        self.listbox.pack(fill = "both", expand = True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)





        # put the teams in the listbox
        self.update_listbox()

    def update_filter(self, *args):
        # get whatever the user typed
        query = self.search_var.get().lower()



        # make a new list with only teams that contain the query
        new_list = []
        for t in self.all_teams:
            if query in t.lower():
                new_list.append(t)

        self.filtered_teams = new_list

        # refresh the listbox
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END) # clear out the listbox


        # add teams one by one
        for t in self.filtered_teams:
            self.listbox.insert(tk.END, t)

    def on_select(self, event):
        
        if not self.listbox.curselection(): # if nothing is selected, do nothing
            return

        # get the index
        index = self.listbox.curselection()[0]
        self.selected_team = self.filtered_teams[index] # store the selected team



    def get_team(self):
        return self.selected_team  # just give back the selected team 


# main window class for the app
class PredictionApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self) # init tk.Tk


        self.title("College Hoops Predictor")
        self.geometry("750x450")

        # try to load the teams using the other file
        try:
            self.teams = load_team_list()
        except Exception as e:


            # if this fails, pop an error and close the window
            messagebox.showerror(
                "Error loading team list",
                "Could not load team list:\n" + str(e)
            )
            self.destroy()
            return
        



        # try to load the other dataframes too
        try:
            data = load_all_data()
            self.results_df = data[0] # unpack the tuple
            self.ratings_df = data[1]
            self.adv_df = data[2]
        except Exception as e:
            print("Warning: could not load all model datasets:", e) # if this fails, just print something to console
            self.results_df = None
            self.ratings_df = None
            self.adv_df = None

        # after data is ready, set up all the widgets
        self.create_widgets()



    def create_widgets(self):
        header = ttk.Label( # header label at the top
            self,
            text = "College Hoops Predictor",
            font = ("Times New Roman", 20, "bold")
        )
        header.pack(pady=10)




        # frame that holds both team selectors side by side
        selector_frame = ttk.Frame(self)
        selector_frame.pack(fill = "x", expand = True, padx = 15)



        # left side team 1 
        self.team1_selector = TeamSelector(selector_frame, self.teams, "Team 1")
        self.team1_selector.pack(side = "left", fill = "both", expand = True, padx = 10)



        # right side eam 2 
        self.team2_selector = TeamSelector(selector_frame, self.teams, "Team 2")
        self.team2_selector.pack(side = "left", fill = "both", expand = True, padx = 10)



        # button to run the prediction
        self.predict_button = ttk.Button(
            self,
            text = "Predict Winner",
            command=self.predict
        )
        self.predict_button.pack(pady = 15)



        # label where we show the result text
        self.result_label = ttk.Label(
            self,
            text = "Pick two teams to start.",
            font = ("Times New Roman", 14)
        )
        self.result_label.pack()



        # label at the bottom that shows how many teams we loaded
        teams_loaded_text = "Teams loaded: " + str(len(self.teams))
        self.count_label = ttk.Label(self, text = teams_loaded_text)
        self.count_label.pack(pady = 5)
 
    def predict(self):
        team1 = self.team1_selector.get_team()  # get the two teams from the selectors
        team2 = self.team2_selector.get_team()

        # if either team is not chosen, show a warning
        if team1 is None or team2 is None:
            messagebox.showwarning("Missing Teams", "Please select two teams.")
            return


        # if they are the same team, that's not allowed
        if team1 == team2:
            messagebox.showwarning("Error", "Pick two different teams.")
            return
        



        # right now this is just fake logic
        # whichever name is longer wins
        if len(team1) > len(team2):
            winner = team1
        else:
            winner = team2



        # change the label text to show the winner
        self.result_label.config(
            text = "Predicted Winner: " + winner,
            foreground="blue"
        )


# run
if __name__ == "__main__":
    app = PredictionApp()
    app.mainloop()
