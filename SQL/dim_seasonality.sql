CREATE TABLE dim_seasonality (
    month_id INT PRIMARY KEY,
    month_name VARCHAR(15),
    season_category VARCHAR(20),
    traffic_multiplier DECIMAL(3,2),
    description VARCHAR(100)
);