import os
from pyspark.sql import SparkSession
from openf1 import fetch_sessions, save_raw_data

def main():
    year = 2025

    #Step 1 fetch data
    try:
        print("Fetching data...")
        data = fetch_sessions(year)
        save_raw_data(data, year)
    except Exception as error:
        print ("Error during data acquisition:", error)
        return

    #Step 2 spark processing
    spark = SparkSession.builder.appName("F1 OpenF1 Pipeline").getOrCreate()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", f"{year}_sessions.json")
    processed_path = os.path.join(base_dir, "data", "processed", f"{year}_sessions")

    try:
        df = spark.read.option("multiline", "true").json(raw_path)
    except Exception as error:
        print("Error loading JSON:", error)
        spark.stop()
        return

    print("Raw Data Schema:")
    df.printSchema()

#Create Spark session
spark = SparkSession.builder.appName("F1 OpenF1 Pipeline").getOrCreate()

#Paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_path = os.path.join(base_dir, "data", "raw", "2025_sessions.json")
processed_path = os.path.join(base_dir, "data", "processed", "2025_sessions")

os.makedirs(os.path.join(base_dir, "data", "processed"), exist_ok=True)

#Load raw JSON
df = spark.read.option("multiline", "true").json(raw_path)

print("Raw Data Schema:")
df.printSchema()

print("Sample Rows:")
df.show(10, truncate=False)

df.write.mode("overwrite").parquet(processed_path)

print(f"Processed data saved to {processed_path}")

spark.stop()