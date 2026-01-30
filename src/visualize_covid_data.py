#!/usr/bin/env python3
"""
Visualize COVID-19 data for Italy's first pandemic wave.

This script creates a publication-quality figure showing:
1. Cumulative confirmed cases over time
2. Active infections (estimated) over time  
3. Daily new cases as a bar chart

Key events (e.g., lockdown) are marked with vertical lines.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime

# Configuration
DATA_FILE = Path(__file__).parent.parent / "data" / "covid_italy_first_wave.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "covid_italy_overview.png"
LOCKDOWN_DATE = datetime(2020, 3, 9)  # Italy's national lockdown


def load_data(filepath: Path) -> pd.DataFrame:
    """Load preprocessed COVID-19 data."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


def create_overview_figure(df: pd.DataFrame) -> plt.Figure:
    """
    Create a three-panel figure showing COVID-19 overview for Italy.
    
    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed COVID data with columns: date, confirmed, active, daily_new_cases
        
    Returns
    -------
    plt.Figure
        The matplotlib figure object
    """
    # Use a clean style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Create figure with three subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle("COVID-19 First Wave in Italy (Feb–May 2020)", 
                 fontsize=16, fontweight='bold', y=0.98)
    
    dates = df["date"]
    
    # Color palette
    colors = {
        "confirmed": "#1f77b4",  # Blue
        "active": "#ff7f0e",      # Orange
        "daily": "#2ca02c",       # Green
        "lockdown": "#d62728"     # Red
    }
    
    # =========================================================================
    # Panel 1: Cumulative Confirmed Cases
    # =========================================================================
    ax1 = axes[0]
    ax1.fill_between(dates, df["confirmed"], alpha=0.3, color=colors["confirmed"])
    ax1.plot(dates, df["confirmed"], linewidth=2, color=colors["confirmed"])
    ax1.set_ylabel("Cumulative Cases", fontsize=11)
    ax1.set_title("Cumulative Confirmed Cases", fontsize=12, loc='left')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    
    # Add lockdown line
    ax1.axvline(LOCKDOWN_DATE, color=colors["lockdown"], linestyle='--', 
                linewidth=2, alpha=0.8, label='National Lockdown (Mar 9)')
    ax1.legend(loc='upper left', framealpha=0.9)
    
    # =========================================================================
    # Panel 2: Active Infections (Estimated)
    # =========================================================================
    ax2 = axes[1]
    ax2.fill_between(dates, df["active"], alpha=0.3, color=colors["active"])
    ax2.plot(dates, df["active"], linewidth=2, color=colors["active"])
    ax2.set_ylabel("Active Cases", fontsize=11)
    ax2.set_title("Active Infections (Confirmed − Recovered − Deaths)", 
                  fontsize=12, loc='left')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    
    # Add lockdown line
    ax2.axvline(LOCKDOWN_DATE, color=colors["lockdown"], linestyle='--', 
                linewidth=2, alpha=0.8)
    
    # Mark peak
    peak_idx = df["active"].idxmax()
    peak_date = df.loc[peak_idx, "date"]
    peak_value = df.loc[peak_idx, "active"]
    ax2.annotate(f'Peak: {peak_value:,}', 
                 xy=(peak_date, peak_value),
                 xytext=(peak_date + pd.Timedelta(days=10), peak_value * 0.85),
                 fontsize=10,
                 arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                          edgecolor='gray', alpha=0.8))
    
    # =========================================================================
    # Panel 3: Daily New Cases (Bar Chart)
    # =========================================================================
    ax3 = axes[2]
    ax3.bar(dates, df["daily_new_cases"], width=0.8, alpha=0.7, 
            color=colors["daily"], edgecolor='none')
    ax3.set_ylabel("Daily New Cases", fontsize=11)
    ax3.set_xlabel("Date", fontsize=11)
    ax3.set_title("Daily New Confirmed Cases", fontsize=12, loc='left')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    
    # Add lockdown line
    ax3.axvline(LOCKDOWN_DATE, color=colors["lockdown"], linestyle='--', 
                linewidth=2, alpha=0.8)
    
    # =========================================================================
    # Format x-axis dates
    # =========================================================================
    ax3.xaxis.set_major_locator(mdates.MonthLocator())
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax3.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    
    # Rotate date labels for readability
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=0, ha='center')
    
    # Remove top/right spines for cleaner look
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3)
    
    # Adjust layout
    plt.tight_layout()
    fig.subplots_adjust(top=0.93, hspace=0.15)
    
    return fig


def main():
    """Main function to load data and create visualization."""
    print(f"Loading data from: {DATA_FILE}")
    df = load_data(DATA_FILE)
    
    print(f"Data range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Total records: {len(df)}")
    
    print("\nCreating visualization...")
    fig = create_overview_figure(df)
    
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save figure
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nFigure saved to: {OUTPUT_FILE}")
    
    # Also display if running interactively
    plt.show()


if __name__ == "__main__":
    main()
