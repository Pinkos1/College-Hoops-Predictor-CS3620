
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


