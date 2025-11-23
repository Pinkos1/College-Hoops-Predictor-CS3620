"""
@Author - Adam Pinkos
@File - team_logic.py
@Date - 11/18/2025
@Brief - Logic for loading team data for the College Hoops predictor GUI.
"""

import pandas as pd

# Path to your cbb25.csv file
CBB25_PATH = "C:/Users/a13pi/Downloads/cbb25.csv"


def load_team_list():
    """
    Load and return a sorted list of team names from cbb25.csv.

    Tries several common column names to find the team column.
    """
    df = pd.read_csv(CBB25_PATH)

    # Try to determine team column automatically
    possible_cols = ["Team", "TEAM", "team", "TeamName", "School"]

    team_col = None
    for col in possible_cols:
        if col in df.columns:
            team_col = col
            break

    if not team_col:
        raise ValueError("No recognized team column name in cbb25.csv")

    teams = sorted(df[team_col].dropna().unique().tolist())
    return teams
