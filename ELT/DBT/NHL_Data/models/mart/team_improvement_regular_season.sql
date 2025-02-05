-- Config to set as table and not view
{{
    config(
        materialized = 'table'
    )
}}

WITH most_improved AS (
	SELECT *
	FROM {{ ref('team_stats_regular_season_cumulative_model') }}
	WHERE current_season = (
		SELECT MAX(current_season)
		FROM {{ ref('team_stats_regular_season_cumulative_model') }}
	)
)

SELECT
	mi.current_season AS start_year,
	CONCAT(mi.current_season, mi.current_season + 1) AS season_id,
	rt.team_full_name,
	mi.team_id,
	'Regular Season' As game_type,
	2 AS game_type_id,
	((mi.seasons[CARDINALITY(mi.seasons)]::raw.season_stats_type).points - CASE WHEN (mi.seasons[1]::raw.season_stats_type).points = 0 THEN 1 ELSE (mi.seasons[1]::raw.season_stats_type).points::numeric END) / 
	ABS(CASE WHEN (mi.seasons[1]::raw.season_stats_type).points = 0 THEN 1 ELSE (mi.seasons[1]::raw.season_stats_type).points::numeric END) AS team_improvement
FROM most_improved AS mi LEFT JOIN {{ ref('raw_teams') }} AS rt
ON mi.team_id = rt.team_id
ORDER BY team_improvement DESC

