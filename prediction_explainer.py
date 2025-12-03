"""
@Author - Adam Pinkos
@File   - prediction_explainer.py
@Date   - 12/02/2025
@Brief  - Turn prediction.parts into a numeric breakdown string
          that shows which team has the edge in each stat.
"""

def build_breakdown_text(pred):
    """
    Take the prediction dict from MatchupPredictor.predict_matchup()
    and build a multi-line numeric breakdown.

    All values are numeric; labels indicate Team 1 vs Team 2.AQAQ
    """
    parts = pred.get("parts", {})
    team1 = pred.get("team", "Team1")
    team2 = pred.get("opponent", "Team2")

    # raw team stats
    t1_off   = parts.get("team1_ADJOE", 0.0)
    t1_def   = parts.get("team1_ADJDE", 0.0)
    t1_barth = parts.get("team1_BARTHAG", 0.0)
    t1_rank  = parts.get("team1_RANK", 0.0)
    t1_temp  = parts.get("team1_TEMPO", 0.0)

    t2_off   = parts.get("team2_ADJOE", 0.0)
    t2_def   = parts.get("team2_ADJDE", 0.0)
    t2_barth = parts.get("team2_BARTHAG", 0.0)
    t2_rank  = parts.get("team2_RANK", 0.0)
    t2_temp  = parts.get("team2_TEMPO", 0.0)

    # diffs and point contributions
    offense_diff = parts.get("offense_diff", 0.0)
    defense_diff = parts.get("defense_diff", 0.0)
    barthag_diff = parts.get("barthag_diff", 0.0)
    rank_diff    = parts.get("rank_diff", 0.0)
    rating_diff  = parts.get("rating_diff", 0.0)

    margin_off_def   = parts.get("margin_off_def", 0.0)
    margin_barth     = parts.get("margin_barth", 0.0)
    margin_rank      = parts.get("margin_rank", 0.0)
    margin_rating    = parts.get("margin_rating", 0.0)
    location_edge    = parts.get("location_edge", 0.0)

    raw_margin       = parts.get("raw_margin", 0.0)
    final_margin_cap = parts.get("final_margin_clamped", 0.0)

    baseline_total   = parts.get("baseline_total_points", 0.0)
    tempo_total      = parts.get("tempo_adjusted_total", 0.0)
    final_total      = parts.get("final_total_points", 0.0)

    lines = []

    # ------------------------------------------------------------------
    # Offense / defense / BARTHAG / rank / rating by team
    # ------------------------------------------------------------------
    lines.append("=== team_ratings ===")
    lines.append(f"{team1:>15}  off_ADJOE = {t1_off:6.2f}   def_ADJDE = {t1_def:6.2f}   BARTHAG = {t1_barth:6.3f}   rank = {t1_rank:6.1f}   tempo = {t1_temp:6.2f}")
    lines.append(f"{team2:>15}  off_ADJOE = {t2_off:6.2f}   def_ADJDE = {t2_def:6.2f}   BARTHAG = {t2_barth:6.3f}   rank = {t2_rank:6.1f}   tempo = {t2_temp:6.2f}")
    lines.append("")

    # ------------------------------------------------------------------
    # Diffs from the model's perspective (Team1 - Team2)
    # ------------------------------------------------------------------
    lines.append("=== feature_differences (Team1 - Team2) ===")
    lines.append(f"offense_diff      = {offense_diff:+7.2f}")
    lines.append(f"defense_diff      = {defense_diff:+7.2f}")
    lines.append(f"barthag_diff      = {barthag_diff:+7.3f}")
    lines.append(f"rank_diff         = {rank_diff:+7.1f}")
    lines.append(f"rating_diff       = {rating_diff:+7.3f}")
    lines.append("")

    # ------------------------------------------------------------------
    # How many points each feature adds to spread
    # ------------------------------------------------------------------
    lines.append("=== margin_components (points, + favors Team1) ===")
    lines.append(f"margin_off_def    = {margin_off_def:+7.2f}")
    lines.append(f"margin_barth      = {margin_barth:+7.2f}")
    lines.append(f"margin_rank       = {margin_rank:+7.2f}")
    lines.append(f"margin_rating     = {margin_rating:+7.2f}")
    lines.append(f"location_edge     = {location_edge:+7.2f}")
    lines.append("")

    # ------------------------------------------------------------------
    # Final margin and scoring environment
    # ------------------------------------------------------------------
    lines.append("=== final_numbers ===")
    lines.append(f"raw_margin        = {raw_margin:+7.2f}")
    lines.append(f"final_margin_cap  = {final_margin_cap:+7.2f}")
    lines.append("")
    lines.append(f"baseline_total    = {baseline_total:7.2f}")
    lines.append(f"tempo_total       = {tempo_total:7.2f}")
    lines.append(f"final_total_pts   = {final_total:7.2f}")

    return "\n".join(lines)
