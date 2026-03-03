import os
from pyspark.sql import SparkSession

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
df.show(5, truncate=False)

df.write.mode("overwrite").parquet(processed_path)

print(f"Processed data saved to {processed_path}")

spark.stop()