import sqlite3
import csv
import os

# 1. Automatically find the exact path of your project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_csv_to_table(cursor, table_name, file_name, columns):
    """Helper function to load CSV data into SQLite using bulletproof paths"""
    cursor.execute(f"CREATE TABLE {table_name} ({columns})")
    
    # Safely construct the exact path to the Data folder
    absolute_path = os.path.join(PROJECT_ROOT, 'Data', file_name)
    
    with open(absolute_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        cursor.executemany(f"INSERT INTO {table_name} VALUES ({','.join(['?']*len(columns.split(',')))})", reader)

print("✈️ Booting up Airport Arrival Calculator...")

# 2. Boot up the temporary database & load data
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

load_csv_to_table(cursor, 'dim_seasonality', 'dim_seasonality.csv', 'month_id INT, month_name TEXT, season_category TEXT, traffic_multiplier REAL, description TEXT')
load_csv_to_table(cursor, 'dim_airport', 'dim_airport.csv', 'airport_id INT, airport_name TEXT, terminal_number TEXT, airport_code TEXT, size_factor REAL, avg_annual_sec_time INT, avg_annual_checkin_time INT')
load_csv_to_table(cursor, 'fact_flights', 'fact_flights.csv', 'flight_id INT, flight_number TEXT, airport_id INT, destination_code TEXT, haul_type TEXT, departure_time TEXT, departure_hour INT, passenger_capacity INT')

# 3. Create the Base Passenger View (This is what went missing!)
cursor.execute("""
CREATE VIEW vw_hourly_passenger_load AS
SELECT a.airport_id, f.departure_hour, SUM(f.passenger_capacity) AS total_passenger_load
FROM fact_flights f
JOIN dim_airport a ON f.airport_id = a.airport_id
GROUP BY a.airport_id, f.departure_hour;
""")

# 4. Create the Master Itinerary View
cursor.execute("""
CREATE VIEW vw_flight_itineraries AS
WITH RollingMultipliers AS (
    SELECT airport_id, departure_hour,
           AVG(total_passenger_load) OVER(PARTITION BY airport_id ORDER BY departure_hour ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rolling_avg_load,
           AVG(total_passenger_load) OVER(PARTITION BY airport_id) AS daily_avg_load
    FROM vw_hourly_passenger_load
),
CalculatedMultipliers AS (
    SELECT airport_id, departure_hour, ROUND(CAST(rolling_avg_load AS FLOAT) / daily_avg_load, 2) AS hourly_traffic_multiplier
    FROM RollingMultipliers
),
BaseVariables AS (
    SELECT f.flight_number, a.airport_name, a.terminal_number, f.haul_type, f.departure_time, s.month_id, s.month_name,
           CAST(ROUND(a.avg_annual_checkin_time * c.hourly_traffic_multiplier * s.traffic_multiplier) AS INT) AS dt_checkin,
           CAST(ROUND(a.avg_annual_sec_time * c.hourly_traffic_multiplier * s.traffic_multiplier) AS INT) AS dt_security,
           CAST(ROUND(15 * a.size_factor) AS INT) AS dt_transit,
           CASE WHEN f.haul_type = 'Long-Haul' THEN 45 ELSE 30 END AS dt_gate_close
    FROM fact_flights f
    JOIN dim_airport a ON f.airport_id = a.airport_id
    JOIN CalculatedMultipliers c ON f.airport_id = c.airport_id AND f.departure_hour = c.departure_hour
    CROSS JOIN dim_seasonality s 
),
BufferMath AS (
    SELECT *,
           (dt_checkin + dt_security + dt_transit + dt_gate_close) AS base_time_with_bags,
           (dt_security + dt_transit + dt_gate_close) AS base_time_no_bags
    FROM BaseVariables
)
SELECT flight_number, airport_name, terminal_number, haul_type, departure_time, month_id, month_name, dt_checkin, dt_security, dt_transit, dt_gate_close,
       CAST(MAX(base_time_with_bags * 0.10, 15) AS INT) AS dt_buffer_with_bags,
       (base_time_with_bags + CAST(MAX(base_time_with_bags * 0.10, 15) AS INT)) AS total_transit_mins_with_bags,
       time(departure_time, '-' || (base_time_with_bags + CAST(MAX(base_time_with_bags * 0.10, 15) AS INT)) || ' minutes') AS arrival_time_with_bags,
       CAST(MAX(base_time_no_bags * 0.10, 15) AS INT) AS dt_buffer_no_bags,
       (base_time_no_bags + CAST(MAX(base_time_no_bags * 0.10, 15) AS INT)) AS total_transit_mins_no_bags,
       time(departure_time, '-' || (base_time_no_bags + CAST(MAX(base_time_no_bags * 0.10, 15) AS INT)) || ' minutes') AS arrival_time_no_bags
FROM BufferMath;
""")

# 5. The Interactive User Interface
print("\n" + "="*50)
print("   WELCOME TO THE SMART DEPARTURE CALCULATOR")
print("="*50)

# Get a random flight number from the DB just to give the user a hint
cursor.execute("SELECT flight_number FROM fact_flights LIMIT 1")
hint_flight = cursor.fetchone()[0]

user_flight = input(f"Enter your Flight Number (e.g., {hint_flight}): ").strip().upper()
user_month = input("Enter your Travel Month (e.g., August): ").strip().capitalize()
user_bags = input("Are you checking a bag? (Y/N): ").strip().upper()

# 6. Ask SQL for the exact answer!
cursor.execute("""
    SELECT * FROM vw_flight_itineraries 
    WHERE flight_number = ? AND month_name = ?
    LIMIT 1;
""", (user_flight, user_month))

flight = cursor.fetchone()

if flight:
    # Unpack the massive SQL row
    (flight_num, airport, terminal, haul, dep_time, m_id, month, dt_checkin, dt_sec, dt_trans, dt_gate, 
     buf_bags, total_bags, arrive_bags, buf_no_bags, total_no_bags, arrive_no_bags) = flight
    
    print("\n" + "="*50)
    print(f"🎫 ITINERARY FOR FLIGHT: {flight_num} ({month} Departure)")
    print("="*50)
    print(f"Departing: {airport} ({terminal}) at {dep_time}")
    print(f"Haul Type: {haul}\n")
    print("⏳ DURATION BREAKDOWN:")
    
    # Conditional display based on user input
    if user_bags == 'Y':
        print(f"  • Check-in/Bag Drop:   {dt_checkin} mins")
        print(f"  • Security Queue:      {dt_sec} mins")
        print(f"  • Walk to Gate:        {dt_trans} mins")
        print(f"  • Gate Closure:        {dt_gate} mins prior")
        print(f"  • Safety Buffer:       {buf_bags} mins")
        print("-" * 50)
        print(f"TOTAL AIRPORT TIME:      {total_bags} mins")
        print(f"\n✅ RECOMMENDATION: Arrive at terminal by ** {arrive_bags} **")
    else:
        print("  • Check-in/Bag Drop:   SKIPPED (Carry-on only)")
        print(f"  • Security Queue:      {dt_sec} mins")
        print(f"  • Walk to Gate:        {dt_trans} mins")
        print(f"  • Gate Closure:        {dt_gate} mins prior")
        print(f"  • Safety Buffer:       {buf_no_bags} mins")
        print("-" * 50)
        print(f"TOTAL AIRPORT TIME:      {total_no_bags} mins")
        print(f"\n✅ RECOMMENDATION: Arrive at terminal by ** {arrive_no_bags} **")
    print("="*50 + "\n")
else:
    print("\n❌ ERROR: Flight not found or invalid month entered. Please try again.\n")