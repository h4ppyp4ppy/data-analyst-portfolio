import requests
from datetime import datetime
import statistics

# NYC 311 dataset API endpoint
url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

# Request 5 records
params = {
    "$select": "unique_key, created_date, closed_date, complaint_type, status, borough",
    "$where": "status = 'Closed' AND closed_date IS NOT NULL",
    "$order": "created_date DESC",
    "$limit": 5
}

# Send API request
response = requests.get(url, params=params, timeout=30)

# Check the response
response.raise_for_status()

# Convert JSON response into Python data
data = response.json()

print("Connection successful!")
print("HTTP status:", response.status_code)
print("Records received:", len(data))

if data:
    print("\nLATEST 5 SERVICE REQUESTS")

    elapsed_times = []


    for i, record in enumerate(data, start=1):
        print(f"\n--- RECORD {i} ---")

        fields = [
            "unique_key",
            "created_date",
            "closed_date",
            "complaint_type",
            "status",
            "borough"
        ]
        created = datetime.fromisoformat(record["created_date"])
        closed = datetime.fromisoformat(record["closed_date"])

        elapsed = closed - created

        elapsed_minutes = elapsed.total_seconds() / 60

        elapsed_times.append(elapsed_minutes)

        print(f"Elapsed time: {elapsed_minutes:.2f} minutes")


        for field in fields:
            print(f"{field}: {record.get(field, 'Not provided')}")

    if elapsed_times:
        average_elapsed = sum(elapsed_times) / len(elapsed_times)

        print("\nSUMMARY")
        print(f"Average elapsed time: {average_elapsed:.2f} minutes")

    median_elapsed = statistics.median(elapsed_times)

    print(f"Median elapsed time: {median_elapsed:.2f} minutes")

    minimum = min(elapsed_times)
    maximum = max(elapsed_times)
    time_range = maximum - minimum

    print(f"Minimum: {minimum:.2f} minutes")
    print(f"Maximum: {maximum:.2f} minutes")
    print(f"Range: {time_range:.2f} minutes")

    quartiles = statistics.quantiles(
        elapsed_times,
        n=4,
        method="inclusive"
    )

    q1 = quartiles[0]
    q2 = quartiles[1]
    q3 = quartiles[2]

    print(f"Q1: {q1:.2f} minutes")
    print(f"Q2: {q2:.2f} minutes")
    print(f"Q3: {q3:.2f} minutes")

    iqr = q3 - q1

    print(f"IQR: {iqr:.2f} minutes")

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    print(f"Lower limit: {lower_limit:.2f}")
    print(f"Upper limit: {upper_limit:.2f}")

    outliers = []

    for value in elapsed_times:
        if value < lower_limit or value > upper_limit:
            outliers.append(value)

    print("Potential outliers:", outliers)