import os
import sys
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from ingestion.openf1 import fetch_sessions, save_raw_data
from ingestion.fastf1 import fetch_fastf1_data, save_fastf1_data
from processing.transform import DataTransformer

def main():
    year = 2025
    race_name = "Bahrain Grand Prix"

    #Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    #Step 1 fetch data
    try:
        print("Fetching OpenF1 data...")
        data = fetch_sessions(year)
        save_raw_data(data, year)
    except Exception as error:
        print ("OpenF1 error:", error)

    try:
        print("Fetching FastF1 data...")
        fastf1_data = fetch_fastf1_data(year, race_name)

        if fastf1_data:
            laps, results = fastf1_data
            save_fastf1_data(laps, results, year, "bahrain")

    except Exception as error:
        print ("FastF1 error:", error)

    #Step 2 spark processing
    spark = SparkSession.builder.appName("F1 Pipeline").getOrCreate()
    transformer = DataTransformer(spark)

    #OpenF1 JSON
    openf1_path = os.path.join(raw_dir, f"{year}_sessions.json")
    openf1_out = os.path.join(processed_dir, "openf1_sessions")
    os.makedirs(openf1_out, exist_ok=True)

    try:
        df_openf1 = spark.read.option("multiline", "true").json(openf1_path)
        df_openf1_clean = transformer.transform_openf1_sessions(df_openf1)
        df_openf1_clean.write.mode("overwrite").parquet(openf1_out)
        print("OpenF1 processed rows:", df_openf1_clean.count())
    except Exception as error:
        print("OpenF1 processing error:", error)

    #FastF1 csv
    laps_path = os.path.join(raw_dir, f"{year}_bahrain_laps.csv")
    results_path = os.path.join(raw_dir, f"{year}_bahrain_results.csv")
    laps_out = os.path.join(processed_dir, "fastf1_laps")
    results_out = os.path.join(processed_dir, "fastf1_results")
    os.makedirs(laps_out, exist_ok=True)
    os.makedirs(results_out, exist_ok=True)

    try:
        df_laps = spark.read.csv(laps_path, header=True, inferSchema=True)
        df_results = spark.read.csv(results_path, header=True, inferSchema=True)

        df_laps_clean = transformer.transform_fastf1_laps(df_laps, "bahrain")
        df_results_clean = transformer.transform_fastf1_results(df_results, "bahrain")

        df_laps_clean.write.mode("overwrite").parquet(laps_out)
        df_results_clean.write.mode("overwrite").parquet(results_out)

        print("FastF1 laps rows:", df_laps_clean.count())
        print("FastF1 results rows:", df_results_clean.count())

    except Exception as error:
        print("FastF1 processing error:", error)

    #Step 3 skip join entirely
    print("Skipping join: datasets do not overlap")

    #Step 4 sample output
    try:
        print("OpenF1 sample data:")
        df_openf1_clean.show(5)
    except:
        pass

    try:
        print("FastF1 sample laps data:")
        df_laps_clean.show(5)
    except:
        pass

    spark.stop()

if __name__ == "__main__":
    main()