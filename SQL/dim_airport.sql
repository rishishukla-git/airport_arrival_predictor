CREATE TABLE dim_airport (
    airport_id INT PRIMARY KEY,
    airport_name VARCHAR(100),
    terminal_number VARCHAR(50),
    airport_code VARCHAR(3),
    size_factor DECIMAL(3,2),
    avg_annual_sec_time INT,
    avg_annual_checkin_time INT
);