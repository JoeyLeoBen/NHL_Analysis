-- Config to set as table and not view
{{
    config(
        materialized = 'table'
    )
}}

WITH season_avg AS (
    -- Step 1: Calculate the average and team count for each season across all teams
    SELECT
        game_type_id,
        start_year,
        AVG(losses) AS season_avg_losses,
        COUNT(team_id) AS team_count
    FROM {{ ref('analysis_view') }}
    GROUP BY game_type_id, start_year
),

rolling_season_avg AS (
    -- Step 2: Calculate the weighted rolling 3-season average for each game_type_id
    SELECT
        game_type_id,
        start_year,
        season_avg_losses,
        team_count,
        SUM(season_avg_losses * team_count) OVER (
            PARTITION BY game_type_id
            ORDER BY start_year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        )
        / SUM(team_count) OVER (
            PARTITION BY game_type_id
            ORDER BY start_year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS three_year_rolling_season_avg_losses
    FROM season_avg
),

rolling_team_avg AS (
    -- Step 3: Calculate the 3-season rolling average for each team
    SELECT
        team_id,
        game_type_id,
        start_year,
        losses,
        AVG(losses) OVER (
            PARTITION BY team_id, game_type_id
            ORDER BY start_year
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS three_year_rolling_avg_losses
    FROM {{ ref('analysis_view') }}
)

-- Step 4: Combine rolling team and weighted season averages, and calculate the difference
SELECT
    t.team_id,
    t.game_type_id,
    t.start_year,
    t.losses,
    t.three_year_rolling_avg_losses,
    s.three_year_rolling_season_avg_losses,
    t.three_year_rolling_avg_losses - s.three_year_rolling_season_avg_losses AS three_year_rolling_losses_variance
FROM rolling_team_avg t
JOIN rolling_season_avg s
    ON t.game_type_id = s.game_type_id
   AND t.start_year = s.start_year
ORDER BY t.team_id, t.game_type_id, t.start_year
