
CREATE DATABASE IF NOT EXISTS cbb_matchup_app;
USE cbb_matchup_app;


-- 1) season  (2024-2025)
CREATE TABLE seasons (
    season_id      INT AUTO_INCREMENT PRIMARY KEY,
    season_name    VARCHAR(20) NOT NULL UNIQUE,
    year_start     SMALLINT NOT NULL,
    year_end       SMALLINT NOT NULL,
    is_active      TINYINT NOT NULL DEFAULT 0,
    CONSTRAINT chk_year_order CHECK (year_end >= year_start)
);

truncate seasons;
DROP TABLE IF EXISTS seasons;

-- Seed one season for your project
INSERT INTO seasons (season_name, year_start, year_end, is_active)
VALUES ('2024-25', 2024, 2025, 1);


CREATE TABLE teams (
    team_id        INT AUTO_INCREMENT PRIMARY KEY,
    team_name      VARCHAR(100) NOT NULL UNIQUE,  
    conference_id  INT NULL,
    nickname       VARCHAR(100) NULL,
    home_city      VARCHAR(100) NULL,
    home_state     VARCHAR(50) NULL,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_teams_conference
        FOREIGN KEY (conference_id) REFERENCES conferences(conference_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

DROP TABLE IF EXISTS teams;



-- 2) conferences
CREATE TABLE conferences (
    conference_id  INT AUTO_INCREMENT PRIMARY KEY,
    conf_code      VARCHAR(10) NOT NULL UNIQUE,
    conf_name      VARCHAR(100) NULL
);


-- 3) teams  (links to conferences)
--    Maps the "Team" names from your CSVs.
CREATE TABLE teams (
    team_id        INT AUTO_INCREMENT PRIMARY KEY,
    team_name      VARCHAR(100) NOT NULL UNIQUE,
    conference_id  INT NULL,
    nickname       VARCHAR(100) NULL,
    home_city      VARCHAR(100) NULL,
    home_state     VARCHAR(50) NULL,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_teams_conference
        FOREIGN KEY (conference_id) REFERENCES conferences(conference_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);


-- 4) team_season_advanced_stats  (from cbb25.csv)
CREATE TABLE team_season_advanced_stats (
    team_season_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id        INT NOT NULL,
    season_id      INT NOT NULL,
    rk             INT,              -- RK ranking
    games_played   INT,              -- G
    wins           INT,              -- W

    ADJOE          DECIMAL(6,2),     -- offensive efficiency
    ADJDE          DECIMAL(6,2),     -- defensive efficiency
    BARTHAG        DECIMAL(7,4),
    EFG_O          DECIMAL(5,2),
    EFG_D          DECIMAL(5,2),
    TOR            DECIMAL(5,2),
    TORD           DECIMAL(5,2),
    ORB            DECIMAL(5,2),
    DRB            DECIMAL(5,2),
    FTR            DECIMAL(5,2),
    FTRD           DECIMAL(5,2),
    P2_O           DECIMAL(5,2),     -- 2P_O
    P2_D           DECIMAL(5,2),     -- 2P_D
    P3_O           DECIMAL(5,2),     -- 3P_O
    P3_D           DECIMAL(5,2),     -- 3P_D
    P3R            DECIMAL(5,2),     -- 3PR
    P3RD           DECIMAL(5,2),     -- 3PRD
    ADJ_T          DECIMAL(5,2),
    WAB            DECIMAL(6,2),
    SEED           DECIMAL(4,1),

    CONSTRAINT fk_team_season_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_team_season_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uc_team_season UNIQUE (team_id, season_id)
);


-- 5) game_results  (from 2025_cbb_results.csv)
--    Each row is from the perspective of primary_team vs opponent.
CREATE TABLE game_results (
    game_id            INT AUTO_INCREMENT PRIMARY KEY,
    season_id          INT NOT NULL,
    game_date          DATE NOT NULL,
    primary_team_id    INT NOT NULL,   -- from team column
    opponent_team_id   INT NOT NULL,   -- from opponent column
    location_code      CHAR(1) NOT NULL,  -- 'H', 'V', or 'N' (from 'location')
    primary_team_score INT,
    opponent_score     INT,
    canceled           TINYINT NOT NULL DEFAULT 0,
    postponed          TINYINT NOT NULL DEFAULT 0,
    went_overtime      TINYINT NOT NULL DEFAULT 0,
    d1_level           TINYINT,

    CONSTRAINT fk_game_results_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_game_results_primary_team
        FOREIGN KEY (primary_team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_game_results_opponent_team
        FOREIGN KEY (opponent_team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
DROP TABLE IF EXISTS game_results;


-- 6) rating_matrix  (from ncaa_wp_matrix_2025.csv)
--    Predicted matchup outcomes: team vs opponent.
CREATE TABLE rating_matrix (
    rating_id       INT AUTO_INCREMENT PRIMARY KEY,
    season_id       INT NOT NULL,
    team_id         INT NOT NULL,   -- 'team'
    opponent_id     INT NOT NULL,   -- 'opponent'
    rating_team     DECIMAL(7,3),
    rating_opponent DECIMAL(7,3),
    pred_score_diff DECIMAL(7,3),   -- team - opponent
    win_prob        DECIMAL(6,4),   -- between 0 and 1

    CONSTRAINT fk_rating_matrix_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rating_matrix_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_rating_matrix_opponent
        FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uc_rating_matchup UNIQUE (season_id, team_id, opponent_id)
);


-- 7) users  
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    display_name   VARCHAR(100) NOT NULL,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_admin       TINYINT NOT NULL DEFAULT 0
);


-- 8) matchup_predictions  
--    User picks team + opponent,  store the predicted result.
CREATE TABLE matchup_predictions (
    prediction_id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id                    INT NOT NULL,
    season_id                  INT NOT NULL,
    team_id                    INT NOT NULL,  -- selected "team"
    opponent_id                INT NOT NULL,  -- selected "opponent"
    rating_id_used             INT NULL,      -- FK to rating_matrix if you used it
    predicted_team_score       INT,
    predicted_opponent_score   INT,
    predicted_win_prob         DECIMAL(6,4),
    created_at                 DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pred_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pred_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pred_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pred_opponent
        FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pred_rating
        FOREIGN KEY (rating_id_used) REFERENCES rating_matrix(rating_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);


-- 9) favorite_teams 
CREATE TABLE favorite_teams (
    user_id   INT NOT NULL,
    team_id   INT NOT NULL,
    added_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, team_id),

    CONSTRAINT fk_fav_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_fav_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


-- 10) audit_log  (required auditing / logging table)
--     You can log prediction actions, logins, etc.
CREATE TABLE audit_log (
    audit_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NULL,
    action_type   VARCHAR(50) NOT NULL,   -- e.g. 'LOGIN', 'PREDICT_MATCHUP'
    action_detail TEXT NULL,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);



USE cbb_matchup_app;


-- 11) team_scoring_summaries, Season-level scoring summary

CREATE TABLE team_scoring_summaries (
    season_id          INT NOT NULL,
    team_id            INT NOT NULL,
    games_played       INT NOT NULL DEFAULT 0,
    points_for         INT NOT NULL DEFAULT 0,
    points_against     INT NOT NULL DEFAULT 0,
    avg_points_for     DECIMAL(6,2),
    avg_points_against DECIMAL(6,2),
    avg_margin         DECIMAL(6,2),

    PRIMARY KEY (season_id, team_id),

    CONSTRAINT fk_tss_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_tss_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);


-- 12) team_location_splits
--    Home / road / neutral splits (location effect for scores in CBB)
CREATE TABLE team_location_splits (
    season_id      INT NOT NULL,
    team_id        INT NOT NULL,
    location_code  CHAR(1) NOT NULL,  -- 'H', 'V', 'N'
    games_played   INT NOT NULL DEFAULT 0,
    points_for     INT NOT NULL DEFAULT 0,
    points_against INT NOT NULL DEFAULT 0,
    wins           INT NOT NULL DEFAULT 0,
    losses         INT NOT NULL DEFAULT 0,
    avg_points_for     DECIMAL(6,2),
    avg_points_against DECIMAL(6,2),
    avg_margin         DECIMAL(6,2),

    PRIMARY KEY (season_id, team_id, location_code),

    CONSTRAINT fk_tls_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_tls_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);




-- 13) matchup_history_summary
--   history of team vs opponent, helps score/base rate

CREATE TABLE matchup_history_summary (
    season_id      INT NOT NULL,
    team_id        INT NOT NULL,
    opponent_id    INT NOT NULL,
    games_played   INT NOT NULL DEFAULT 0,
    wins           INT NOT NULL DEFAULT 0,
    losses         INT NOT NULL DEFAULT 0,
    points_for     INT NOT NULL DEFAULT 0,
    points_against INT NOT NULL DEFAULT 0,
    avg_points_for     DECIMAL(6,2),
    avg_points_against DECIMAL(6,2),
    avg_margin         DECIMAL(6,2),

    PRIMARY KEY (season_id, team_id, opponent_id),

    CONSTRAINT fk_mhs_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_mhs_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_mhs_opponent
        FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);




-- 14) model_versions
--    Different prediction model 

CREATE TABLE model_versions (
    model_id        INT AUTO_INCREMENT PRIMARY KEY,
    model_name      VARCHAR(100) NOT NULL,
    description     TEXT NULL,
    algorithm_name  VARCHAR(100) NULL,      -- e.g. 'linear_regression', 'xgboost'
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active       TINYINT NOT NULL DEFAULT 0,
    hyperparams_json JSON NULL               -- or TEXT if your MySQL version hates JSON
);




-- 15) model_features
--    Which features each model uses 

CREATE TABLE model_features (
    feature_id      INT AUTO_INCREMENT PRIMARY KEY,
    model_id        INT NOT NULL,
    feature_name    VARCHAR(100) NOT NULL,   -- e.g. 'ADJOE', 'home_advantage'
    source_table    VARCHAR(100) NULL,       -- e.g. 'team_season_advanced_stats'
    source_column   VARCHAR(100) NULL,       -- e.g. 'ADJOE'
    description     TEXT NULL,
    is_active       TINYINT NOT NULL DEFAULT 1,
    importance_score DECIMAL(6,4) NULL,      -- optional feature importance

    CONSTRAINT fk_mf_model
        FOREIGN KEY (model_id) REFERENCES model_versions(model_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);



-- 16) training_samples
--    Training rows for the model (labels = actual scores from game_results)

CREATE TABLE training_samples (
    sample_id         INT AUTO_INCREMENT PRIMARY KEY,
    model_id          INT NOT NULL,
    game_id           INT NOT NULL,
    season_id         INT NOT NULL,
    team_id           INT NOT NULL,
    opponent_id       INT NOT NULL,
    location_code     CHAR(1) NOT NULL,       
    label_team_score  INT NOT NULL,
    label_opp_score   INT NOT NULL,
    label_margin      INT NOT NULL,           
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ts_model
        FOREIGN KEY (model_id) REFERENCES model_versions(model_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ts_game
        FOREIGN KEY (game_id) REFERENCES game_results(game_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ts_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ts_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ts_opponent
        FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);




-- 17) prediction_feature_values
--    Stores the actual feature values used for a user prediction

CREATE TABLE prediction_feature_values (
    pred_feature_id  INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id    INT NOT NULL,           -- FK to matchup_predictions
    model_id         INT NOT NULL,
    feature_name     VARCHAR(100) NOT NULL,
    feature_value    DECIMAL(18,6) NULL,     -- numeric features
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pfv_prediction
        FOREIGN KEY (prediction_id) REFERENCES matchup_predictions(prediction_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pfv_model
        FOREIGN KEY (model_id) REFERENCES model_versions(model_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);



-- 18) precomputed_matchup_projections
--    Fast lookup table for predicted scores for all team vs opponent pairs
--    This is what the GUI can hit directly to show a score
CREATE TABLE precomputed_matchup_projections (
    projection_id            INT AUTO_INCREMENT PRIMARY KEY,
    season_id                INT NOT NULL,
    model_id                 INT NOT NULL,
    team_id                  INT NOT NULL,
    opponent_id              INT NOT NULL,
    location_code            CHAR(1) NOT NULL,    -- assume H/V/N
    projected_team_score     DECIMAL(6,2),
    projected_opponent_score DECIMAL(6,2),
    projected_margin         DECIMAL(6,2),       -- team - opponent
    projected_win_prob       DECIMAL(6,4),       -- 0..1
    last_computed_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pmp_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pmp_model
        FOREIGN KEY (model_id) REFERENCES model_versions(model_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pmp_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pmp_opponent
        FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT uc_pmp UNIQUE (season_id, model_id, team_id, opponent_id, location_code)
);



-- 19) schedule_strength
--    Strength of schedule features per team/season

CREATE TABLE schedule_strength (
    season_id             INT NOT NULL,
    team_id               INT NOT NULL,
    overall_sos           DECIMAL(7,4) NULL,
    non_conf_sos          DECIMAL(7,4) NULL,
    conf_sos              DECIMAL(7,4) NULL,
    avg_opponent_rating   DECIMAL(7,4) NULL,
    computed_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (season_id, team_id),

    CONSTRAINT fk_sos_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_sos_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);



-- 20) team_recent_form
--    Rolling form metrics (last N games) to affect predictions
CREATE TABLE team_recent_form (
    form_id              INT AUTO_INCREMENT PRIMARY KEY,
    season_id            INT NOT NULL,
    team_id              INT NOT NULL,
    window_size_games    INT NOT NULL,         
    games_played_window  INT NOT NULL DEFAULT 0,
    avg_points_for       DECIMAL(6,2),
    avg_points_against   DECIMAL(6,2),
    avg_margin           DECIMAL(6,2),
    offensive_rating     DECIMAL(7,3) NULL,     
    defensive_rating     DECIMAL(7,3) NULL,
    last_game_date       DATE NULL,
    computed_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_trf_season
        FOREIGN KEY (season_id) REFERENCES seasons(season_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_trf_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

