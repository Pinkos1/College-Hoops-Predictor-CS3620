"""
@Author - Adam Pinkos
@File - file_loader.py
@Date - 11/23/2025
@Brief - Load all 3 datasets from the project folder
"""

import os
import pandas as pd

# Directory this file lives in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exact filenames as shown in your screenshot
PATH_RESULTS  = os.path.join(BASE_DIR, "2025_cbb_results.csv")
PATH_RATING   = os.path.join(BASE_DIR, "ncaa_wp_matrix_2025.csv")
PATH_ADVANCED = os.path.join(BASE_DIR, "cbb25.csv")


def load_all_data():
    """Load all three datasets and return as dataframes."""
    results = pd.read_csv(PATH_RESULTS)
    ratings = pd.read_csv(PATH_RATING)
    adv = pd.read_csv(PATH_ADVANCED)
    return results, ratings, adv
