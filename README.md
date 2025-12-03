2024-2025 College Hoops Predictor
NCAA Division I Basketball Matchup Score Prediction System

Author: Adam Pinkos
Course: CS3620 — Advanced Database Systems
Date: Spring 2025

## Overview ##

College Hoops Predictor is a full-stack NCAA Division I basketball analytics system that allows users to:

Select any two D1 teams
Generate a predicted final score
Get a win probability
View an in-depth numeric breakdown of why the model produced that score
View an embedded stat glossary explaining every metric

This project integrates:
- A Tkinter GUI interface for matchup selection
- A custom Python prediction engine
- Fully structured SQL schema for teams, matchups, ratings, advanced stats, and model outputs

Three real NCAA datasets:
 - cbb25.csv (advanced efficiency metrics)
 - 2025_cbb_results.csv (game results + scores)
 - ncaa_wp_matrix_2025.csv (team-vs-team win probability matrix)

 The system simulates simplified versions of real basketball analytics models (KenPom-style efficiencies, tempo adjustments, power ratings, logistic win probabilities, etc.), while remaining interpretable for end users.

## How the Prediction Model Works

The core prediction logic lives in prediction.py.
The model computes a predicted margin (Team1 − Team2) using:

1. Offensive / Defensive Efficiency
From cbb25.csv:
- ADJOE — Adjusted offensive efficiency
- ADJDE — Adjusted defensive efficiency

2. Team Strength Metrics
BARTHAG — Power rating
rk / RK — Rank (lower = better)
Tempo (ADJ_T)

3. Rating Matrix Comparison
From ncaa_wp_matrix_2025.csv:
- rating_team – rating_opponent
- Reversed rows are handled automatically.

4. Total Points Prediction
Uses:
-Team scoring averages
-League average scoring
-Pace (tempo) adjustment
-Clamping to realistic D1 scores (120–180)

5. Score Solver
Using two equations:
-team_score + opp_score = total
-team_score - opp_score = margin

6. Win Probability
A logistic curve converts final margin = win chance.
GUI Features (gui.py)
The GUI is built using Tkinter and provides:

# Team Search
Searchable listboxes for Team 1 and Team 2.
# Score Prediction
Shows:
-Final predicted score
-Win probability

# Scrollable Breakdown Panel
Displays numeric explanations:
-Offense/Defense differences
-BARTHAG, ranking, rating diffs
-Point contributions to the spread
-Tempo-adjusted total scoring calculations

# Stat Glossary Tab
A second GUI tab explains every stat:
-ADJOE / ADJDE
-BARTHAG
-Tempo (ADJ_T)
-Rank interpretation
-Rating matrix meaning
-Margin components
-Beginner-friendly explanations included.

 Datasets Used
1. cbb25.csv includes:
-ADJOE
-ADJDE
-BARTHAG
-ADJ_T
-SEED
-rk / RK
-Team name

2. 2025_cbb_results.csv includes:
-team
-opponent
-teamscore
-oppscore
-location (H/V/N)
-total_points (generated)
-margin (generated)

3. ncaa_wp_matrix_2025.csv contains predicted ratings for matchup pairs:
-team
-opponent
-rating_team
-rating_opponent

# SQL Database Schema
- Core Tables
- seasons
- teams
- conferences
- team_season_advanced_stats
- game_results
- rating_matrix
- Prediction System Tables
- model_versions
- model_features
- training_samples
- precomputed_matchup_projections
- prediction_feature_values
- matchup_predictions
- User & Favorite Tables
- users
- favorite_teams
- audit_log
- Analytics Tables
- team_scoring_summaries
- team_location_splits
- matchup_history_summary
- schedule_strength
- team_recent_form
- The schema is structured to support:
- model training
- model versioning
- fast lookup projections
- historical analysis
- user-stored predictions
- All tables include foreign keys and cascading behavior.

# How to Run the Predictor
1. Install dependencies

pip install pandas

Tkinter comes preinstalled on most Python distributions.

3. Place CSVs in project folder
Make sure the files are named exactly:
cbb25.csv
2025_cbb_results.csv
ncaa_wp_matrix_2025.csv

4. Run the GUI
python gui.py

Example Prediction Output
Input

Team1: Ohio University
Team2: Maine
Location: Neutral

Output
Ohio State 82 – 58 Maine  (Win prob 96.4%)

Breakdown excerpt:
=== team_ratings ===
           Ohio State   off_ADJOE = 121.40   def_ADJDE = 95.10   BARTHAG = 0.880   rank = 22.0   tempo = 69.4
                 Maine   off_ADJOE = 103.00   def_ADJDE = 108.00   BARTHAG = 0.140   rank = 334.0  tempo = 65.4

=== feature_differences (Team1 - Team2) ===
offense_diff     +18.40
defense_diff     +12.90
barthag_diff     +0.740
rank_diff        +312.0
rating_diff      +0.250


Realistic, data-driven, interpretable.

