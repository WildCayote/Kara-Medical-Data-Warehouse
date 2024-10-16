{{config(materialized='table')}}

WITH message_pool AS (
    SELECT 
        id,
        channel_id,
        media_path,
        message
    FROM {{source('public', 'message')}} 
),
matched_prices AS (
    SELECT 
        id,
        channel_id,
        media_path,
        regexp_matches("message", '^(.*?)\s*(?:price|Price|PRICE)\s*(\d+)\s*(birr|ETB)', 'g') AS matches
    FROM message_pool   
)

SELECT
    id,
    channel_id,
    media_path,
    CASE 
        WHEN matches IS NOT NULL THEN
            matches[1]
        ELSE NULL
    END AS name
FROM matched_prices
WHERE matches IS NOT NULL