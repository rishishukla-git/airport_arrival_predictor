CREATE VIEW vw_hourly_passenger_load AS
WITH hourly_totals AS (
    -- Step 1: Calculate the raw passenger counts per hour
    SELECT 
        a.airport_id,
        a.airport_name,
        a.terminal_number,
        f.departure_hour,
        COUNT(f.flight_id) AS total_departures,
        SUM(f.passenger_capacity) AS total_passenger_load
    FROM fact_flights f
    JOIN dim_airport a 
        ON f.airport_id = a.airport_id
    GROUP BY 
        a.airport_id,
        a.airport_name,
        a.terminal_number,
        f.departure_hour
)
-- Step 2: Create the multiplier using a Window Function
SELECT 
    airport_id,
    airport_name,
    terminal_number,
    departure_hour,
    total_departures,
    total_passenger_load,
    ROUND(
        CAST(total_passenger_load AS FLOAT) / AVG(total_passenger_load) OVER(PARTITION BY airport_id), 
    2) AS hourly_traffic_multiplier
FROM hourly_totals;