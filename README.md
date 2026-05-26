Airport Arrival Time Predictor (Analytics Engineering Portfolio)

# Smart Airport Arrival Time Predictor

## Overview
"When should I leave for the airport?" is a classic logistics problem. This project is an end-to-end data architecture and predictive model designed to calculate the optimal arrival time for passengers at major UK airports. 

Rather than relying on static advice (e.g., "arrive 2 hours early"), this model uses reverse scheduling. It dynamically calculates arrival times based on terminal layouts, real-world baseline security data, and predictive hourly/seasonal queue multipliers.

## Project Goals
As an Analytics Engineer, I built this project to demonstrate:

Dimensional Data Modeling: Designing a scalable Star Schema (Fact and Dimension tables) to handle static airport data, seasonal multipliers, and dynamic hourly flight loads.

Data Transformation: Processing and weighting real-world survey data into usable baseline metrics.

Predictive Analytics: Establishing a mathematical framework to predict queue bottlenecks based on terminal capacity and concurrent departure volumes.

## Data Sources & Business Logic Assumptions
This model is built on realistic operational assumptions and public data:
* **Baseline Queue Data:** Terminal-specific baseline check-in and security wait times are modeled using publicly available aviation data from the **UK Government Civil Aviation Authority (CAA)**.
* **Walking/Transit Times:** A standard 15-minute gate walk is dynamically multiplied by an `airport_size_factor` (e.g., Heathrow Terminal 5 takes significantly longer to traverse than London City).
* **Gate Closure Rules:** 45 minutes prior to departure for Long-Haul flights; 30 minutes for Short-Haul/Domestic flights.
* **Dynamic Safety Buffer:** The model applies a flexible safety margin calculated as `MAX(10% of total transit time, 15 minutes)`. This ensures small flights get a minimum 15-minute pad, while complex long-haul itineraries receive proportionally larger safety nets.

## The Core Logistics Model
The target arrival time is calculated using a series of sequential durations:

$$T_{arrive} = T_{std} - \Delta t_{gate\_close} - \Delta t_{transit} - \Delta t_{security} - \Delta t_{checkin} - \Delta t_{buffer}$$

### Variable Breakdown:
* **T_std:** Scheduled time of departure.
* **Δt_gate_close:** Time before departure that the boarding gate closes (varies by domestic vs. international).
* **Δt_transit:** Walking time from the security checkpoint to the specific departure gate.
* **Δt_security:** The primary variable predicted by the model (baseline security wait time * seasonal multiplier).
* **Δt_checkin:** Time spent checking bags (equals 0 if hand-luggage only).
* **Δt_buffer:** Dynamic safety margin (10-15% of total ETA times).

## Data Architecture
This project utilizes a robust **Star Schema** built with SQL to organize the data for efficient modeling, pushing complex mathematical computation directly into the database via SQL Views.

### Schema Breakdown:
* `dim_airport`: Static terminal data, physical size factors, and UK CAA baseline queue times.
* `dim_seasonality`: Monthly traffic multipliers and descriptions.
* `fact_flights`: A static daily timetable of scheduled departures, aircraft haul types, and passenger capacities.
* `vw_flight_itineraries`: The master analytical view that handles all feature engineering and duration math.

## Tech Stack & Skills Demonstrated
* **Data Architecture:** Star Schema Design (Fact and Dimension modeling) optimized for analytical queries.
* **Advanced SQL:** DDL, Common Table Expressions (CTEs), Window Functions, and complex conditional aggregations.
* **Data Engineering Workflow:** CSV Seed Files for staging simulated modern data warehouse workflows.
* **Application Layer:** Interactive Python CLI using `sqlite3` to orchestrate in-memory database queries.
* **Analytical Modeling:** Mathematical reverse-scheduling logic and weighted average baseline calculations derived from real-world survey datasets.
* **Version Control:** Git & GitHub (modular directory structuring and iterative logic deployment).
