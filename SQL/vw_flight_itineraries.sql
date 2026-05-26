CREATE VIEW vw_flight_itineraries AS
WITH RollingMultipliers AS (
    -- Step 1: Calculate the rolling average multiplier on the fly
    SELECT 
        airport_id,
        departure_hour,
        AVG(total_passenger_load) OVER(
            PARTITION BY airport_id 
            ORDER BY departure_hour 
            ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
        ) AS rolling_avg_load,
        AVG(total_passenger_load) OVER(PARTITION BY airport_id) AS daily_avg_load
    FROM vw_hourly_passenger_load
),
CalculatedMultipliers AS (
    -- Step 2: Finalize the hourly traffic multiplier
    SELECT 
        airport_id, 
        departure_hour, 
        ROUND(CAST(rolling_avg_load AS FLOAT) / daily_avg_load, 2) AS hourly_traffic_multiplier
    FROM RollingMultipliers
),
BaseVariables AS (
    -- Step 3: Join everything together and apply Seasonal & Hourly multipliers
    SELECT 
        f.flight_number, 
        a.airport_name, 
        a.terminal_number, 
        f.haul_type, 
        f.departure_time, 
        s.month_id,
        s.month_name,
        
        CAST(ROUND(a.avg_annual_checkin_time * c.hourly_traffic_multiplier * s.traffic_multiplier) AS INT) AS dt_checkin,
        CAST(ROUND(a.avg_annual_sec_time * c.hourly_traffic_multiplier * s.traffic_multiplier) AS INT) AS dt_security,
        
        15 AS dt_transit,
        CASE WHEN f.haul_type = 'Long-Haul' THEN 45 ELSE 30 END AS dt_gate_close
    FROM fact_flights f
    JOIN dim_airport a 
        ON f.airport_id = a.airport_id
    JOIN CalculatedMultipliers c 
        ON f.airport_id = c.airport_id AND f.departure_hour = c.departure_hour
    CROSS JOIN dim_seasonality s 
),
BufferMath AS (
    -- Step 4: Split the base times for Baggage vs No Baggage
    SELECT 
        *,
        (dt_checkin + dt_security + dt_transit + dt_gate_close) AS base_time_with_bags,
        (dt_security + dt_transit + dt_gate_close) AS base_time_no_bags
    FROM BaseVariables
)
-- Step 5: Final dual-output recommendation
SELECT 
    flight_number, 
    airport_name, 
    terminal_number, 
    haul_type, 
    departure_time, 
    month_id,
    month_name,
    dt_checkin, 
    dt_security, 
    dt_transit, 
    dt_gate_close,
    
    -- Scenario A: WITH Checked Bags
    CAST(MAX(base_time_with_bags * 0.10, 15) AS INT) AS dt_buffer_with_bags,
    (base_time_with_bags + CAST(MAX(base_time_with_bags * 0.10, 15) AS INT)) AS total_transit_mins_with_bags,
    time(departure_time, '-' || (base_time_with_bags + CAST(MAX(base_time_with_bags * 0.10, 15) AS INT)) || ' minutes') AS arrival_time_with_bags,

    -- Scenario B: WITHOUT Checked Bags (Carry-on only)
    CAST(MAX(base_time_no_bags * 0.10, 15) AS INT) AS dt_buffer_no_bags,
    (base_time_no_bags + CAST(MAX(base_time_no_bags * 0.10, 15) AS INT)) AS total_transit_mins_no_bags,
    time(departure_time, '-' || (base_time_no_bags + CAST(MAX(base_time_no_bags * 0.10, 15) AS INT)) || ' minutes') AS arrival_time_no_bags

FROM BufferMath;