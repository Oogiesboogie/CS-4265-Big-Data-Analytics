from pyspark.sql.functions import col, to_timestamp, lower


class DataTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform_openf1_sessions(selfself, df):
        df = df.dropna
        columns_to_keep = ["session_key", "session_name", "location", "country", "date_start", "date_end"]
        df = df.select(*[c for c in columns_to_keep if c in df.columns])

        #Rename for consistency
        if "session_name" in df.columns:
            df = df.withColumnRenamed("session_name", "session")

        #Convert timestamp
        if "date_start" in df.columns:
            df = df.withColumn("date_start", to_timestamp(col("date_start")))
        if "date_end" in df.columns:
            df = df.withColumn("date_end", to_timestamp(col("date_end")))

        #create normalized join key
        df = df.withColumn("event_name", lower(col("location")))

        return df

    def transform_fastf1_laps(self, df, race_name):
        df = df.dropna()
        columns_to_keep = ["Driver","LapTime","LapNumber","Stint","Compound","Team"]
        df = df.select(*[c for c in columns_to_keep if c in df.columns])
        df = df.withColumn("event_name", lower(col(lit(race_name)))) #add join key
        return df

    def transform_fastf1_results(self, df, race_name):
        df = df.dropna()
        columns_to_keep = ["DriverNumber","FullName","TeamName","Position","Points"]
        df = df.select(*[c for c in columns_to_keep if c in df.columns])
        df = df.withColumn("event_name", lower(col(lit(race_name)))) #add join key

        return df

#Join OpenF1 sessions with FastF1 results
def join_openf1_fastf1(self, openf1_df, fastf1_df):
    return fastf1_df.join(openf1_df, on="event_name", how="inner")