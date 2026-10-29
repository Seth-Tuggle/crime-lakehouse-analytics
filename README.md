# Chicago / Washington DC Crime Analytics

## Historical coursework

I'm keeping this older CS440 project to explain my analysis and preserve the main
code, with a supporting helper from CS443. It was written for the class data and
Spark/Databricks environment, not as a standalone program for an individual
device. Dependencies, data sources, and service access may now be outdated or
deprecated, and I'm not maintaining a current installation path.

## About the project

My SQL and Python work explores crime patterns in Chicago and Washington, D.C.
I compare offense locations, weekday and hourly patterns, population-adjusted
rates, and offense categories.

- `OperationTables.sql`: lakehouse analysis tables and queries.
- `crime_visualization.py`: Spark-backed pandas and matplotlib plots.
- `helpers/dc_dashboard.py`: pandas filtering and summary helpers from my CS443 work.

## Original environment and limitations

The plotting code expects an existing Spark session and populated tables under
`crime_lakehouse.analysis`. The original upstream data-loading process and every
source-table definition aren't included. The SQL also contains schema names from
different class stages, so these files don't provide a complete setup for a fresh
environment.

Raw incident records and personal datasets aren't included. The plot titles refer
to the original 2025 exercise. I use population adjustment and offense grouping to
explore the data, not to establish causes or draw policy conclusions; differences
in how the cities record offenses matter when comparing results.

## Ownership

For details about my contributions and project attribution, see [CREDITS.md](CREDITS.md).
