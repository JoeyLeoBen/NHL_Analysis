-- Config to set as table and not view
{{
    config(
        materialized = 'table'
    )
}}

SELECT * 
FROM {{ source('raw', 'season_stats') }}

