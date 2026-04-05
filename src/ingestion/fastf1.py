import fastf1
import pandas as pd
import os

def fetch_fastf1_data(year=2025, race_name = "Bahrain Grand Prix"):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    cache_dir = os.path.join(project_root, "data", "cache")

    #Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    fastf1.Cache.enable_cache(cache_dir)

    try:
        session = fastf1.get_session(year, race_name, "R")
        session.load()

    except Exception as error:
        print("Error loading FastF1 session", error)
        return None

    try:
        laps = session.laps
        results = session.results
    except Exception as error:
        print("error extracting session data:", error)
        return None

    return laps, results

def save_fastf1_data(laps, results, year=2025, race_name="bahrain"):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    raw_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    laps_path = os.path.join(raw_dir, f"{year}_{race_name}_laps.csv")
    results_path = os.path.join(raw_dir, f"{year}_{race_name}_results.csv")

    try:
        laps_df = pd.DataFrame(laps)
        results_df = pd.DataFrame(results)

        laps_df.to_csv(laps_path, index=False)
        results_df.to_csv(results_path, index=False)

        print(f"Laps saved to {laps_path}")
        print(f"Results saved to {results_path}")

    except Exception as error:
        print("error saving FastF1 data:", error)