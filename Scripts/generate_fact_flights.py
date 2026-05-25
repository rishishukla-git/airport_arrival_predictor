import csv
import random
from datetime import datetime, timedelta

# Configuration
TOTAL_ROWS = 1000
OUTPUT_FILE = 'Data/fact_flights.csv'

# Reference data based on your dim_airport table
airport_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
airlines = ['BA', 'EZ', 'VS', 'FR', 'LM']

# Map specific destinations to their logical haul types
destination_map = {
    'EDI': 'Domestic',     # Edinburgh
    'BFS': 'Domestic',     # Belfast
    'GLA': 'Domestic',     # Glasgow
    'ABZ': 'Domestic',     # Aberdeen
    'CDG': 'Short-Haul',   # Paris
    'AMS': 'Short-Haul',   # Amsterdam
    'FRA': 'Short-Haul',   # Frankfurt
    'BCN': 'Short-Haul',   # Barcelona
    'DUB': 'Short-Haul',   # Dublin
    'JFK': 'Long-Haul',    # New York
    'DXB': 'Long-Haul',    # Dubai
    'LAX': 'Long-Haul',    # Los Angeles
    'SIN': 'Long-Haul',    # Singapore
    'HND': 'Long-Haul'     # Tokyo
}

# Start generating flights from August 1, 2026
start_date = datetime(2026, 8, 1, 5, 0, 0)

print(f"Generating {TOTAL_ROWS} logically correct flights...")

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['flight_id', 'flight_number', 'airport_id', 'destination_code', 'haul_type', 'scheduled_departure', 'passenger_capacity'])
    
    # Generate the rows
    for i in range(1, TOTAL_ROWS + 1):
        flight_id = i
        
        # Randomize airline and airport
        airline = random.choice(airlines)
        flight_num = f"{airline}{random.randint(100, 999)}"
        airport_id = random.choice(airport_ids)
        
        # Pick a destination and automatically grab its matching haul type
        destination, haul = random.choice(list(destination_map.items()))
        
        # Capacity logic based on the mapped haul type
        if haul == 'Long-Haul':
            capacity = random.randint(250, 400)
        elif haul == 'Short-Haul':
            capacity = random.randint(150, 220)
        else: # Domestic
            capacity = random.randint(80, 150)
            
        # Random departure time within a 30-day window
        random_minutes = random.randint(0, 43200) # 30 days in minutes
        departure_time = start_date + timedelta(minutes=random_minutes)
        
        writer.writerow([flight_id, flight_num, airport_id, destination, haul, departure_time.strftime('%Y-%m-%d %H:%M:%S'), capacity])

print(f"Success! {TOTAL_ROWS} rows saved to {OUTPUT_FILE}")