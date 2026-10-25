-- Sessionization and noise filtering for raw telemetry data
WITH time_diffs AS (
    SELECT
        user_id,
        event_time,
        event_type,
        LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_event_time
    FROM raw_events
),
new_sessions AS (
    SELECT
        user_id,
        event_time,
        event_type,
        CASE
            WHEN prev_event_time IS NULL THEN 1
            WHEN EXTRACT(EPOCH FROM (event_time - prev_event_time)) > 1800 THEN 1
            ELSE 0
        END AS is_new_session
    FROM time_diffs
),
session_ids AS (
    SELECT
        user_id,
        event_time,
        event_type,
        SUM(is_new_session) OVER (PARTITION BY user_id ORDER BY event_time) AS session_idx
    FROM new_sessions
),
session_stats AS (
    SELECT
        user_id,
        session_idx,
        COUNT(event_type) AS events_count,
        EXTRACT(EPOCH FROM (MAX(event_time) - MIN(event_time))) AS session_duration_sec
    FROM session_ids
    GROUP BY user_id, session_idx
)
SELECT
    s.user_id,
    s.session_idx,
    s.event_time,
    s.event_type
FROM session_ids s
JOIN session_stats st
  ON s.user_id = st.user_id AND s.session_idx = st.session_idx
WHERE st.events_count > 1
  AND st.session_duration_sec > 0
  AND st.session_duration_sec < 14400
ORDER BY s.user_id, s.session_idx, s.event_time;