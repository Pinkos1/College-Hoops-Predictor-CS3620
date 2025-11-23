

"""
@Author - Adam Pinkos
@File - file_loader.py
@Date - 11/23/2025
@Brief - Simple file where I can upload all 3 datasets
"""


import pandas as pd

# Paths to your uploaded files
PATH_RESULTS = "/mnt/data/2025_cbb_results (1).csv"
PATH_RATING = "/mnt/data/ncaa_wp_matrix_2025 (1).csv"
PATH_ADVANCED = "/mnt/data/cbb25 (1).csv"

def load_all_data():
    """Load all three datasets and return as dataframes."""
    results = pd.read_csv(PATH_RESULTS)
    ratings = pd.read_csv(PATH_RATING)
    adv = pd.read_csv(PATH_ADVANCED)

    return results, ratings, adv
