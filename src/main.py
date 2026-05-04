import os
import sys
import logging
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, min, max

# Ensure correct Python environment for Spark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Project imports
from ingestion.openf1 import fetch_sessions, save_raw_data
from ingestion.fastf1 import fetch_fastf1_data, save_fastf1_data
from processing.transform import DataTransformer

# Config
CONFIG = {
    "years": [2023, 2024, 2025],
    "session_type": "R", # R = Race, Q = Qualifying
    "output_path": "output/",
    "log_level": "INFO"
}

# Logging
def setup_logging():
    logging.basicConfig(
        level=getattr(logging, CONFIG["log_level"]),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Spark
def create_spark_session():
    return (
        SparkSession.builder
        .appName("F1 Big Data Pipeline")
        .getOrCreate()
    )

def ingest_data():
    logging.info("Starting data ingestion...")
    all_data = []

    for year in CONFIG["years"]:
        logging.info(f"Fetching sessions for {year}")

        try:
            sessions = fetch_sessions(year=year)

            for session in sessions:
                try:
                    logging.info(f"Processing session {session}")

                    data = fetch_fastf1_data(session)
                    all_data.extend(data)

                except Exception as e:
                    logging.error(f"Failed session {session}: {e}")

        except Exception as e:
            logging.error(f"Failed year {year}: {e}")

    logging.info(f"Ingested {len(all_data)} records")
    return all_data

# Transformation
def transform_data(spark, raw_data):
    logging.info("Transforming data...")

    df = spark.createDataFrame(raw_data)

    # Basic cleaning
    df = df.dropna()

    # Example derived column
    df = df.withColumn("lap_time_seconds", col("lap_time") / 1000)

    # Aggregations
    driver_stats = df.groupBy("driver").agg(
        avg("lap_time_seconds").alias("avg_lap_time"),
        min("lap_time_seconds").alias("min_lap_time"),
        max("lap_time_seconds").alias("max_lap_time")
    )

    race_summary = df.groupBy("race").agg(
        avg("lap_time_seconds").alias("avg_race_pace"),
        max("speed").alias("top_speed")
    )

    logging.info("Finished transforming data")
    return df, driver_stats, race_summary

# Validation
def validate_data(df):
    logging.info("Running validation checks...")

    if df.count() == 0:
        raise ValueError("Dataset is empty!")

    if "lap_time" not in df.columns:
        raise ValueError("Missing required column: lap_time")

    logging.info("Validation passed")

# Save
def save_outputs(df, driver_stats, race_summary):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    base_path = CONFIG["output_path"]

    df.write.mode("overwrite").parquet(f"{base_path}/raw/{timestamp}")
    driver_stats.write.mode("overwrite").parquet(f"{base_path}/driver_stats/{timestamp}")
    race_summary.write.mode("overwrite").parquet(f"{base_path}/race_summary/{timestamp}")

    logging.info("Data saved successfully!")

# Main
def main():
    setup_logging()
    spark = create_spark_session()

    try:
        raw_data = ingest_data()

        if not raw_data:
            logging.error("No data ingested. Exiting...")
            return

        df, driver_stats, race_summary = transform_data(spark, raw_data)

        validate_data(df)

        save_outputs(df, driver_stats, race_summary)

        logging.info("Pipeline completed successfully!")

    except Exception as e:
        logging.critical(f"Pipeline failed: {e}")

    finally:
        spark.stop()

if __name__ == "__main__":
    main()