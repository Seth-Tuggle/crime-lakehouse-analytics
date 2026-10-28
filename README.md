# Chicago / Washington DC Crime Analytics

CS440 analytical SQL and Python plotting code for comparing Chicago and
Washington, D.C. crime patterns. It includes offense-location plots, weekday/hour
heatmaps, population-adjusted comparisons, and category distributions.

## Files

- `OperationTables.sql`: recovered lakehouse analytical tables/queries.
- `crime_visualization.py`: Spark-backed pandas/matplotlib plots.
- `helpers/dc_dashboard.py`: supporting CS443 pandas filtering and summary helpers.

## Runtime and data requirements

Install `requirements.txt`. The plotting module expects a Spark/Databricks session
named `spark` and tables under `crime_lakehouse.analysis`. In a notebook, import
the module and assign your existing session (for example, `plots.spark = spark`)
before invoking its plotting functions. Read the SQL first: the upstream ingestion
and all source-table definitions are not fully recovered here.

Use appropriately sourced Chicago and DC public crime datasets and document their
versions when recreating the tables. No raw incident records or personal datasets
are uploaded in this snapshot. Plot titles describe the original 2025 exercise
and should be updated when using different data. Population adjustment and offense
grouping are exploratory choices, not causal or policy conclusions.

Recovery corrected a string bitwise-AND expression in `load_coordinates()` to a
single Spark SQL filter. No Spark/cloud queries or plots were executed during recovery.

See `RECOVERY_NOTES.md` for snapshot provenance.
