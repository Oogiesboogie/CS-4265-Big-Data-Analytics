from pyspark.sql.functions import col, to_timestamp

class DataTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform_openf1_sessions(selfself, df):
        """
        Clean and normalize OpenF1 session data
        """

        #Drop null rows
        df = df.dropna()

        #Select useful columns
        columns_to_keep = [
            "session_key",
            "session_name",
            "location",
            "country",
            "date_start",
            "date_end"
        ]

        existing_cols = [c for c in columns_to_keep if c in df.columns]
        df = df.select(*existing_cols)

        #Rename columns for consistency
        if "session_name" in df.columns:
            df = df.withColumnRenamed("session_name", "session")

        #Convert timestamp
        if "date_start" in df.columns:
            df = df.withColumn("date_start", to_timestamp(col("date_start")))

        if "date_end" in df.columns:
            df = df.withColumn("date_end", to_timestamp(col("date_end")))

        return df

    def transform_fastf1_laps(self, df):
        """
        Clean FastF1 lap data
        """

        df = df.dropna()

        columns_to_keep = [
            "Driver",
            "LapTime",
            "LapNumber",
            "Stint",
            "Compound",
            "Team"
        ]

        existing_cols = [c for c in columns_to_keep if c in df.columns]
        df = df.select(*existing_cols)

        return df

    def transform_fastf1_results(self, df):
        """
        Clean FastF1 results data
        """

        df = df.dropna()

        columns_to_keep = [
            "DriverNumber",
            "FullName",
            "TeamName",
            "Position",
            "Points"
        ]

        existing_cols = [c for c in columns_to_keep if c in df.columns]
        df = df.select(*existing_cols)

        return df