# HDB Resale Flat Data Engineering Technical Test

## Overview

This project implements a Python-based ETL pipeline for HDB resale flat transaction data from data.gov.sg.

The objective is to extract, profile, clean, and transform HDB resale data covering January 2012 to December 2016.

The source files are processed programmatically and the raw downloaded datasets are retained without manual modification.

---

## Project Structure

```text
hdb_technical_test/
│
├── main.py
├── extract.py
│
├── data/
│   ├── raw/
│   │   ├── dataset_1.csv
│   │   ├── dataset_2.csv
│   │   ├── dataset_3.csv
│   │   ├── dataset_4.csv
│   │   └── dataset_5.csv
│   │
│   ├── edited/
│   │   ├── dataset_edited_1.csv
│   │   └── dataset_edited_5.csv
│   │
│   ├── cleaned/
│   │   └── master_dataset.csv
│   │
│   ├── transformed/
│   │   └── transformed_dataset.csv
│   │
│   └── quarantined/
│       └── quarantined_dataset.csv
│
├── profiling/
│   ├── report_1.html
│   ├── report_2.html
│   ├── report_3.html
│   ├── report_4.html
│   ├── report_5.html
│   └── report_master.html
│
├── notebooks/
│   └── hdb_pipeline.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

The exact Python script names may differ depending on the final implementation.

---

## Environment Setup

### Python Virtual Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Example dependencies:

```text
pandas
requests
ydata-profiling
jupyter
```

---

## Running the Pipeline

The complete pipeline can be executed through:

```bash
python main.py
```

`main.py` acts as the orchestration layer and invokes the individual ETL stages in sequence.

The current processing flow is:

```text
data.gov.sg
     ↓
Extraction
     ↓
Raw CSV files
     ↓
Data Profiling
     ↓
Schema Normalisation
     ↓
Master Dataset
     ↓
Remaining Lease Calculation
     ↓
Duplicate Detection
     ↓
Transformed / Quarantined Data
```

---

# Data Extraction

Dataset metadata is obtained programmatically from the data.gov.sg Collection API using collection ID:

```text
189
```

The collection metadata provides the child dataset IDs.

For each dataset ID, the data.gov.sg download API is called to obtain a temporary download URL.

The CSV file is then downloaded using `requests`.

Example processing sequence:

```text
Collection ID
    ↓
Collection Metadata API
    ↓
Child Dataset IDs
    ↓
Dataset Download API
    ↓
S3 Download URL
    ↓
Raw CSV files
```

The downloaded files are stored under:

```text
hdb_technical_test/data/raw/
```

The raw source files are retained without manual modification.

---

# Data Profiling

Data profiling is performed using `ProfileReport`.

A profiling report is generated for each source dataset.

Example output:

```text
profiling/report_1.html
profiling/report_2.html
profiling/report_3.html
profiling/report_4.html
profiling/report_5.html
```

A further profiling report is generated after the datasets are combined:

```text
profiling/report_master.html
```

The profiling reports are used to review:

- column types
- missing values
- distinct values
- distributions
- correlations
- duplicate records
- potential data quality issues

---

# Dataset Schema Normalisation

Profiling identified that some source datasets contain an existing:

```text
remaining_lease
```

column while other datasets do not.

The existing column is removed from the relevant working copies so that remaining lease can be recalculated consistently for all records using the same business rule.

The original files under:

```text
data/raw/
```

are not modified.

Edited working copies are stored under:

```text
data/edited/
```

The following datasets are then combined:

```text
dataset_edited_1.csv
dataset_2.csv
dataset_3.csv
dataset_4.csv
dataset_edited_5.csv
```

using:

```python
pd.concat(
    datasets,
    ignore_index=True,
    sort=False
)
```

The resulting combined dataset is stored as:

```text
data/cleaned/master_dataset.csv
```

---

# Data Quality Validation

The following additional validation checks can be applied:

- **Missing value validation**  
  Check critical fields such as `month`, `town`, `flat_type`, `block`, `floor_area_sqm`, `lease_commence_date`, and `resale_price` for null or missing values.

- **Numeric value validation**  
  Validate that numeric fields such as `resale_price` and `floor_area_sqm` contain positive values and do not contain invalid negative or zero values.
  Check `floor_area_sqm` to be in the correct unit measures, and not in square feet or square centimeters.

- **Lease validation**  
  Ensure that `lease_commence_date` is not later than the transaction year and that the calculated remaining lease falls within the expected range of 0 to 99 years.

- **Schema consistency validation**  
  Check that the expected columns and data types are consistent across the source datasets before they are combined into the master dataset.

- Records that fail validation checks should be flagged for review and can be placed in the **Quarantined** output rather than being silently discarded.

---

### Outputs

Retained records:

```text
data/transformed/transformed_dataset.csv
```

Duplicate records:

```text
data/quarantined/quarantined_dataset.csv
```

Duplicate records are retained for traceability instead of being silently discarded.

---

# Output Datasets

The project produces the following logical output groups.

## Raw

Original files downloaded from data.gov.sg.

```text
data/raw/
```

## Cleaned

Combined dataset after schema normalisation.

```text
data/cleaned/
```

## Transformed

Dataset after remaining lease calculation and duplicate handling.

```text
data/transformed/
```

## Quarantined

Records requiring review, including lower-priced duplicate records and potential anomalous records.

```text
data/quarantined/
```

---

# Key Assumptions

1. `month` follows the `YYYY-MM` format.

2. HDB lease duration is assumed to be 99 years.

3. Because only the lease commencement year is supplied, leases are assumed to commence in January of that year.

4. Existing source `remaining_lease` values are excluded from the working dataset and recalculated consistently.

5. The original downloaded datasets are preserved in the Raw layer.

6. Duplicate resolution keeps the highest resale price where all other composite-key attributes match.

7. Statistical resale-price anomalies are treated as records requiring review and not automatically assumed to be incorrect.

---

# Software Engineering Considerations

The pipeline is separated into Python modules so individual stages can be developed, tested and maintained independently.

`main.py` provides a single execution entry point for the workflow.

Other engineering considerations include:

- Python virtual environment
- dependency management through `requirements.txt`
- separation of raw and processed data
- preservation of source files
- modular Python scripts
- deterministic transformations
- quarantining rather than silently discarding duplicate records
- reproducible execution

---

# Known Limitations / Future Improvements

The following enhancements may be considered:

- automated unit tests for validation rules
- structured logging instead of `print()`
- configuration file for collection IDs and paths
- retry handling for external API calls
- schema validation before concatenation
- automatic creation of output directories
- summary metrics for transformed and quarantined records
- additional anomaly detection rules

