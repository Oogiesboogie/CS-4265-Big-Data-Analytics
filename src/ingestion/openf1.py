import requests
import json
import os

def fetch_sessions(year=2025):
    url = f"https://api.openf1.org/v1/sessions?year={year}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print("API request failed: ", error)
        return []

    return response.json()

def save_raw_data(data, year=2025):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")

    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"{year}_sessions.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

        print(f"Saved raw data to {file_path}")

if __name__ == "__main__":
    year = 2025
    data = fetch_sessions(year)
    save_raw_data(data, year)