
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Find the project directory
project_dir = Path(__file__).resolve().parents[1]

# Define the CSV file location
csv_path = project_dir / "data" / "noise_residential_2025_pilot.csv"

# Load the CSV file into Pandas
df = pd.read_csv(csv_path)

print("DATASET LOADED SUCCESSFULLY")

print("\nDataset dimensions:")
print(df.shape)

print("\nFirst five records:")
print(df.head())

print("\nDATASET INFORMATION")
df.info()

print("\nDATASET STATISTICS")
print(df.describe(include="all").T)


# Check the date range
print("\nCREATED DATE RANGE")
print("Earliest:", df["created_date"].min())
print("Latest:", df["created_date"].max())

# Count records by borough
print("\nREQUESTS BY BOROUGH")
print(df["borough"].value_counts())

# Count records by agency
print("\nREQUESTS BY AGENCY")
print(df["agency"].value_counts())

# Check for duplicate request IDs
print("\nDUPLICATE REQUEST IDS")
print(df["unique_key"].duplicated().sum())

# Convert date columns to datetime
df["created_date"] = pd.to_datetime(df["created_date"])
df["closed_date"] = pd.to_datetime(df["closed_date"])

print("\nUPDATED DATA TYPES")
print(df[["created_date", "closed_date"]].dtypes)

# Calculate elapsed time in hours
df["elapsed_hours"] = (
    df["closed_date"] - df["created_date"]
).dt.total_seconds() / 3600

print("\nCLOSURE TIME — FIRST FIVE RECORDS")
print(df[["unique_key", "borough", "elapsed_hours"]].head())

print("\nELAPSED TIME STATISTICS")
print(df["elapsed_hours"].describe())


# Create a histogram of elapsed times

plt.hist(df["elapsed_hours"], bins=10, edgecolor="black")

plt.title("Distribution of NYC 311 Closure Times")
plt.xlabel("Elapsed time (hours)")
plt.ylabel("Number of service requests")

plt.tight_layout()
plt.show()

# Count records in each histogram interval
bin_counts = pd.cut(
    df["elapsed_hours"],
    bins=10
).value_counts().sort_index()

print("\nHISTOGRAM FREQUENCY TABLE")
print(bin_counts)

# Investigate requests with long recorded closure times

long_requests = df[df["elapsed_hours"] >= 37]

print("\nREQUESTS WITH ELAPSED TIME >= 37 HOURS")
print(long_requests["borough"].value_counts())

print("\nTOTAL LONG-DURATION REQUESTS:")
print(len(long_requests))


# Compare closure times by borough

borough_analysis = df.groupby("borough")["elapsed_hours"].agg(
    ["count", "mean", "median", "min", "max"]
).round(2)

print("\nCLOSURE TIME STATISTICS BY BOROUGH")
print(borough_analysis)

# Calculate the percentage of long-duration requests by borough

long_requests = df[df["elapsed_hours"] >= 37]

long_counts = long_requests.groupby("borough").size()

borough_analysis["long_requests"] = (
    long_counts.reindex(borough_analysis.index, fill_value=0)
)

borough_analysis["long_request_percentage"] = (
    borough_analysis["long_requests"]
    / borough_analysis["count"] * 100
).round(2)

print("\nLONG-DURATION REQUESTS BY BOROUGH")
print(
    borough_analysis[
        ["count", "long_requests", "long_request_percentage"]
    ]
)
