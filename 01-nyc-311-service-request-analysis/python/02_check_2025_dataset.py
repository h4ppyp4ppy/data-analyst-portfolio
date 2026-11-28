
import requests
import csv
from pathlib import Path


# NYC 311 API endpoint
url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

# Define our selection criteria

params = {
    "$select": (
        "unique_key, complaint_type, borough, "
        "agency, created_date, closed_date"
    ),
    "$where": (
        "created_date >= '2025-01-01T00:00:00' "
        "AND created_date < '2026-01-01T00:00:00' "
        "AND status = 'Closed' "
        "AND closed_date IS NOT NULL "
        "AND complaint_type = 'Noise - Residential' "
        "AND borough IS NOT NULL"
    ),
    "$order": "created_date ASC, unique_key ASC",
    "$limit": 100
}

# Send the API request
response = requests.get(url, params=params, timeout=60)

# Check the response
if not response.ok:
    print("API error details:")
    print(response.text)

response.raise_for_status()

# Convert the response to Python data
data = response.json()

# Display the results

if data:

    # Define project and output directories
    project_dir = Path(__file__).resolve().parents[1]
    data_dir = project_dir / "data"

    # Create data folder if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)

    # Define output file
    output_file = data_dir / "noise_residential_2025_pilot.csv"

    # Define CSV columns
    fieldnames = [
        "unique_key",
        "complaint_type",
        "borough",
        "agency",
        "created_date",
        "closed_date"
    ]

    # Save records to CSV
    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(data)

    print("\nDATA EXPORT SUCCESSFUL")
    print("----------------------")
    print(f"Records saved: {len(data)}")
    print(f"File location: {output_file}")

else:
    print("No matching records found.")
