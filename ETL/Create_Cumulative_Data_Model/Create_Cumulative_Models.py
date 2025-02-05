# Import libraries
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

import time
import warnings

warnings.filterwarnings("ignore")


###########################################################################################################################################
# NEW CODE BLOCK - Cumulative SQL functions
###########################################################################################################################################


# Playoffs
#####################################################################
def create_team_stats_cumulative_playoffs_model(conn, cur):
    """
    - Creates a cumulative idempotent view for teams stats in the playoffs
    - - Old range: range(1918,2025)
    """
    for start_year in range(1918, 2026):

        query = f"""

                WITH season_stats_basic_view AS (
                    SELECT 
                        st.*,
                        t.team_full_name,
                        g.game_type,
                        s.season,
                        SPLIT_PART(s.season, '/', 1)::int AS start_year,
                        SPLIT_PART(s.season, '/', 2)::int AS end_year
                    FROM raw.season_stats AS st LEFT JOIN raw.teams AS t
                    ON st.team_id = t.team_id
                    LEFT JOIN raw.season AS s
                    ON st.season_id = s.season_id 
                    LEFT JOIN raw.game_type AS g
                    ON st.game_type_id = g.game_type_id  
                ),

                last_season AS (
                    SELECT * 
                    FROM raw.team_stats_playoffs
                    WHERE current_season = {start_year - 2}
                ), 

                this_season AS (
                    SELECT * 
                    FROM season_stats_basic_view
                    WHERE start_year = {start_year - 1} AND game_type = 'Playoffs'
                )

                INSERT INTO raw.team_stats_playoffs
                SELECT
                    COALESCE(ls.season_id, ts.season_id) as season_id,
                    COALESCE(ls.team_id, ts.team_id) as team_id,
                    COALESCE(ls.game_type_id, ts.game_type_id) as game_type_id,
                    COALESCE(ls.seasons,
                        ARRAY[]::raw.season_stats_type[]
                        ) || CASE WHEN ts.season IS NOT NULL THEN
                            ARRAY[ROW(
                                ts.start_year::int,
                                ts.faceoff_win_pct::real,
                                ts.games_played::int,
                                ts.goals_against::int,
                                ts.goals_against_per_game::real,
                                ts.goals_for::int,
                                ts.goals_for_per_game::real,
                                ts.losses::int,
                                ts.overtime_losses::real,
                                ts.penalty_kill_net_pct::real,
                                ts.penalty_kill_pct::real,
                                ts.points_pct::real,
                                ts.points::int,
                                ts.power_play_net_pct::real,
                                ts.power_play_pct::real,
                                ts.regulation_and_overtime_wins::int,
                                ts.shots_against_per_game::real,
                                ts.shots_for_per_game::real,
                                ts.ties::real,
                                ts.wins::int,
                                ts.wins_in_regulation::int,
                                ts.wins_in_shootout::int,
                                ts.time_on_ice::text,
                                ts.corsi_for::real,
                                ts.corsi_against::real,
                                ts.corsi_for_pct::real,
                                ts.fenwick_for::real,
                                ts.fenwick_against::real,
                                ts.fenwick_for_pct::real,
                                ts.shots_for::real,
                                ts.shots_against::real,
                                ts.shots_for_pct::real,
                                ts.goals_for_pct::real,
                                ts.expected_goals_for::real,
                                ts.expected_goals_against::real,
                                ts.expected_goals_for_pct::real,
                                ts.scoring_chances_for::real,
                                ts.scoring_chances_against::real,
                                ts.scoring_chances_for_pct::real,
                                ts.scoring_chances_shots_for::real,
                                ts.scoring_chances_shots_against::real,
                                ts.scoring_chances_shots_for_pct::real,
                                ts.scoring_chances_goals_for::real,
                                ts.scoring_chances_goals_against::real,
                                ts.scoring_chances_goals_for_pct::real,
                                ts.scoring_chances_shooting_pct::real,
                                ts.scoring_chances_save_pct::real,
                                ts.high_danger_chances_for::real,
                                ts.high_danger_chances_against::real,
                                ts.high_danger_chances_for_pct::real,
                                ts.high_danger_shots_for::real,
                                ts.high_danger_shots_against::real,
                                ts.high_danger_shots_for_pct::real,
                                ts.high_danger_goals_for::real,
                                ts.high_danger_goals_against::real,
                                ts.high_danger_goals_for_pct::real,
                                ts.high_danger_shooting_pct::real,
                                ts.high_danger_save_pct::real,
                                ts.medium_danger_chances_for::real,
                                ts.medium_danger_chances_against::real,
                                ts.medium_danger_chances_for_pct::real,
                                ts.medium_danger_shots_for::real,
                                ts.medium_danger_shots_against::real,
                                ts.medium_danger_shots_for_pct::real,
                                ts.medium_danger_goals_for::real,
                                ts.medium_danger_goals_against::real,
                                ts.medium_danger_goals_for_pct::real,
                                ts.medium_danger_shooting_pct::real,
                                ts.medium_danger_save_pct::real,
                                ts.low_danger_chances_for::real,
                                ts.low_danger_chances_against::real,
                                ts.low_danger_chances_for_pct::real,
                                ts.low_danger_shots_for::real,
                                ts.low_danger_shots_against::real,
                                ts.low_danger_shots_for_pct::real,
                                ts.low_danger_goals_for::real,
                                ts.low_danger_goals_against::real,
                                ts.low_danger_goals_for_pct::real,
                                ts.low_danger_shooting_pct::real,
                                ts.low_danger_save_pct::real,
                                ts.shooting_pct::real,
                                ts.save_pct::real,
                                ts.pdo_rating::real
                            )::raw.season_stats_type]
                            ELSE ARRAY[]::raw.season_stats_type[] 
                        END AS seasons,
                    COALESCE(ts.start_year, ls.current_season + 1) AS current_season,
                    ts.season_id IS NOT NULL AS is_active,
                    CASE 
                        WHEN ts.start_year IS NOT NULL 
                        THEN 0
                        ELSE ls.years_since_last_active + 1
                    END AS years_since_last_active
                FROM last_season ls FULL OUTER JOIN this_season ts
                ON ls.team_id = ts.team_id;
        """

        cur.execute(query)
        conn.commit()

        print(query)
        time.sleep(1)


# Regular Season
#####################################################################
def create_team_stats_cumulative_regular_season_model(cur, conn):
    """
    - Creates a cumulative idempotent view for teams stats during the regular season
    - Old range: range(1918,2025)
    """
    for start_year in range(1918, 2026):

        query = f"""

                WITH season_stats_basic_view AS (
                    SELECT 
                        st.*,
                        t.team_full_name,
                        g.game_type,
                        s.season,
                        SPLIT_PART(s.season, '/', 1)::int AS start_year,
                        SPLIT_PART(s.season, '/', 2)::int AS end_year
                    FROM raw.season_stats AS st LEFT JOIN raw.teams AS t
                    ON st.team_id = t.team_id
                    LEFT JOIN raw.season AS s
                    ON st.season_id = s.season_id 
                    LEFT JOIN raw.game_type AS g
                    ON st.game_type_id = g.game_type_id  
                ),

                last_season AS (
                    SELECT * 
                    FROM raw.team_stats_regular_season
                    WHERE current_season = {start_year - 2}
                ), 

                this_season AS (
                    SELECT * 
                    FROM season_stats_basic_view
                    WHERE start_year = {start_year - 1} AND game_type = 'Regular Season'
                )

                INSERT INTO raw.team_stats_regular_season
                SELECT
                    COALESCE(ls.season_id, ts.season_id) as season_id,
                    COALESCE(ls.team_id, ts.team_id) as team_id,
                    COALESCE(ls.game_type_id, ts.game_type_id) as game_type_id,
                    COALESCE(ls.seasons,
                        ARRAY[]::raw.season_stats_type[]
                        ) || CASE WHEN ts.season IS NOT NULL THEN
                            ARRAY[ROW(
                                ts.start_year::int,
                                ts.faceoff_win_pct::real,
                                ts.games_played::int,
                                ts.goals_against::int,
                                ts.goals_against_per_game::real,
                                ts.goals_for::int,
                                ts.goals_for_per_game::real,
                                ts.losses::int,
                                ts.overtime_losses::real,
                                ts.penalty_kill_net_pct::real,
                                ts.penalty_kill_pct::real,
                                ts.points_pct::real,
                                ts.points::int,
                                ts.power_play_net_pct::real,
                                ts.power_play_pct::real,
                                ts.regulation_and_overtime_wins::int,
                                ts.shots_against_per_game::real,
                                ts.shots_for_per_game::real,
                                ts.ties::real,
                                ts.wins::int,
                                ts.wins_in_regulation::int,
                                ts.wins_in_shootout::int,
                                ts.time_on_ice::text,
                                ts.corsi_for::real,
                                ts.corsi_against::real,
                                ts.corsi_for_pct::real,
                                ts.fenwick_for::real,
                                ts.fenwick_against::real,
                                ts.fenwick_for_pct::real,
                                ts.shots_for::real,
                                ts.shots_against::real,
                                ts.shots_for_pct::real,
                                ts.goals_for_pct::real,
                                ts.expected_goals_for::real,
                                ts.expected_goals_against::real,
                                ts.expected_goals_for_pct::real,
                                ts.scoring_chances_for::real,
                                ts.scoring_chances_against::real,
                                ts.scoring_chances_for_pct::real,
                                ts.scoring_chances_shots_for::real,
                                ts.scoring_chances_shots_against::real,
                                ts.scoring_chances_shots_for_pct::real,
                                ts.scoring_chances_goals_for::real,
                                ts.scoring_chances_goals_against::real,
                                ts.scoring_chances_goals_for_pct::real,
                                ts.scoring_chances_shooting_pct::real,
                                ts.scoring_chances_save_pct::real,
                                ts.high_danger_chances_for::real,
                                ts.high_danger_chances_against::real,
                                ts.high_danger_chances_for_pct::real,
                                ts.high_danger_shots_for::real,
                                ts.high_danger_shots_against::real,
                                ts.high_danger_shots_for_pct::real,
                                ts.high_danger_goals_for::real,
                                ts.high_danger_goals_against::real,
                                ts.high_danger_goals_for_pct::real,
                                ts.high_danger_shooting_pct::real,
                                ts.high_danger_save_pct::real,
                                ts.medium_danger_chances_for::real,
                                ts.medium_danger_chances_against::real,
                                ts.medium_danger_chances_for_pct::real,
                                ts.medium_danger_shots_for::real,
                                ts.medium_danger_shots_against::real,
                                ts.medium_danger_shots_for_pct::real,
                                ts.medium_danger_goals_for::real,
                                ts.medium_danger_goals_against::real,
                                ts.medium_danger_goals_for_pct::real,
                                ts.medium_danger_shooting_pct::real,
                                ts.medium_danger_save_pct::real,
                                ts.low_danger_chances_for::real,
                                ts.low_danger_chances_against::real,
                                ts.low_danger_chances_for_pct::real,
                                ts.low_danger_shots_for::real,
                                ts.low_danger_shots_against::real,
                                ts.low_danger_shots_for_pct::real,
                                ts.low_danger_goals_for::real,
                                ts.low_danger_goals_against::real,
                                ts.low_danger_goals_for_pct::real,
                                ts.low_danger_shooting_pct::real,
                                ts.low_danger_save_pct::real,
                                ts.shooting_pct::real,
                                ts.save_pct::real,
                                ts.pdo_rating::real
                            )::raw.season_stats_type]
                            ELSE ARRAY[]::raw.season_stats_type[] 
                        END AS seasons,
                    COALESCE(ts.start_year, ls.current_season + 1) AS current_season,
                    ts.season_id IS NOT NULL AS is_active,
                    CASE 
                        WHEN ts.start_year IS NOT NULL 
                        THEN 0
                        ELSE ls.years_since_last_active + 1
                    END AS years_since_last_active
                FROM last_season ls FULL OUTER JOIN this_season ts
                ON ls.team_id = ts.team_id;
        """

        cur.execute(query)
        conn.commit()

        print(query)
        time.sleep(1)
