WITH eligible AS (
 SELECT *, ROW_NUMBER() OVER (PARTITION BY league ORDER BY npxg_per90 DESC, minutes DESC, player_id ASC) AS representative_order
 FROM striker_scatter_ready WHERE minutes >= 900 AND non_penalty_shots >= 50
)
SELECT CASE league WHEN 'EPL' THEN 'Premier League' WHEN 'La_liga' THEN 'La Liga' WHEN 'Serie_A' THEN 'Serie A' WHEN 'Ligue_1' THEN 'Ligue 1' ELSE league END AS league,
 player_name AS player, player_id, minutes, npshots_per90 AS volume, npxg_per_shot AS quality,
 npxg_per90 AS production, non_penalty_shots AS shots
FROM eligible WHERE representative_order = 1 ORDER BY league