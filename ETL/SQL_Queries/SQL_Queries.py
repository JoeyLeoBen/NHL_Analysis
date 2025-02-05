###########################################################################################################################################
# NEW CODE BLOCK - Drop all tables
###########################################################################################################################################

# DROP TABLES
teams_table_drop = "DROP TABLE IF EXISTS raw.teams;"
season_table_drop = "DROP TABLE IF EXISTS raw.season;"
game_type_table_drop = "DROP TABLE IF EXISTS raw.game_type;"
season_stats_table_drop = "DROP TABLE IF EXISTS raw.season_stats;"

playoffs_cumulative_data_model_drop = "DROP TABLE IF EXISTS raw.team_stats_playoffs;"
regular_season_cumulative_data_model_drop = (
    "DROP TABLE IF EXISTS raw.team_stats_regular_season;"
)

###########################################################################################################################################
# NEW CODE BLOCK - Create all tables
###########################################################################################################################################

# CREATE TABLES
# DIMENSION TABLES
teams_table_create = """

    CREATE TABLE IF NOT EXISTS raw.teams (
        team_id int NOT NULL PRIMARY KEY,
        team_full_name varchar NOT NULL
    );
    
"""


season_table_create = """

    CREATE TABLE IF NOT EXISTS raw.season (
        season_id int NOT NULL PRIMARY KEY,
        season varchar NOT NULL
    );
    
"""

game_type_table_create = """

    CREATE TABLE IF NOT EXISTS raw.game_type (
        game_type_id int NOT NULL PRIMARY KEY,
        game_type varchar NOT NULL
    );
    
"""

# FACT TABLE
season_stats_table_create = """

CREATE TABLE IF NOT EXISTS raw.season_stats (
        PRIMARY KEY (team_id, season_id, game_type_id),
        season_id int NOT NULL,
        game_type_id int NOT NULL,
        team_id int NOT NULL,
        faceoff_win_pct float NOT NULL,
        games_played int NOT NULL,
        goals_against int NOT NULL,
        goals_against_per_game float NOT NULL,
        goals_for int NOT NULL,
        goals_for_per_game float NOT NULL,
        losses int NOT NULL,
        overtime_losses float NOT NULL,
        penalty_kill_net_pct float NOT NULL,
        penalty_kill_pct float NOT NULL,
        points_pct float NOT NULL,
        points int NOT NULL,
        power_play_net_pct float NOT NULL,
        power_play_pct float NOT NULL,
        regulation_and_overtime_wins int NOT NULL,
        shots_against_per_game float NOT NULL,
        shots_for_per_game float NOT NULL,
        ties float NOT NULL,
        wins int NOT NULL,
        wins_in_regulation int NOT NULL,
        wins_in_shootout int NOT NULL,
        time_on_ice varchar NOT NULL,
        corsi_for float NOT NULL,
        corsi_against float NOT NULL,
        corsi_for_pct float NOT NULL,
        fenwick_for float NOT NULL,
        fenwick_against float NOT NULL,
        fenwick_for_pct float NOT NULL,
        shots_for float NOT NULL,
        shots_against float NOT NULL,
        shots_for_pct float NOT NULL,
        goals_for_pct float NOT NULL,
        expected_goals_for float NOT NULL,
        expected_goals_against float NOT NULL,
        expected_goals_for_pct float NOT NULL,
        scoring_chances_for float NOT NULL,
        scoring_chances_against float NOT NULL,
        scoring_chances_for_pct float NOT NULL,
        scoring_chances_shots_for float NOT NULL,
        scoring_chances_shots_against float NOT NULL,
        scoring_chances_shots_for_pct float NOT NULL,
        scoring_chances_goals_for float NOT NULL,
        scoring_chances_goals_against float NOT NULL,
        scoring_chances_goals_for_pct float NOT NULL,
        scoring_chances_shooting_pct float NOT NULL,
        scoring_chances_save_pct float NOT NULL,
        high_danger_chances_for float NOT NULL,
        high_danger_chances_against float NOT NULL,
        high_danger_chances_for_pct float NOT NULL,
        high_danger_shots_for float NOT NULL,
        high_danger_shots_against float NOT NULL,
        high_danger_shots_for_pct float NOT NULL,
        high_danger_goals_for float NOT NULL,
        high_danger_goals_against float NOT NULL,
        high_danger_goals_for_pct float NOT NULL,
        high_danger_shooting_pct float NOT NULL,
        high_danger_save_pct float NOT NULL,
        medium_danger_chances_for float NOT NULL,
        medium_danger_chances_against float NOT NULL,
        medium_danger_chances_for_pct float NOT NULL,
        medium_danger_shots_for float NOT NULL,
        medium_danger_shots_against float NOT NULL,
        medium_danger_shots_for_pct float NOT NULL,
        medium_danger_goals_for float NOT NULL,
        medium_danger_goals_against float NOT NULL,
        medium_danger_goals_for_pct float NOT NULL,
        medium_danger_shooting_pct float NOT NULL,
        medium_danger_save_pct float NOT NULL,
        low_danger_chances_for float NOT NULL,
        low_danger_chances_against float NOT NULL,
        low_danger_chances_for_pct float NOT NULL,
        low_danger_shots_for float NOT NULL,
        low_danger_shots_against float NOT NULL,
        low_danger_shots_for_pct float NOT NULL,
        low_danger_goals_for float NOT NULL,
        low_danger_goals_against float NOT NULL,
        low_danger_goals_for_pct float NOT NULL,
        low_danger_shooting_pct float NOT NULL,
        low_danger_save_pct float NOT NULL,
        shooting_pct float NOT NULL,
        save_pct float NOT NULL,
        pdo_rating float NOT NULL
    );
        
"""

# MODEL TABLES
create_season_stats_type_raw = """
                            
CREATE TYPE raw.season_stats_type AS (
        start_year int, 
        faceoff_win_pct float,
        games_played int,
        goals_against int,
        goals_against_per_game float,
        goals_for int,
        goals_for_per_game float,
        losses int,
        overtime_losses float,
        penalty_kill_net_pct float,
        penalty_kill_pct float,
        points_pct float,
        points int,
        power_play_net_pct float,
        power_play_pct float,
        regulation_and_overtime_wins int,
        shots_against_per_game float,
        shots_for_per_game float,
        ties float,
        wins int,
        wins_in_regulation int,
        wins_in_shootout int,
        time_on_ice varchar,
        corsi_for float,
        corsi_against float,
        corsi_for_pct float,
        fenwick_for float,
        fenwick_against float,
        fenwick_for_pct float,
        shots_for float,
        shots_against float,
        shots_for_pct float,
        goals_for_pct float,
        expected_goals_for float,
        expected_goals_against float,
        expected_goals_for_pct float,
        scoring_chances_for float,
        scoring_chances_against float,
        scoring_chances_for_pct float,
        scoring_chances_shots_for float,
        scoring_chances_shots_against float,
        scoring_chances_shots_for_pct float,
        scoring_chances_goals_for float,
        scoring_chances_goals_against float,
        scoring_chances_goals_for_pct float,
        scoring_chances_shooting_pct float,
        scoring_chances_save_pct float,
        high_danger_chances_for float,
        high_danger_chances_against float,
        high_danger_chances_for_pct float,
        high_danger_shots_for float,
        high_danger_shots_against float,
        high_danger_shots_for_pct float,
        high_danger_goals_for float,
        high_danger_goals_against float,
        high_danger_goals_for_pct float,
        high_danger_shooting_pct float,
        high_danger_save_pct float,
        medium_danger_chances_for float,
        medium_danger_chances_against float,
        medium_danger_chances_for_pct float,
        medium_danger_shots_for float,
        medium_danger_shots_against float,
        medium_danger_shots_for_pct float,
        medium_danger_goals_for float,
        medium_danger_goals_against float,
        medium_danger_goals_for_pct float,
        medium_danger_shooting_pct float,
        medium_danger_save_pct float,
        low_danger_chances_for float,
        low_danger_chances_against float,
        low_danger_chances_for_pct float,
        low_danger_shots_for float,
        low_danger_shots_against float,
        low_danger_shots_for_pct float,
        low_danger_goals_for float,
        low_danger_goals_against float,
        low_danger_goals_for_pct float,
        low_danger_shooting_pct float,
        low_danger_save_pct float,
        shooting_pct float,
        save_pct float,
        pdo_rating float
    );
                            
"""

create_season_stats_type_analytics = """
                            
CREATE TYPE analytics.season_stats_type AS (
        start_year int, 
        faceoff_win_pct float,
        games_played int,
        goals_against int,
        goals_against_per_game float,
        goals_for int,
        goals_for_per_game float,
        losses int,
        overtime_losses float,
        penalty_kill_net_pct float,
        penalty_kill_pct float,
        points_pct float,
        points int,
        power_play_net_pct float,
        power_play_pct float,
        regulation_and_overtime_wins int,
        shots_against_per_game float,
        shots_for_per_game float,
        ties float,
        wins int,
        wins_in_regulation int,
        wins_in_shootout int,
        time_on_ice varchar,
        corsi_for float,
        corsi_against float,
        corsi_for_pct float,
        fenwick_for float,
        fenwick_against float,
        fenwick_for_pct float,
        shots_for float,
        shots_against float,
        shots_for_pct float,
        goals_for_pct float,
        expected_goals_for float,
        expected_goals_against float,
        expected_goals_for_pct float,
        scoring_chances_for float,
        scoring_chances_against float,
        scoring_chances_for_pct float,
        scoring_chances_shots_for float,
        scoring_chances_shots_against float,
        scoring_chances_shots_for_pct float,
        scoring_chances_goals_for float,
        scoring_chances_goals_against float,
        scoring_chances_goals_for_pct float,
        scoring_chances_shooting_pct float,
        scoring_chances_save_pct float,
        high_danger_chances_for float,
        high_danger_chances_against float,
        high_danger_chances_for_pct float,
        high_danger_shots_for float,
        high_danger_shots_against float,
        high_danger_shots_for_pct float,
        high_danger_goals_for float,
        high_danger_goals_against float,
        high_danger_goals_for_pct float,
        high_danger_shooting_pct float,
        high_danger_save_pct float,
        medium_danger_chances_for float,
        medium_danger_chances_against float,
        medium_danger_chances_for_pct float,
        medium_danger_shots_for float,
        medium_danger_shots_against float,
        medium_danger_shots_for_pct float,
        medium_danger_goals_for float,
        medium_danger_goals_against float,
        medium_danger_goals_for_pct float,
        medium_danger_shooting_pct float,
        medium_danger_save_pct float,
        low_danger_chances_for float,
        low_danger_chances_against float,
        low_danger_chances_for_pct float,
        low_danger_shots_for float,
        low_danger_shots_against float,
        low_danger_shots_for_pct float,
        low_danger_goals_for float,
        low_danger_goals_against float,
        low_danger_goals_for_pct float,
        low_danger_shooting_pct float,
        low_danger_save_pct float,
        shooting_pct float,
        save_pct float,
        pdo_rating float
    );
                            
"""

playoffs_cumulative_data_model_create = """

    CREATE TABLE IF NOT EXISTS raw.team_stats_playoffs (
        season_id int,
        team_id int,
        game_type_id int,
        seasons raw.season_stats_type[],
        current_season int,
        is_active boolean,
        years_since_last_active int,
        PRIMARY KEY (team_id, current_season)
    );
    
"""

regular_season_cumulative_data_model_create = """

    CREATE TABLE IF NOT EXISTS raw.team_stats_regular_season (
        season_id int,
        team_id int,
        game_type_id int,
        seasons raw.season_stats_type[],
        current_season int,
        is_active boolean,
        years_since_last_active int,
        PRIMARY KEY (team_id, current_season)
    );
    
"""


###########################################################################################################################################
# NEW CODE BLOCK - Insert records
###########################################################################################################################################

# INSERT RECORDS
teams_table_col_num = 2
teams_table_variables = "%s" + (",%s" * (teams_table_col_num - 1))
teams_table_insert = (
    """

    INSERT INTO raw.teams(
        team_id,
        team_full_name
    )
    VALUES ("""
    + teams_table_variables
    + """)
    ON CONFLICT (team_id)
        DO NOTHING;
        
"""
)

season_table_col_num = 2
season_table_variables = "%s" + (",%s" * (season_table_col_num - 1))
season_table_insert = (
    """

    INSERT INTO raw.season(
        season_id,
        season
    )
    VALUES ("""
    + season_table_variables
    + """)
    ON CONFLICT (season_id)
        DO NOTHING;
        
"""
)

game_type_table_col_num = 2
game_type_table_variables = "%s" + (",%s" * (game_type_table_col_num - 1))
game_type_table_insert = (
    """

    INSERT INTO raw.game_type(
        game_type_id,
        game_type
    )
    VALUES ("""
    + game_type_table_variables
    + """)
    ON CONFLICT (game_type_id)
        DO NOTHING;
        
"""
)

season_stats_table_col_num = 85
season_stats_table_variables = "%s" + (",%s" * (season_stats_table_col_num - 1))
season_stats_table_insert = (
    """

    INSERT INTO raw.season_stats(
        season_id,
        game_type_id,
        team_id,
        faceoff_win_pct,
        games_played,
        goals_against,
        goals_against_per_game,
        goals_for,
        goals_for_per_game,
        losses,
        overtime_losses,
        penalty_kill_net_pct,
        penalty_kill_pct,
        points_pct,
        points,
        power_play_net_pct,
        power_play_pct,
        regulation_and_overtime_wins,
        shots_against_per_game,
        shots_for_per_game,
        ties,
        wins,
        wins_in_regulation,
        wins_in_shootout,
        time_on_ice,
        corsi_for,
        corsi_against,
        corsi_for_pct,
        fenwick_for,
        fenwick_against,
        fenwick_for_pct,
        shots_for,
        shots_against,
        shots_for_pct,
        goals_for_pct,
        expected_goals_for,
        expected_goals_against,
        expected_goals_for_pct,
        scoring_chances_for,
        scoring_chances_against,
        scoring_chances_for_pct,
        scoring_chances_shots_for,
        scoring_chances_shots_against,
        scoring_chances_shots_for_pct,
        scoring_chances_goals_for,
        scoring_chances_goals_against,
        scoring_chances_goals_for_pct,
        scoring_chances_shooting_pct,
        scoring_chances_save_pct,
        high_danger_chances_for,
        high_danger_chances_against,
        high_danger_chances_for_pct,
        high_danger_shots_for,
        high_danger_shots_against,
        high_danger_shots_for_pct,
        high_danger_goals_for,
        high_danger_goals_against,
        high_danger_goals_for_pct,
        high_danger_shooting_pct,
        high_danger_save_pct,
        medium_danger_chances_for,
        medium_danger_chances_against,
        medium_danger_chances_for_pct,
        medium_danger_shots_for,
        medium_danger_shots_against,
        medium_danger_shots_for_pct,
        medium_danger_goals_for,
        medium_danger_goals_against,
        medium_danger_goals_for_pct,
        medium_danger_shooting_pct,
        medium_danger_save_pct,
        low_danger_chances_for,
        low_danger_chances_against,
        low_danger_chances_for_pct,
        low_danger_shots_for,
        low_danger_shots_against,
        low_danger_shots_for_pct,
        low_danger_goals_for,
        low_danger_goals_against,
        low_danger_goals_for_pct,
        low_danger_shooting_pct,
        low_danger_save_pct,
        shooting_pct,
        save_pct,
        pdo_rating
    )
    VALUES ("""
    + season_stats_table_variables
    + """)
         
"""
)


###########################################################################################################################################
# NEW CODE BLOCK - Query lists
###########################################################################################################################################

# QUERY LISTS
create_table_queries = [
    teams_table_create,
    season_table_create,
    game_type_table_create,
    season_stats_table_create,
    playoffs_cumulative_data_model_create,
    regular_season_cumulative_data_model_create,
]

drop_table_queries = [
    teams_table_drop,
    season_table_drop,
    game_type_table_drop,
    season_stats_table_drop,
    playoffs_cumulative_data_model_drop,
    regular_season_cumulative_data_model_drop,
]
