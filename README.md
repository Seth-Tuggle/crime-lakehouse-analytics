# Chicago / Washington DC Crime Analytics

My CS440 project uses SQL and Python to explore crime patterns in Chicago and
Washington, D.C. I compare offense locations, weekday and hourly patterns,
population-adjusted rates, and offense categories.

## Files

- `OperationTables.sql`: lakehouse analysis tables and queries.
- `crime_visualization.py`: Spark-backed pandas and matplotlib plots.
- `helpers/dc_dashboard.py`: pandas filtering and summary helpers from my CS443 work.

## Setup and data requirements

Install `requirements.txt`. The plotting module needs a Spark or Databricks
session and tables under `crime_lakehouse.analysis`. In a notebook, import the
module and pass it your existing session before calling a plotting function:

```python
import crime_visualization as plots

plots.spark = spark
```

Review the SQL before preparing the tables. I haven't included the full upstream
ingestion process or every source-table definition, so the Python module won't
run against an empty Spark environment by itself.

Use public Chicago and DC crime datasets and record the versions you choose.
I keep raw incident records and personal datasets out of this repository. The
plot titles refer to the original 2025 exercise; update them if you use other data.

## Interpreting the plots

I use population adjustment and offense grouping to explore the data, not to
establish causes or draw policy conclusions. Differences in how the two cities
record and categorize offenses also matter when comparing results.

## Ownership

For details about my contributions and project attribution, see [CREDITS.md](CREDITS.md).
