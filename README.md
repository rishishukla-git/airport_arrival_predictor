Airport Arrival Time Predictor (Analytics Engineering Portfolio)

## Overview
"When should I leave for the airport?" is a classic logistics problem. This project is an end-to-end data architecture and predictive model designed to calculate the optimal arrival time for passengers at major UK airports.

Rather than relying on the standard "arrive 2 hours early" advice, this model uses reverse scheduling. It calculates a dynamic arrival time based on static airport layouts, real-world historical security queue data (UK CAA), and simulated live flight volumes.

## Project Goals
As an Analytics Engineer, I built this project to demonstrate:

Dimensional Data Modeling: Designing a scalable Star Schema (Fact and Dimension tables) to handle static airport data, seasonal multipliers, and dynamic hourly flight loads.

Data Transformation: Processing and weighting real-world survey data into usable baseline metrics.

Predictive Analytics: Establishing a mathematical framework to predict queue bottlenecks based on terminal capacity and concurrent departure volumes.

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

## Data Architecture (Star Schema)
This project utilizes a traditional Star Schema built with SQL to organize the data for efficient modeling.

## Tech Stack

* **Data Architecture:** Star Schema Design (Fact and Dimension modeling) optimized for analytical queries.
* **SQL:** Data Definition Language (DDL) for robust database structuring, including strict constraint management (Primary Keys) and optimized data types.
* **Data Engineering Concepts:** Utilization of CSV Seed Files for static dimension loading, simulating modern data warehouse staging practices (similar to dbt workflows).
* **Analytical Modeling:** Mathematical reverse-scheduling logic and weighted average baseline calculations derived from real-world survey datasets.
* **Version Control:** Git & GitHub (Command-line workflows, modular directory structuring, and repository management).