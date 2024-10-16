{{config(materialized='table')}}

WITH message_pool AS (
    SELECT 
        id,
        channel_id,
        message
    FROM {{source('public', 'message')}} 
)

SELECT
    id,
    channel_id,
    array_to_string(ARRAY(
            SELECT regexp_replace(unnest(regexp_matches("message", '09\s*[0-9]{8}', 'g')), '\s+', '', 'g')
        ), ', ') AS phone_numbers
FROM message_pool