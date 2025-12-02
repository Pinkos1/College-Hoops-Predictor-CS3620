"""
@Author - Adam Pinkos
@File - team_logic.py
@Date - 11/18/2025
@Brief - Logic for loading team data for the College Hoops predictor GUI.
"""

import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CBB25_PATH = os.path.join(BASE_DIR, "cbb25.csv")


def load_team_list():
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
