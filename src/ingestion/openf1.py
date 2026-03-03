import requests
import json
import os

def fetch_sessions(year=2025):
    url = f"https://api.openf1.org/v1/sessions?year={year}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

def save_raw_data(data, year=2025):
    os.makedirs("../../data/raw", exist_ok=True)

    file_path = f"../../data/raw/{year}_sessions.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

        print(f"Saved raw data to {file_path}")

if __name__ == "__main__":
    year = 2025
    data = fetch_sessions(year)
    save_raw_data(data, year)