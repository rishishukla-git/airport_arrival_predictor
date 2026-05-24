Airport Arrival Time Predictor (Analytics Engineering Portfolio)

## Overview
"When should I leave for the airport?" is a classic logistics problem. This project is an end-to-end data architecture and predictive model designed to calculate the optimal arrival time for passengers at major UK airports.

Rather than relying on the standard "arrive 2 hours early" advice, this model uses reverse scheduling. It calculates a dynamic arrival time based on static airport layouts, real-world historical security queue data (UK CAA), and simulated live flight volumes.

## Project Goals
As an Analytics Engineer, I built this project to demonstrate:

Dimensional Data Modeling: Designing a scalable Star Schema (Fact and Dimension tables) to handle static airport data, seasonal multipliers, and dynamic hourly flight loads.

Data Transformation: Processing and weighting real-world survey data into usable baseline metrics.

Predictive Analytics: Establishing a mathematical framework to predict queue bottlenecks based on terminal capacity and concurrent departure volumes.

## Tech Stack

Database / Data Warehouse: (e.g., PostgreSQL / SQLite)

Transformations: (e.g., SQL / Python)

Predictive Logic: (e.g., Python / Scikit-learn)
