WITH full_stats AS (
	SELECT *
	FROM {{ ref('season_stats_cumulative_regular_season_view') }}
	UNION
	SELECT *
	FROM {{ ref('season_stats_cumulative_playoffs_view') }}
),

grouped_regular_season_sums AS (
	SELECT 
		game_type_id,
		team_id,
		SUM(CASE WHEN game_type_id = 2 THEN 1 ELSE 0 END) AS regular_season_sum
	FROM full_stats
	GROUP BY game_type_id, team_id
	HAVING game_type_id = 2
	ORDER BY regular_season_sum DESC
),

grouped_playoff_sums AS (
	SELECT 
		game_type_id,
		team_id,
		SUM(CASE WHEN game_type_id = 3 THEN 1 ELSE 0 END) AS made_playoffs_sum
	FROM full_stats
	GROUP BY game_type_id, team_id
	HAVING game_type_id = 3
	ORDER BY made_playoffs_sum DESC
),

playoff_outcomes AS(
	SELECT
		3 AS game_type_id,
		season_id,
		start_year,
		winning_team_id AS team_id,
		winning_team AS team_full_name,
		4 AS playoff_outcome_id,
		'Stanley Cup Winners' AS playoff_outcome
	FROM {{ ref('stanley_cup_winners') }}
	UNION
	SELECT 
		3 AS game_type_id,
		season_id,
		start_year,
		losing_team_id AS team_id,
		losing_team AS team_full_name,
		5 AS playoff_outcome_id,
		'Stanley Cup Runner-up' AS playoff_outcome
	FROM {{ ref('stanley_cup_winners') }}
	ORDER BY start_year
),

stanley_cup AS (
	SELECT 
		team_id,
		game_type_id,
		playoff_outcome_id,
		SUM(CASE WHEN playoff_outcome_id = 4 THEN 1 ELSE 0 END) AS won_stanley_cup_sum
	FROM playoff_outcomes
	GROUP BY team_id, game_type_id, playoff_outcome_id
	HAVING playoff_outcome_id = 4
	ORDER BY won_stanley_cup_sum DESC
), 

final AS (
	SELECT 
		fs.*,
		im.team_improvement AS team_improvement_during_regular_season,
		CASE WHEN po.playoff_outcome_id IS NULL THEN 0 ELSE po.playoff_outcome_id END AS playoff_outcome_id,
		CASE WHEN po.playoff_outcome IS NULL THEN 'Other' ELSE po.playoff_outcome END AS playoff_outcome,
		CASE WHEN fs.game_type_id = 2 THEN 1 ELSE 0 END AS regular_season_count,
		CASE WHEN fs.game_type_id = 3 THEN 1 ELSE 0 END AS made_playoffs_count,
		grs.regular_season_sum,
		CASE WHEN gps.made_playoffs_sum IS NULL THEN 0 ELSE gps.made_playoffs_sum END AS made_playoffs_sum,
		CASE WHEN po.playoff_outcome_id = 4 THEN 1 ELSE 0 END AS won_stanely_cup_count,
		CASE WHEN po.playoff_outcome_id = 5 THEN 1 ELSE 0 END AS lost_in_stanely_cup_final_count
	FROM full_stats AS fs LEFT JOIN {{ ref('team_improvement_regular_season') }} AS im
	ON fs.team_id = im.team_id 
	LEFT JOIN playoff_outcomes AS po
	ON fs.start_year = po.start_year AND fs.game_type_id = po.game_type_id AND fs.team_id = po.team_id
	LEFT JOIN grouped_regular_season_sums AS grs
	ON fs.team_id = grs.team_id
	LEFT JOIN grouped_playoff_sums AS gps
	ON fs.team_id = gps.team_id
),

final_2 AS (
	SELECT 
		f.*,
		CASE WHEN sc.won_stanley_cup_sum IS NULL OR sc.won_stanley_cup_sum = 0 
			THEN 0
			ELSE sc.won_stanley_cup_sum
		END AS won_stanley_cup_sum,

		(CASE WHEN 
			f.made_playoffs_sum IS NULL OR f.made_playoffs_sum = 0 
			THEN 0.000000001 
			ELSE f.made_playoffs_sum
		END)::real / f.regular_season_sum AS made_playoffs_efficiency,

		(CASE WHEN 
			sc.won_stanley_cup_sum IS NULL OR sc.won_stanley_cup_sum = 0 
			THEN 0.000000001 
			ELSE sc.won_stanley_cup_sum 
		END)::real / 
		(CASE WHEN 
			f.made_playoffs_sum IS NULL OR f.made_playoffs_sum = 0 
			THEN 0.000000001 
			ELSE f.made_playoffs_sum
		END)::real AS won_stanley_cup_efficiency

	FROM final AS f LEFT JOIN stanley_cup AS sc
	ON f.team_id = sc.team_id
	ORDER BY start_year
)

SELECT 
    team_full_name,
    team_id,
    game_type,
    game_type_id,
    playoff_outcome,
    playoff_outcome_id,
    years_since_last_active,
    start_year,
    team_improvement_during_regular_season,
    regular_season_sum,
    made_playoffs_sum,
    won_stanley_cup_sum,
    made_playoffs_efficiency,
    won_stanley_cup_efficiency,
    time_on_ice,
    regular_season_count,
    made_playoffs_count,
    won_stanely_cup_count,
    lost_in_stanely_cup_final_count,
    games_played,
    faceoff_win_pct,
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
FROM final_2