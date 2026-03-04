# Lap by Lap: Formula 1 Telemetry and Race Analytics

## Overview

This project builds a scalable Big Data pipeline for analyzing Formula 1 sessions and telemetry data using Apache Spark. 
The system ingests data from external APIs, stores it persistently, and provides a modular framework for distributed processing and future analytical workloads. 
Milestone 2 Demonstrates a working proof of concept, including data acquisition, persistent storage, and structured pipeline organization.
---
## Data Sources
The project uses:
- OpenF1 - Session-level metadata and structures event data
- FastF1 - Detailed telemetry and official timing data (planned integration)
Originally, the project proposed using Ergast API. This was replaced with FastF1 to improve telemetry depth and long term extensibility.
At Milestone 2, OpenF1 ingestion is fully operational. FastF1 integration will be implemented in Milestone 3.
---
## Project Structure
project/\
+-- src/\
| _ +-- ingestion/\
| _ |   +-- openf1.py\
| _ +-- processing/\
| _ |   +-- transform.py\
| _ +-- main.py\
+-- data/\
| _ +-- raw/\
| _ +-- processed/\
+-- requirements.txt\
+-- README.md\
+-- .gitignore

- 'ingestion/' - API data acquisition modules
- 'processing/' - Transformation and normalization logic
- 'main.py' - Spark orchestration
- 'data/raw/' - Raw JSON storage
- 'data/processed/' - Parquet output
---
## Technology Stack
- Python 3
- Apache Spark (PySpark)
- JSON (raw ingestion)
- Parquet (analytical storage format)
---
## Setup Instructions
### 1. Clone the Repository
'''bash
git clone https://github.com/Oogiesboogie/CS-4265-Big-Data-Analytics.git
cd CS-4265-Big-Data-Analytics
### 2. Create Virtual Environment
python -m venv .venv
Activate:
.venv\Scripts\activate
### 3. Install Dependencies
pip install -r requirements.txt
## Running the Pipeline
### Step 1: Fetch Raw Data (OpenF1)
python src/ingestion/openf1.py
this saves session data to data/raw/
### Step 2: Process Data with Spark
spark-submit src/main.py
This writes Parquet output to data/processed/
## Current Status (Milestone 2)
- working API data acquisition
- Persistent raw JSON storage
- Spark-based Parquet generation
- Modular pipeline structure
- Clean repository with documented dependencies
This milestone validates the feasibility of the proposed distributed analytics architecture
## Next Steps (Milestone 3)
- Integrate FastF1 telemetry ingestion
- Normalization schemas across multiple sources
- Implement aggregation and analytical queries
- Evaluate scalability as data volume increases
