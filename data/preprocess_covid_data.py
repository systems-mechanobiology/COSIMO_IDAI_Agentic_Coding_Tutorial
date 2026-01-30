#!/usr/bin/env python3
"""
Preprocess JHU CSSE COVID-19 data for SIR model fitting.

This script:
1. Loads the three time series CSV files (confirmed, deaths, recovered)
2. Filters for a specific country (default: Italy)
3. Extracts a time period (default: Feb 1 - May 31, 2020)
4. Computes daily new cases from cumulative data
5. Estimates active infections: I(t) = Confirmed(t) - Recovered(t) - Deaths(t)
6. Saves the result to a clean CSV file

Data source: https://github.com/CSSEGISandData/COVID-19
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional

# Configuration
DATA_DIR = Path(__file__).parent
COUNTRY = "Italy"
START_DATE = "2020-02-01"
END_DATE = "2020-05-31"
OUTPUT_FILE = "covid_italy_first_wave.csv"


def load_jhu_timeseries(filename: str) -> pd.DataFrame:
    """
    Load a JHU CSSE time series CSV file.
    
    The data format has:
    - Province/State, Country/Region, Lat, Long as the first 4 columns
    - Dates as column headers (M/D/YY format)
    - Cumulative counts as values
    
    Parameters
    ----------
    filename : str
        Name of the CSV file (not full path)
        
    Returns
    -------
    pd.DataFrame
        Raw dataframe with all countries and dates
    """
    filepath = DATA_DIR / filename
    return pd.read_csv(filepath)


def extract_country_data(df: pd.DataFrame, country: str) -> pd.Series:
    """
    Extract and aggregate time series for a specific country.
    
    Some countries (like China, Canada, Australia) have multiple rows
    for different provinces. We sum these to get the national total.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw JHU time series data
    country : str
        Country/Region name (exact match)
        
    Returns
    -------
    pd.Series
        Time series indexed by date (as string in M/D/YY format)
    """
    # Filter for the country
    country_data = df[df["Country/Region"] == country]
    
    if country_data.empty:
        raise ValueError(f"Country '{country}' not found in data")
    
    # Get date columns (everything after the first 4 metadata columns)
    date_columns = df.columns[4:]
    
    # Sum across provinces if multiple rows exist
    totals = country_data[date_columns].sum(axis=0)
    
    return totals


def parse_jhu_dates(date_strings: pd.Index) -> pd.DatetimeIndex:
    """
    Parse JHU date format (M/D/YY) to datetime.
    
    Parameters
    ----------
    date_strings : pd.Index
        Index of date strings in M/D/YY format
        
    Returns
    -------
    pd.DatetimeIndex
        Parsed datetime index
    """
    return pd.to_datetime(date_strings, format="%m/%d/%y")


def preprocess_covid_data(
    country: str = COUNTRY,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    output_file: Optional[str] = OUTPUT_FILE
) -> pd.DataFrame:
    """
    Main preprocessing function.
    
    Parameters
    ----------
    country : str
        Country to extract (default: Italy)
    start_date : str
        Start of time period (YYYY-MM-DD format)
    end_date : str
        End of time period (YYYY-MM-DD format)
    output_file : str, optional
        Output filename. If None, data is not saved.
        
    Returns
    -------
    pd.DataFrame
        Processed data with columns: date, confirmed, deaths, recovered, 
        active, daily_new_cases
    """
    print(f"Loading COVID-19 data for {country}...")
    
    # Load the three time series
    confirmed_df = load_jhu_timeseries("time_series_covid19_confirmed_global.csv")
    deaths_df = load_jhu_timeseries("time_series_covid19_deaths_global.csv")
    recovered_df = load_jhu_timeseries("time_series_covid19_recovered_global.csv")
    
    # Extract country-specific data
    confirmed = extract_country_data(confirmed_df, country)
    deaths = extract_country_data(deaths_df, country)
    recovered = extract_country_data(recovered_df, country)
    
    # Parse dates and create a combined dataframe
    dates = parse_jhu_dates(confirmed.index)
    
    df = pd.DataFrame({
        "date": dates,
        "confirmed": confirmed.values,
        "deaths": deaths.values,
        "recovered": recovered.values
    })
    
    # Filter to the specified time period
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    df = df[(df["date"] >= start) & (df["date"] <= end)].copy()
    
    if df.empty:
        raise ValueError(f"No data found for {country} between {start_date} and {end_date}")
    
    # Reset index after filtering
    df = df.reset_index(drop=True)
    
    # Compute active infections: I(t) = Confirmed - Recovered - Deaths
    df["active"] = df["confirmed"] - df["recovered"] - df["deaths"]
    
    # Compute daily new cases from cumulative confirmed
    df["daily_new_cases"] = df["confirmed"].diff()
    # First day's new cases is just the confirmed count (or 0 if we want consistency)
    df.loc[0, "daily_new_cases"] = 0
    
    # Ensure non-negative values (data corrections can cause negative diffs)
    df["daily_new_cases"] = df["daily_new_cases"].clip(lower=0)
    df["active"] = df["active"].clip(lower=0)
    
    # Convert to integer types where appropriate
    for col in ["confirmed", "deaths", "recovered", "active", "daily_new_cases"]:
        df[col] = df[col].astype(int)
    
    # Summary statistics
    print(f"\n{'='*50}")
    print(f"Summary for {country} ({start_date} to {end_date})")
    print(f"{'='*50}")
    print(f"Total days:           {len(df)}")
    print(f"Total confirmed:      {df['confirmed'].iloc[-1]:,}")
    print(f"Total deaths:         {df['deaths'].iloc[-1]:,}")
    print(f"Total recovered:      {df['recovered'].iloc[-1]:,}")
    print(f"Peak active cases:    {df['active'].max():,}")
    print(f"Peak daily new cases: {df['daily_new_cases'].max():,}")
    
    # Save if output file specified
    if output_file:
        output_path = DATA_DIR / output_file
        df.to_csv(output_path, index=False)
        print(f"\nData saved to: {output_path}")
    
    return df


if __name__ == "__main__":
    # Run preprocessing with default parameters
    df = preprocess_covid_data()
    
    # Show first and last few rows
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())
