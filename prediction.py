
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


    

    