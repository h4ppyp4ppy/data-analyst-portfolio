
# Data Source and Documentation

## Source

NYC 311 Service Requests from 2020 to Present

Official source:
https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9

Dataset ID: erm2-nwe9

## Dataset Overview

- Approximately 23.2 million records (at the time of initial research).
- 44 columns.
- Updated daily.
- Each row represents one service request.
- Data is publicly available.

## Key Fields

| Field | Description |
|---|---|
| unique_key | Unique request identifier |
| created_date | Request creation date |
| closed_date | Request closure date |
| agency | Responsible agency |
| agency_name | Full agency name |
| complaint_type | Problem category |
| descriptor | Problem detail |
| status | Request status |
| due_date | Expected update date |
| borough | Geographical area |
| open_data_channel_type | Submission channel |

## Data Access

The dataset will be accessed through the NYC Open Data API.

The project will use selected records rather than downloading the entire dataset.

