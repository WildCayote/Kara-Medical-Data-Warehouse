{{config(materialized='table')}}

WITH message_pool AS (
    SELECT 
        id,
        channel_id,
        message
    FROM {{source('public', 'message')}} 
),
matched_prices AS (
    SELECT 
        id,
        channel_id,
        regexp_matches("message", '^(.*?)\s*(?:price|Price|PRICE)\s*(\d+)\s*(birr|ETB)', 'g') AS matches
    FROM message_pool   
)

SELECT
    id,
    channel_id,
    CASE 
        WHEN matches IS NOT NULL THEN
            matches[2] || ' ' || matches[3]
        ELSE NULL
    END AS price
FROM matched_prices
WHERE matches IS NOT NULL
