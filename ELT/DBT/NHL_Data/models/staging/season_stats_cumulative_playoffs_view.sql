WITH unnested AS (
	SELECT
		team_id,
		game_type_id,
		years_since_last_active,
		UNNEST(seasons)::raw.season_stats_type AS season_stats
	FROM {{ ref('team_stats_playoffs_cumulative_model') }}
	WHERE current_season = 2023
)

SELECT 
	t.team_full_name,
	u.team_id,
	g.game_type,
	u.game_type_id,
	u.years_since_last_active,
	(season_stats::raw.season_stats_type).*
FROM unnested AS u LEFT JOIN {{ ref('raw_teams') }} AS t
ON u.team_id = t.team_id
LEFT JOIN {{ ref('raw_game_type') }} AS g
ON u.game_type_id = g.game_type_id

