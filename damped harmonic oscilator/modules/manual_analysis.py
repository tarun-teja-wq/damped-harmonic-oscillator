
"""
Manual Experimental Analysis
Damped Harmonic Oscillator

Based on the actual laboratory procedure:
Measure the total time for 10 or 20 oscillations.
"""

import pandas as pd
from pathlib import Path


def get_manual_readings():

    print("\n========== MANUAL EXPERIMENTAL READINGS ==========")

    number_of_trials = int(
        input("Number of trials: ")
    )

    if number_of_trials < 1:
        raise ValueError("At least one trial is required.")

    readings = []

    for i in range(number_of_trials):

        print(f"\n========== TRIAL {i + 1} ==========")

        oscillations = int(
            input("Number of oscillations (10 or 20): ")
        )

        if oscillations not in (10, 20):
            raise ValueError("Enter either 10 or 20 oscillations.")

        total_time = float(
            input("Total time taken (seconds): ")
        )

        if total_time <= 0:
            raise ValueError("Time must be positive.")

        period = total_time / oscillations

        readings.append({
            "trial": i + 1,
            "oscillations": oscillations,
            "total_time_s": total_time,
            "period_s": period
        })

    return pd.DataFrame(readings)


def analyze_manual_readings(readings):

    if readings.empty:
        raise ValueError("No readings available.")

    periods = readings["period_s"]

    average_period = periods.mean()

    standard_deviation = (
        periods.std(ddof=1)
        if len(periods) > 1
        else 0.0
    )

    maximum_period = periods.max()
    minimum_period = periods.min()

    frequency = 1 / average_period

    results = {
        "number_of_trials": len(readings),
        "average_period_s": average_period,
        "standard_deviation_s": standard_deviation,
        "maximum_period_s": maximum_period,
        "minimum_period_s": minimum_period,
        "experimental_frequency_Hz": frequency
    }

    print("\n========== MANUAL ANALYSIS RESULTS ==========")

    print(readings.to_string(index=False))

    print("\nAverage time period:",
          round(average_period, 5), "s")

    print("Standard deviation:",
          round(standard_deviation, 5), "s")

    print("Experimental frequency:",
          round(frequency, 5), "Hz")

    print("\nNote: Amplitude decay and experimental damping")
    print("cannot be calculated from timing readings alone.")

    return results


def save_manual_readings(readings):

    Path("results").mkdir(exist_ok=True)

    filename = "results/manual_readings.csv"

    readings.to_csv(filename, index=False)

    print("\nManual readings saved to:", filename)
