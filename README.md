# Lap by Lap: Formula 1 Telemetry and Race Analytics

## Overview

This project builds a scalable Big Data pipeline for analyzing Formula 1 sessions and telemetry data using Apache Spark. 

The system
- Fetches data from external APIs (OpenF1 and FastF1)
- Stores raw data persistently (JSON/CSV)
- Applies cleaning, normalization, and transformation
- Outputs analytics-ready Parquet datasets

Milestone 3 demonstrates a fully functional pipeline, with automated data flow from ingestion through processing to output.

---

## Data Sources
The project uses:
- OpenF1 - Session-level metadata (races, sessions, drivers)
- FastF1 - Detailed telemetry and official timing data
  
Notes
- Previously proposed Ergast API was replaced with FastF1 for richer telemetry
- OpenF1 ingestion is fully operational; FastF1 ingestion integrated in M3
- All data is stored locally under data/raw/ and data/processed/

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
| - +-- cache/\
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
- Python 3.12
- Apache Spark (PySpark)
- JSON (raw ingestion)
- CSV (some telemetry input (FastF1))
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
python src/ingestion/fastf1.py
- downloads session and telemetry data
- this saves session data to data/raw/
### Step 2: Process Data with Spark
spark-submit src/main.py
- Applies transformations
- This writes Parquet output to data/processed/
- Handles missing data and API errors gracefully
- Prints sample output and summary statistics 
## Data Dictionary

**Raw Files:**
| File | Description | Format |
|------|-------------|--------|
| '2025_sessions.json' | OpenF1 session metadata | JSON |
| '2018_bahrain_laps.csv' | FastF1 lap timing | CSV |
| '2018_bahrain_results.csv' | FastF1 official results | CSV |

**Processed Files:**
| File/Folder | Description | Format | Notes |
|-------------|-------------|--------|-------|
| 'openf1_sessions/' | Cleaned OpenF1 session data | Parquet | Columns: 'FullName, Team, Event, SessionType, LapTime' |
| 'fastf1_laps/' | Cleaned lap data | Parquet | Columns: 'Driver, LapNumber, LapTime, RaceName' |
| 'fastf1_results/' | Cleaned race results | Parquet | Columns: 'Driver, Position, Points, Team' |

### Sample Output

**OpenF1 processed rows:** 120
**FastF1 laps rows:** 90
**FastF1 results rows:** 22

**Sample OpenF1:**
| FullName | Team | Event | SessionType | LapTime |
|----------|------|-------|-------------|---------|
| Lando N | Mclaren | Bahrain GP | Race | 1:34.123 |
| Max V | Red Bull | Bahrain GP | Race | 1:34.567 |

**Sample FastF1 laps:**
| Driver | LapNumber | LapTime | RaceName| 
|--------|-----------|---------|---------|
| Lando N | 1 | 1:34.123 | Bahrain GP |
| Max V | 1 | 1:34.567 | Bahrain GP |

## Next Steps (Milestone 4)
- Aggregation and analytical queries on processed data
- Integration of additional APIs or historical datasets
- Enhanced visualizations and dashboards
- Performance optimization and distributed scaling
