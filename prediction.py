
"""
@Author - Adam Pinkos
@File  - prediction.py
@Date  - 11/29/2025
@Brief - Predict matchup scores using the 3 data files
"""

import math
from typing import Dict, Any

import pandas as pd

from file_loader import load_all_data



#  Tunable constants. These constants are not in the data, but are used in KENPOM College Basketball offical ratings.
COEF_OFFENSE   = 0.18   # ADJOE_team - ADJOE_opp
COEF_DEFENSE   = 0.14   # ADJDE_opp - ADJDE_team
COEF_BARTHAG   = 22.0   # BARTHAG_team - BARTHAG_opp
COEF_RANK      = 0.25   # opp_rank - team_rank
COEF_RATING    = 55.0   # rating_team - rating_opp

HOME_EDGE      = 3.5    # Home game advantage
MARGIN_SCALE   = 7.0





class MatchupPredictor:

    def __init__(self):
        results_df, ratings_df, adv_df = load_all_data()  # load_all_data() gives us the 3 data sets

        # store copies of the 3 dataframes inside the class
        self.results_df = results_df.copy()
        self.ratings_df = ratings_df.copy()
        self.adv_df = adv_df.copy()

        # clean  all 3 datasets
        self._prepare_results()
        self._prepare_advanced()
        self._prepare_ratings()

        # compute the average total points per game
        self.league_avg_total_points = float(self.results_df["total_points"].mean())

        # compute the average tempo for the whole league, if the dataset has ADJ_T, we use it
        if "ADJ_T" in self.adv_df.columns:
            self.league_avg_tempo = float(self.adv_df["ADJ_T"].mean())
        else:
            # if for some reason ADJ_T is missing,
            # just assume a normal D1 tempo of about 67 possessions. This is found one KENPOM College basketball Ratings
            self.league_avg_tempo = 67.0

    # Data prep
    def _prepare_results(self) -> None:

        # Work with the dataframe that has actual game results
        df = self.results_df

        # Make sure the team score column is numeric
        # turns bad values into NaN instead of crashing.
        df["teamscore"] = pd.to_numeric(df.get("teamscore"), errors = "coerce")


        # Same thing for the opponent score.
        df["oppscore"] = pd.to_numeric(df.get("oppscore"), errors = "coerce")


        # Total points scored in the game 
        # team + opponent
        df["total_points"] = df["teamscore"] + df["oppscore"]


        # Margin = points_for_team - points_for_opponent
        # Positive margin means the primary team won
        df["margin"] = df["teamscore"] - df["oppscore"]

        self.results_df = df




    def _prepare_advanced(self) -> None:
        # Work with the cbb25 that has all the advanced team stats
        df = self.adv_df

        # These columns all contain numeric values in cbb25.csv
        # loop through each one and convert it to a real number type.
        for col in ["ADJOE", "ADJDE", "BARTHAG", "ADJ_T", "SEED", "rk", "RK"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")  # If the value is missing or invalid, errors = coerce will turn it into NaN
                # instead of causing the code to crash


        # The model needs to quickly look up stats for a team by name
        if "Team" in df.columns:
            self.adv_index = df.set_index("Team")  # turn the "Team" column into the index
        else:
            self.adv_index = pd.DataFrame()

        self.adv_df = df


    
    def _prepare_ratings(self) -> None:
        # Work with the dataframe that holds team-vs-team ratings which is caa_wp_matrix_2025.csv
        df = self.ratings_df

    # Both columns contain  numeric values
    # We convert them to actual numeric types so math works correctly
        for col in ["rating_team", "rating_opponent"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors = "coerce")  # if the value is bad or missing, turn it into NaN
        self.ratings_df = df



    # 
    # Look up
    def _get_adv_features(self, team_name: str) -> Dict[str, float]:
    
        
        # Check if the team exists in the adv_index (created earlier in _prepare_advanced
        if team_name in self.adv_index.index:

            # Grab that entire row of stats
            row = self.adv_index.loc[team_name]


            # Get offensive efficiency (ADJOE)
            adjoe   = float(row.get("ADJOE", 110.0))

            # Get defensive efficiency (ADJDE)
            adjde   = float(row.get("ADJDE", 100.0))

            # BARTHAG = overall power rating (0.00 – 1.00)
            barthag = float(row.get("BARTHAG", 0.50))

            # Tempo (ADJ_T) = estimated possessions per game
            tempo   = float(row.get("ADJ_T", self.league_avg_tempo))



        # Rankings
        #   "rk" is the primary column in the file,
        #   "RK" appears in some versions of cbb25 datasets
            if not pd.isna(row.get("rk", float("nan"))):
                rank = float(row["rk"])
            elif not pd.isna(row.get("RK", float("nan"))):
                rank = float(row["RK"])
            else:
                rank = 180.0  #### Kinda AVERAGE



            # SEED (NCAA March Madness tournament projection)
            seed    = float(row.get("SEED", 16.0))


        # If the team name wasn't found at all in the advanced stats,
        # we give them generic average D1 numbers so the model doesn’t break
        #### JUST INCASE
        else:
            adjoe = 110.0
            adjde = 100.0
            barthag = 0.50
            tempo = self.league_avg_tempo
            rank = 180.0
            seed = 16.0


        # Return everything in a dictionary to the caller
        return {
            "ADJOE": adjoe,
            "ADJDE": adjde,
            "BARTHAG": barthag,
            "ADJ_T": tempo,
            "RANK": rank,
            "SEED": seed,
        }
    

    def _get_team_total_points_avg(self, team_name: str) -> float:

        df = self.results_df

        # Make a mask (filter) for all games where this team played
        # Either as "team" or "opponent"
        mask = (df["team"] == team_name) | (df["opponent"] == team_name)

        # Pull only those games
        subset = df[mask]

        # If the team has no recorded games, return NaN so the caller knows it's missing
        if subset.empty:
            return float("nan")
        
        # Compute and return the average total points in those gameess
        return float(subset["total_points"].mean())
    


    def _get_rating_diff(self, team_name: str, opponent_name: str) -> float:

        df = self.ratings_df

        # If the expected numeric columns are missing, we can't compute anything
        if "rating_team" not in df.columns or "rating_opponent" not in df.columns:
            return 0.0


        # Try to find the matchup exactly as written #   (team_name vs opponent_name)
        direct = df[(df["team"] == team_name) & (df["opponent"] == opponent_name)]

         # If this row exists in the file
        if not direct.empty:

            # rating_team is Team 1's rating
            # rating_opponent is Team 2's rating
            row = direct.iloc[0]
            return float(row["rating_team"] - row["rating_opponent"])


        # If the row wasn't stored in that order,
        # make the file has it reversed (opponent vs team)
        rev = df[(df["team"] == opponent_name) & (df["opponent"] == team_name)]
        if not rev.empty:
            row = rev.iloc[0]


            # Instead of (rating_team - rating_opponent), do -(that value) to convert it into Team1 - Team2.
            return float(-(row["rating_team"] - row["rating_opponent"]))


        ### JUST INCASE
        return 0.0

    

    