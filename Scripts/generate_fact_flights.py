import csv
import random

# Configuration
TOTAL_ROWS = 1000
OUTPUT_FILE = 'Data/fact_flights.csv'

# Reference data
airport_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
airlines = ['BA', 'EZ', 'VS', 'FR', 'LM']

# Map specific destinations to their logical haul types
destination_map = {
    'EDI': 'Domestic',     'BFS': 'Domestic',     'GLA': 'Domestic',     'ABZ': 'Domestic',
    'CDG': 'Short-Haul',   'AMS': 'Short-Haul',   'FRA': 'Short-Haul',   'BCN': 'Short-Haul',   'DUB': 'Short-Haul',
    'JFK': 'Long-Haul',    'DXB': 'Long-Haul',    'LAX': 'Long-Haul',    'SIN': 'Long-Haul',    'HND': 'Long-Haul'
}

# Standard airline scheduling minute intervals
minute_blocks = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

print(f"Generating {TOTAL_ROWS} daily scheduled flights...")

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the updated column headers
    writer.writerow(['flight_id', 'flight_number', 'airport_id', 'destination_code', 'haul_type', 'departure_time', 'departure_hour', 'passenger_capacity'])
    
    # Generate the rows
    for i in range(1, TOTAL_ROWS + 1):
        flight_id = i
        
        airline = random.choice(airlines)
        flight_num = f"{airline}{random.randint(100, 999)}"
        airport_id = random.choice(airport_ids)
        destination, haul = random.choice(list(destination_map.items()))
        
        # Capacity logic
        if haul == 'Long-Haul':
            capacity = random.randint(250, 400)
        elif haul == 'Short-Haul':
            capacity = random.randint(150, 220)
        else: # Domestic
            capacity = random.randint(80, 150)
            
        # Generate the daily schedule time
        hour = random.randint(5, 23) # Flights between 5 AM and 11 PM
        minute = random.choice(minute_blocks)
        departure_time = f"{hour:02d}:{minute:02d}:00"
        
        writer.writerow([flight_id, flight_num, airport_id, destination, haul, departure_time, hour, capacity])

print(f"Success! Timetable generated at {OUTPUT_FILE}")