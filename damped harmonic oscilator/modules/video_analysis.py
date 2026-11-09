"""
OpenCV Video Analysis
Damped Harmonic Oscillator

Tracks a selected bob in an experimental video,
calculates its vertical displacement and detects peaks.
"""

import cv2
import numpy as np
import pandas as pd

from pathlib import Path
from scipy.signal import find_peaks


def select_video():

    video_path = input("\nEnter video file path: ").strip().strip('"')

    if not Path(video_path).is_file():
        raise FileNotFoundError("Video file not found.")

    return video_path


def open_video(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open the video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0 or total_frames <= 0:
        cap.release()
        raise ValueError("Invalid video information.")

    return cap, fps, total_frames


def select_bob(frame):

    print("\nSelect the bob using your mouse.")
    print("Draw a rectangle around the bob and press ENTER.")

    roi = cv2.selectROI(
        "Select Oscillator Bob",
        frame,
        fromCenter=False,
        showCrosshair=True
    )

    cv2.destroyWindow("Select Oscillator Bob")

    x, y, width, height = roi

    if width == 0 or height == 0:
        raise ValueError("No bob selected.")

    template = frame[
        y:y + height,
        x:x + width
    ]

    return template, (x, y, width, height)


def track_bob(video_path):

    cap, fps, total_frames = open_video(video_path)

    success, first_frame = cap.read()

    if not success:
        cap.release()
        raise ValueError("Could not read the first frame.")

    template, roi = select_bob(first_frame)

    x, y, width, height = roi

    template_gray = cv2.cvtColor(
        template,
        cv2.COLOR_BGR2GRAY
    )

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    positions = []

    previous_y = y

    frame_number = 0

    print("\nTracking bob... Press Q to stop early.")

    while True:

        success, frame = cap.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # Search near the previous bob position.
        search_margin = 100

        search_x1 = max(0, x - search_margin)
        search_y1 = max(0, previous_y - search_margin)

        search_x2 = min(
            frame_width,
            x + width + search_margin
        )

        search_y2 = min(
            frame_height,
            previous_y + height + search_margin
        )

        search_region = gray[
            search_y1:search_y2,
            search_x1:search_x2
        ]

        if (
            search_region.shape[0] < height
            or search_region.shape[1] < width
        ):
            break

        result = cv2.matchTemplate(
            search_region,
            template_gray,
            cv2.TM_CCOEFF_NORMED
        )

        _, confidence, _, location = cv2.minMaxLoc(result)

        if confidence >= 0.45:

            current_x = search_x1 + location[0]
            current_y = search_y1 + location[1]

            center_y = current_y + height / 2

            positions.append({
                "time_s": (frame_number + 1) / fps,
                "position_px": center_y,
                "tracking_confidence": confidence
            })

            previous_y = current_y

            # Display tracking rectangle.
            cv2.rectangle(
                frame,
                (current_x, current_y),
                (current_x + width, current_y + height),
                (0, 255, 0),
                2
            )

        else:

            positions.append({
                "time_s": (frame_number + 1) / fps,
                "position_px": np.nan,
                "tracking_confidence": confidence
            })

        cv2.imshow("Oscillator Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        frame_number += 1

    cap.release()
    cv2.destroyAllWindows()

    if len(positions) < 5:
        raise ValueError("Not enough video frames were tracked.")

    data = pd.DataFrame(positions)

    # Fill short tracking gaps for analysis.
    data["position_px"] = data["position_px"].interpolate(
        limit=5,
        limit_area="inside"
    )

    data = data.dropna(subset=["position_px"]).reset_index(drop=True)

    if len(data) < 5:
        raise ValueError("Too many tracking failures.")

    return data


def convert_to_amplitude(data):

    # Estimate the equilibrium position.
    equilibrium = data["position_px"].median()

    data = data.copy()

    data["displacement_px"] = (
        data["position_px"] - equilibrium
    )

    return data, equilibrium


def calibrate_scale():

    print("\n========== VIDEO CALIBRATION ==========")

    known_distance_mm = float(
        input("Enter visible scale distance (mm): ")
    )

    pixel_distance = float(
        input("Enter corresponding distance in video (pixels): ")
    )

    if known_distance_mm <= 0 or pixel_distance <= 0:
        raise ValueError("Calibration values must be positive.")

    return known_distance_mm / pixel_distance


def detect_amplitude_peaks(data, mm_per_pixel):

    data = data.copy()

    data["amplitude_mm"] = (
        data["displacement_px"].abs() * mm_per_pixel
    )

    amplitude = data["amplitude_mm"].to_numpy()

    # Find peaks in the absolute displacement.
    # A peak may occur at either extreme of the oscillation.
    peak_indices, _ = find_peaks(
        amplitude,
        prominence=max(np.ptp(amplitude) * 0.05, 0.01),
        distance=max(1, int(0.3 * len(data) / (
            data["time_s"].iloc[-1] - data["time_s"].iloc[0]
        )))
    )

    peaks = data.iloc[peak_indices][
        ["time_s", "amplitude_mm"]
    ].copy()

    peaks = peaks.reset_index(drop=True)

    return data, peaks


def calculate_video_period(peaks):

    if len(peaks) < 3:
        return None

    times = peaks["time_s"].to_numpy()

    # Absolute-displacement peaks occur approximately
    # twice per full oscillation.
    intervals = np.diff(times)

    if len(intervals) < 2:
        return None

    return float(np.mean(intervals) * 2)


def analyze_video():

    video_path = select_video()

    data = track_bob(video_path)

    data, equilibrium = convert_to_amplitude(data)

    mm_per_pixel = calibrate_scale()

    data, peaks = detect_amplitude_peaks(
        data,
        mm_per_pixel
    )

    period = calculate_video_period(peaks)

    data["displacement_mm"] = (
        data["displacement_px"] * mm_per_pixel
    )

    print("\n========== VIDEO ANALYSIS RESULTS ==========")

    print("Tracked frames:", len(data))
    print("Estimated equilibrium:", round(equilibrium, 2), "pixels")
    print("Detected amplitude peaks:", len(peaks))

    if period is not None:
        print("Estimated time period:", round(period, 5), "s")
    else:
        print("Time period: Not enough peaks detected.")

    print("\nDetected peaks:")
    print(peaks.to_string(index=False))

    Path("results").mkdir(exist_ok=True)

    data.to_csv(
        "results/video_tracking.csv",
        index=False
    )

    peaks.to_csv(
        "results/video_peaks.csv",
        index=False
    )

    print("\nSaved:")
    print("results/video_tracking.csv")
    print("results/video_peaks.csv")

    return data, peaks, period


if __name__ == "__main__":
    analyze_video()