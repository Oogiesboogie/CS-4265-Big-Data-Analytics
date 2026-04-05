import requests
import json
import os

def fetch_sessions(year=2025):
    url = f"https://api.openf1.org/v1/sessions?year={year}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as error:
        print("API request failed: ", error)
        return []

    return response.json()

def save_raw_data(data, year=2025):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_dir = os.path.join(project_root, "data", "raw")

    os.makedirs(raw_dir, exist_ok=True)
    file_path = os.path.join(raw_dir, f"{year}_sessions.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved raw data to {file_path}")