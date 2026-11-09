
"""
Manual vs Video Period Comparison
Damped Harmonic Oscillator
"""

import pandas as pd
from pathlib import Path


def compare_periods(manual_results, video_period):

    if manual_results is None:
        raise ValueError("Manual readings are not available.")

    if video_period is None or video_period <= 0:
        raise ValueError("Valid video period is not available.")

    manual_period = manual_results["average_period_s"]

    if manual_period <= 0:
        raise ValueError("Manual period must be positive.")

    absolute_difference = abs(manual_period - video_period)

    average = (manual_period + video_period) / 2

    percentage_difference = (
        absolute_difference / average
    ) * 100

    status = (
        "CHECK REQUIRED"
        if percentage_difference > 10
        else "GOOD AGREEMENT"
    )

    results = {
        "Manual average period (s)": manual_period,
        "Video period (s)": video_period,
        "Absolute difference (s)": absolute_difference,
        "Percentage difference (%)": percentage_difference,
        "Status": status
    }

    return results


def display_period_comparison(results):

    print("\n========== MANUAL VS VIDEO COMPARISON ==========")

    for key, value in results.items():

        if isinstance(value, (int, float)):
            print(f"{key}: {value:.5f}")
        else:
            print(f"{key}: {value}")


def save_period_comparison(results):

    Path("results").mkdir(exist_ok=True)

    filename = "results/manual_video_period_comparison.csv"

    dataframe = pd.DataFrame([results])

    dataframe.to_csv(filename, index=False)

    print("\nComparison saved to:", filename)
