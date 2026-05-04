# Data Validation Report

## Overview

This document describes the validation steps used to ensure data quality, correctness, and consistency in the Formula 1 Big Data Analytics Pipeline.

---

## Data Quality Checks

The following checks are applied to all datasets:

- Ensure dataset is not empty
- Validate required columns exist
- Check for null values in critical fields (Driver, Lap Time)
- Ensure lap times are greater than zero
- Verify schema consistency across processed datasets

---

## Validation Logic

Example validation code used in the pipeline:

```python
def validate_data(df):
    assert df.count() > 0, "Dataset is empty"
    assert "driver" in df.columns, "Missing driver column"
    assert "lap_time" in df.columns, "Missing lap_time column"

    # Ensure no invalid lap times
    invalid_laps = df.filter(df.lap_time <= 0).count()
    assert invalid_laps == 0, "Invalid lap times detected"