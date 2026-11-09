
"""
Scientific Graph Generation
Damped Harmonic Oscillator
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path


RESULTS_FOLDER = Path("results")
RESULTS_FOLDER.mkdir(exist_ok=True)


def save_figure(filename):

    path = RESULTS_FOLDER / filename

    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Graph saved:", path)

    return str(path)


def clear_old_graphs():

    old_graphs = [
        "time_vs_oscillations.png",
        "period_vs_trial.png",
        "frequency_vs_trial.png",
        "video_displacement_vs_time.png",
        "video_amplitude_decay.png",
        "manual_vs_video_period.png"
    ]

    for filename in old_graphs:

        path = RESULTS_FOLDER / filename

        if path.exists():
            path.unlink()


# GRAPH 1: TOTAL TIME VS NUMBER OF OSCILLATIONS

def time_vs_oscillations_graph(readings):

    plt.figure(figsize=(9, 5))

    x = readings["oscillations"]
    y = readings["total_time_s"]

    plt.scatter(
        x, y,
        s=65,
        label="Experimental readings"
    )

    # Linear trend line
    if len(readings) >= 2:

        slope, intercept = __import__("numpy").polyfit(x, y, 1)

        fitted_y = slope * x + intercept

        plt.plot(
            x,
            fitted_y,
            linestyle="--",
            label=f"Best-fit slope = {slope:.4f} s"
        )

        plt.text(
            0.05,
            0.95,
            f"Experimental period (s) = {slope:.4f}",
            transform=plt.gca().transAxes,
            verticalalignment="top"
        )

    plt.xlabel("Number of Oscillations")
    plt.ylabel("Total Time (s)")
    plt.title("Total Time vs Number of Oscillations")

    plt.grid(True, alpha=0.3)
    plt.legend()

    return save_figure("time_vs_oscillations.png")


# GRAPH 2: PERIOD VS TRIAL

def period_trial_graph(readings):

    plt.figure(figsize=(9, 5))

    plt.plot(
        readings["trial"],
        readings["period_s"],
        marker="o",
        linewidth=2,
        label="Experimental time period"
    )

    average = readings["period_s"].mean()

    plt.axhline(
        average,
        linestyle="--",
        label=f"Average period = {average:.4f} s"
    )

    plt.xlabel("Trial Number")
    plt.ylabel("Time Period (s)")
    plt.title("Experimental Time Period vs Trial")

    plt.xticks(readings["trial"])
    plt.grid(True, alpha=0.3)
    plt.legend()

    return save_figure("period_vs_trial.png")


# GRAPH 3: FREQUENCY VS TRIAL

def frequency_trial_graph(readings):

    frequency = 1 / readings["period_s"]

    plt.figure(figsize=(9, 5))

    plt.plot(
        readings["trial"],
        frequency,
        marker="s",
        linewidth=2,
        label="Experimental frequency"
    )

    plt.xlabel("Trial Number")
    plt.ylabel("Frequency (Hz)")
    plt.title("Experimental Frequency vs Trial")

    plt.xticks(readings["trial"])
    plt.grid(True, alpha=0.3)
    plt.legend()

    return save_figure("frequency_vs_trial.png")


# GRAPH 4: VIDEO DISPLACEMENT VS TIME

def video_displacement_graph(video_readings):

    if video_readings is None or video_readings.empty:
        return None

    required = {"time_s", "amplitude_mm"}

    if not required.issubset(video_readings.columns):
        print("Video data missing required columns.")
        return None

    plt.figure(figsize=(10, 5))

    plt.plot(
        video_readings["time_s"],
        video_readings["amplitude_mm"],
        linewidth=1.5,
        label="Video-tracked motion"
    )

    plt.axhline(
        0,
        linestyle="--",
        alpha=0.6,
        label="Equilibrium reference"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Tracked displacement (mm)")
    plt.title("Oscillator Displacement vs Time")

    plt.grid(True, alpha=0.3)
    plt.legend()

    return save_figure("video_displacement_vs_time.png")


# GRAPH 5: VIDEO PEAK AMPLITUDE VS TIME

def video_amplitude_graph(video_peaks):

    if video_peaks is None or video_peaks.empty:
        return None

    required = {"time_s", "amplitude_mm"}

    if not required.issubset(video_peaks.columns):
        print("Video peak data missing required columns.")
        return None

    plt.figure(figsize=(9, 5))

    plt.scatter(
        video_peaks["time_s"],
        video_peaks["amplitude_mm"],
        label="Detected peak amplitudes"
    )

    plt.plot(
        video_peaks["time_s"],
        video_peaks["amplitude_mm"],
        alpha=0.6
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Peak displacement (mm)")
    plt.title("Peak Amplitude vs Time")

    plt.grid(True, alpha=0.3)
    plt.legend()

    return save_figure("video_amplitude_decay.png")


# GRAPH 6: MANUAL VS VIDEO PERIOD

def manual_video_graph(comparison):

    if comparison is None:
        return None

    manual = comparison["Manual average period (s)"]
    video = comparison["Video period (s)"]

    plt.figure(figsize=(8, 5))

    plt.bar(
        ["Manual", "Video"],
        [manual, video],
        width=0.5
    )

    plt.ylabel("Time Period (s)")
    plt.title("Manual vs Video Time Period")

    plt.grid(axis="y", alpha=0.3)

    return save_figure("manual_vs_video_period.png")


# GENERATE ALL AVAILABLE GRAPHS

def generate_all_graphs(
    readings,
    video_readings=None,
    video_peaks=None,
    comparison=None
):

    if readings is None or readings.empty:
        raise ValueError("No manual experimental readings available.")

    required_columns = {
        "trial",
        "oscillations",
        "total_time_s",
        "period_s"
    }

    if not required_columns.issubset(readings.columns):
        raise ValueError("Manual readings are missing required columns.")

    clear_old_graphs()

    print("\nGenerating scientific graphs...\n")

    graph_paths = []

    graph_paths.append(
        time_vs_oscillations_graph(readings)
    )

    graph_paths.append(
        period_trial_graph(readings)
    )

    graph_paths.append(
        frequency_trial_graph(readings)
    )

    video_graph = video_displacement_graph(video_readings)

    if video_graph:
        graph_paths.append(video_graph)

    amplitude_graph = video_amplitude_graph(video_peaks)

    if amplitude_graph:
        graph_paths.append(amplitude_graph)

    comparison_graph = manual_video_graph(comparison)

    if comparison_graph:
        graph_paths.append(comparison_graph)

    print("\n====================================")
    print("SCIENTIFIC GRAPH GENERATION COMPLETE")
    print("====================================")

    print("Total graphs generated:", len(graph_paths))

    return graph_paths
