import fastf1
import pandas as pd
import os

def fetch_fastf1_data(year=2025, race_name = "Bahrain Grand Prix", session_type = "R"):
    """
    Fetch session data using FastF1
    session_type:
        R = Race
        Q = Qualifying
        FP1/FP2/FP3 = Practice
    """

    try:
        fastf1.Cache.enable_cache('cache') #speeds up repeated runs

        print(f"Loading {race_name} {year} ({session_type})...")
        session = fastf1.get_session(year, race_name, session_type)
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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_dir = os.path.join(base_dir, "data", "raw")
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

if __name__ == "__main__":
    year = 2025
    race = "Bahrain Grand Prix"

    data = fetch_fastf1_data(year, race)

    if data:
        laps, results = data
        save_fastf1_data(laps, results, year, "bahrain")