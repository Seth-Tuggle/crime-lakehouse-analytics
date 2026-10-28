
"""
dc_dashboard.py

Simple helper functions to act like a notebook "dashboard" for D.C. crime data.
Functions operate on a pandas DataFrame and attempt to be robust to common DC crime dataset schemas.

Usage:
    from dc_dashboard import (
        prepare_df, crimes_in_ward_on_date, summary_counts_by_offense,
        top_locations, daily_trend, recent_incidents
    )
    df = prepare_df(your_dataframe_or_csv_path)
    crimes = crimes_in_ward_on_date(df, ward="2", date="2025-10-21")

The module standardizes date columns and returns pandas DataFrames for easy display in a notebook.
"""

from typing import Optional, List
import pandas as pd
from datetime import datetime

# Helper: possible date column names often found in datasets
_POSSIBLE_DATE_COLS = ["OCCURRED_ON_DATE", "OCCURRED_ON", "REPORT_DAT", "REPORT_DATE", "Date", "date", "REPORTDAT"]

def _infer_date_col(df: pd.DataFrame) -> Optional[str]:
    for c in _POSSIBLE_DATE_COLS:
        if c in df.columns:
            return c
    # fallback: find any column dtype datetime or with 'date' in name
    for c in df.columns:
        if "date" in c.lower():
            return c
    return None

def prepare_df(df_or_path, date_name="event_date") -> pd.DataFrame:
    """
    Accepts either a pandas DataFrame or a CSV/path string. Returns a DataFrame
    with a standardized datetime column named `event_date` and some common columns lowercased.
    """
    if isinstance(df_or_path, str):
        df = pd.read_csv(df_or_path)
    else:
        df = df_or_path.copy()
    # normalize column names (strip)
    df.columns = [c.strip() for c in df.columns]
    date_col = _infer_date_col(df)
    if date_col is None:
        # try to parse a column named 'timestamp' or index
        if df.index.name and "date" in (df.index.name or "").lower():
            df = df.reset_index()
            date_col = df.columns[0]
        else:
            # no date column found; leave as-is and raise a friendly error when needed
            df[date_name] = pd.NaT
            return df
    # parse date
    try:
        df[date_name] = pd.to_datetime(df[date_col], errors="coerce")
    except Exception:
        df[date_name] = pd.to_datetime(df[date_col], errors="coerce", infer_datetime_format=True)
    # convenience columns
    df["event_day"] = df[date_name].dt.date
    df["event_month"] = df[date_name].dt.to_period("M")
    # typical columns lowercased for consistency
    df_cols = {c: c.lower() for c in df.columns if c.upper() in ["OFFENSE", "OFFENSE_CODE", "OFFENSE_DESCRIPTION", "NEIGHBORHOOD", "WARD", "BLOCK", "LOCATION", "LAT", "LON", "PRECINCT", "DISTRICT", "INCIDENT_ID"]}
    df = df.rename(columns=df_cols)
    return df

def crimes_in_ward_on_date(df: pd.DataFrame, ward: str, date: str or datetime.date) -> pd.DataFrame:
    """
    Return all crimes that occurred in the given ward on the specified date.
    `date` may be a YYYY-MM-DD string or a datetime.date/datetime object.
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date).date()
    # ensure prepared
    if "event_day" not in df.columns:
        df = prepare_df(df)
    res = df[df["event_day"] == date]
    # ward column name flexible: try 'ward' or 'district'
    ward_cols = [c for c in df.columns if c.lower() == "ward" or c.lower() == "district" or c.lower().endswith("ward")]
    if ward_cols:
        col = ward_cols[0]
        res = res[res[col].astype(str) == str(ward)]
    else:
        # no ward column found; return empty with informative message
        return res.iloc[0:0]
    return res.sort_values("event_date")

def summary_counts_by_offense(df: pd.DataFrame, start_date: Optional[str]=None, end_date: Optional[str]=None) -> pd.DataFrame:
    """
    Return counts grouped by offense (or closest offense-like column) within optional date range.
    """
    if "event_date" not in df.columns:
        df = prepare_df(df)
    dff = df
    if start_date:
        dff = dff[dff["event_date"] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff["event_date"] <= pd.to_datetime(end_date)]
    # find offense column
    offense_cols = [c for c in dff.columns if "offense" in c or "offenc" in c or "crime" in c]
    if offense_cols:
        col = offense_cols[0]
    else:
        # fallback: try 'offense_code' like
        col = dff.columns[0]
    return dff.groupby(col).size().reset_index(name="count").sort_values("count", ascending=False)

def top_locations(df: pd.DataFrame, n:int=10, start_date:Optional[str]=None, end_date:Optional[str]=None) -> pd.DataFrame:
    """
    Return top N locations (by block or location text) where crimes concentrated.
    """
    if "event_date" not in df.columns:
        df = prepare_df(df)
    dff = df
    if start_date:
        dff = dff[dff["event_date"] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff["event_date"] <= pd.to_datetime(end_date)]
    loc_cols = [c for c in dff.columns if "block" in c or "location" in c or "address" in c]
    if not loc_cols:
        return dff.iloc[0:0]
    loc = loc_cols[0]
    return dff.groupby(loc).size().reset_index(name="count").sort_values("count", ascending=False).head(n)

def daily_trend(df: pd.DataFrame, offense: Optional[str]=None, ward:Optional[str]=None,
                start_date:Optional[str]=None, end_date:Optional[str]=None) -> pd.DataFrame:
    """
    Return a timeseries DataFrame with counts per day. Optionally filter by offense or ward.
    """
    if "event_date" not in df.columns:
        df = prepare_df(df)
    dff = df
    if start_date:
        dff = dff[dff["event_date"] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff["event_date"] <= pd.to_datetime(end_date)]
    if offense:
        # pick offense-like col
        offense_cols = [c for c in dff.columns if "offense" in c or "crime" in c]
        if offense_cols:
            dff = dff[dff[offense_cols[0]] == offense]
    if ward:
        ward_cols = [c for c in dff.columns if c.lower() == "ward" or c.lower() == "district" or c.lower().endswith("ward")]
        if ward_cols:
            dff = dff[dff[ward_cols[0]].astype(str) == str(ward)]
        else:
            return dff.iloc[0:0]
    ts = dff.groupby(dff["event_day"]).size().reset_index(name="count").sort_values("event_day")
    return ts

def recent_incidents(df: pd.DataFrame, n:int=10) -> pd.DataFrame:
    """
    Return the N most recent incidents (sorted by event_date desc).
    """
    if "event_date" not in df.columns:
        df = prepare_df(df)
    return df.sort_values("event_date", ascending=False).head(n)
