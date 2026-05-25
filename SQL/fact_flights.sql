CREATE TABLE fact_flights (
    flight_id INT PRIMARY KEY,
    flight_number VARCHAR(10),
    airport_id INT,
    destination_code VARCHAR(3),
    haul_type VARCHAR(15),
    scheduled_departure TIMESTAMP,
    passenger_capacity INT
);