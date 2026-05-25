import csv
import random
from datetime import datetime, timedelta

# Configuration
TOTAL_ROWS = 1000
OUTPUT_FILE = 'Data/fact_flights.csv'

# Reference data based on your dim_airport table
airport_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
airlines = ['BA', 'EZ', 'VS', 'FR', 'LM']
destinations = ['JFK', 'CDG', 'DXB', 'AMS', 'FRA', 'LAX', 'DUB', 'EDI', 'BCN', 'MAD']
haul_types = ['Domestic', 'Short-Haul', 'Long-Haul']

# Start generating flights from August 1, 2026
start_date = datetime(2026, 8, 1, 5, 0, 0)

print(f"Generating {TOTAL_ROWS} flights...")

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['flight_id', 'flight_number', 'airport_id', 'destination_code', 'haul_type', 'scheduled_departure', 'passenger_capacity'])
    
    # Generate the rows
    for i in range(1, TOTAL_ROWS + 1):
        flight_id = i
        
        # Randomize flight details
        airline = random.choice(airlines)
        flight_num = f"{airline}{random.randint(100, 999)}"
        airport_id = random.choice(airport_ids)
        destination = random.choice(destinations)
        haul = random.choice(haul_types)
        
        # Capacity logic based on haul type
        if haul == 'Long-Haul':
            capacity = random.randint(250, 400)
        else:
            capacity = random.randint(100, 200)
            
        # Random departure time within a 30-day window
        random_minutes = random.randint(0, 43200) # 30 days in minutes
        departure_time = start_date + timedelta(minutes=random_minutes)
        
        writer.writerow([flight_id, flight_num, airport_id, destination, haul, departure_time.strftime('%Y-%m-%d %H:%M:%S'), capacity])

print(f"Success! {TOTAL_ROWS} rows saved to {OUTPUT_FILE}")