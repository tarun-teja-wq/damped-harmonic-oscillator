
"""
Damped Harmonic Oscillator
Unified Scientific Analysis Application
Modules A-F
"""

from pathlib import Path
import shutil

from modules.comparison import get_experiment_inputs

from modules.physics import (
    natural_frequency,
    damping_ratio,
    damped_frequency,
    time_period,
    calculate_displaced_volume,
    fluid_interaction
)

from modules.manual_analysis import (
    get_manual_readings,
    analyze_manual_readings,
    save_manual_readings
)

from modules.video_analysis import analyze_video

from modules.reading_comparison import (
    compare_periods,
    display_period_comparison,
    save_period_comparison
)

from modules.experiment_comparison import (
    compare_experiments,
    display_comparison as display_experiment_comparison,
    save_comparison as save_experiment_comparison
)

from modules.graphs import generate_all_graphs

from modules.report_generator import generate_pdf_report


RESULTS_FOLDER = Path("results")


# ==========================================
# CLEAR PREVIOUS RESULTS
# ==========================================

def clear_previous_results():

    RESULTS_FOLDER.mkdir(exist_ok=True)

    for item in RESULTS_FOLDER.iterdir():

        if item.is_file() or item.is_symlink():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)

    print("\nPrevious experiment results cleared.")


# ==========================================
# RESET EXPERIMENT DATA
# ==========================================

def reset_experiment_data():

    return {
        "experiment": None,
        "physics_results": None,
        "manual_readings": None,
        "manual_results": None,
        "video_readings": None,
        "video_peaks": None,
        "video_period": None,
        "comparison": None,
        "experiment_comparison": None,
        "graph_paths": []
    }


# ==========================================
# PHYSICS ANALYSIS
# ==========================================

def analyze_physics(experiment):

    mass = experiment["mass_kg"]
    spring = experiment["spring_constant"]
    density = experiment["fluid_density"]

    frequency = natural_frequency(mass, spring)
    period = time_period(frequency)

    volume = calculate_displaced_volume(
        experiment["shape"],
        **experiment["dimensions"]
    )

    fluid_results = fluid_interaction(
        mass,
        density,
        volume
    )

    damping = float(
        input("\nEnter damping coefficient (N.s/m): ")
    )

    if damping < 0:
        raise ValueError("Damping cannot be negative.")

    zeta = damping_ratio(
        mass,
        spring,
        damping
    )

    results = {
        "Natural frequency (Hz)": frequency,
        "Natural period (s)": period,
        "Damping coefficient (N.s/m)": damping,
        "Damping ratio": zeta,
        "Displaced volume (m³)": volume,
        "Actual weight (N)": fluid_results["actual_weight_N"],
        "Buoyant force (N)": fluid_results["buoyant_force_N"],
        "Apparent weight (N)": fluid_results["apparent_weight_N"]
    }

    if zeta < 1:

        fd = damped_frequency(
            mass,
            spring,
            damping
        )

        results["Damped frequency (Hz)"] = fd
        results["Damped period (s)"] = time_period(fd)

        results["Damping condition"] = "Underdamped"

    elif zeta == 1:

        results["Damping condition"] = "Critically damped"

    else:

        results["Damping condition"] = "Overdamped"

    return results


# ==========================================
# DISPLAY PHYSICS RESULTS
# ==========================================

def display_physics_results(results):

    print("\n========== PHYSICS RESULTS ==========")

    for key, value in results.items():

        if isinstance(value, (int, float)):
            print(f"{key}: {value:.6f}")

        else:
            print(f"{key}: {value}")


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    RESULTS_FOLDER.mkdir(exist_ok=True)

    data = reset_experiment_data()

    print("\n========================================")
    print("   DAMPED HARMONIC OSCILLATOR ANALYZER")
    print("========================================")

    while True:

        print("\n========== MAIN MENU ==========")

        print("1. Configure NEW experiment")
        print("2. Enter manual readings")
        print("3. Analyze experimental video")
        print("4. Compare manual and video periods")
        print("5. Compare shapes, masses and mediums")
        print("6. Generate scientific graphs")
        print("7. Generate PDF report")
        print("8. Clear previous results")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        try:

            # ----------------------------------
            # OPTION 1: NEW EXPERIMENT
            # ----------------------------------

            if choice == "1":

                confirm = input(
                    "\nStart a new experiment and clear old results? (yes/no): "
                ).strip().lower()

                if confirm not in ("yes", "y"):

                    print("New experiment cancelled.")
                    continue

                clear_previous_results()

                data = reset_experiment_data()

                data["experiment"] = get_experiment_inputs()

                data["physics_results"] = analyze_physics(
                    data["experiment"]
                )

                display_physics_results(
                    data["physics_results"]
                )

            # ----------------------------------
            # OPTION 2: MANUAL READINGS
            # ----------------------------------

            elif choice == "2":

                data["manual_readings"] = get_manual_readings()

                data["manual_results"] = analyze_manual_readings(
                    data["manual_readings"]
                )

                save_manual_readings(
                    data["manual_readings"]
                )

                # New readings invalidate previous comparison
                data["comparison"] = None

            # ----------------------------------
            # OPTION 3: VIDEO ANALYSIS
            # ----------------------------------

            elif choice == "3":

                (
                    data["video_readings"],
                    data["video_peaks"],
                    data["video_period"]
                ) = analyze_video()

                # New video invalidates previous comparison
                data["comparison"] = None

            # ----------------------------------
            # OPTION 4: MANUAL VS VIDEO
            # ----------------------------------

            elif choice == "4":

                if data["manual_results"] is None:

                    print("Enter manual readings first.")
                    continue

                if data["video_period"] is None:

                    print("Analyze a video first.")
                    continue

                data["comparison"] = compare_periods(
                    data["manual_results"],
                    data["video_period"]
                )

                display_period_comparison(
                    data["comparison"]
                )

                save_period_comparison(
                    data["comparison"]
                )

            # ----------------------------------
            # OPTION 5: EXPERIMENT COMPARISON
            # ----------------------------------

            elif choice == "5":

                data["experiment_comparison"] = (
                    compare_experiments()
                )

                display_experiment_comparison(
                    data["experiment_comparison"]
                )

                save_experiment_comparison(
                    data["experiment_comparison"]
                )

            # ----------------------------------
            # OPTION 6: SCIENTIFIC GRAPHS
            # ----------------------------------

            elif choice == "6":

                if data["manual_readings"] is None:

                    print("Enter manual readings first.")
                    continue

                data["graph_paths"] = generate_all_graphs(
                    readings=data["manual_readings"],
                    video_readings=data["video_readings"],
                    video_peaks=data["video_peaks"],
                    comparison=data["comparison"]
                )

                print("\nGenerated graph files:")

                for graph in data["graph_paths"]:
                    print(" -", graph)

            # ----------------------------------
            # OPTION 7: PDF REPORT
            # ----------------------------------

            elif choice == "7":

                if data["experiment"] is None:

                    print("Configure an experiment first.")
                    continue

                generate_pdf_report(
                    experiment=data["experiment"],
                    physics_results=data["physics_results"],
                    manual_readings=data["manual_readings"],
                    video_readings=data["video_readings"],
                    comparison=data["comparison"],
                    experiment_comparison=data["experiment_comparison"],
                    graph_paths=data["graph_paths"]
                )

            # ----------------------------------
            # OPTION 8: CLEAR RESULTS
            # ----------------------------------

            elif choice == "8":

                confirm = input(
                    "\nDelete ALL files inside results? (yes/no): "
                ).strip().lower()

                if confirm in ("yes", "y"):

                    clear_previous_results()

                    data = reset_experiment_data()

                    print("All experiment data cleared.")

                else:

                    print("Deletion cancelled.")

            # ----------------------------------
            # OPTION 0: EXIT
            # ----------------------------------

            elif choice == "0":

                print("\nApplication closed.")
                break

            else:

                print("\nInvalid choice. Try again.")

        except Exception as error:

            print("\n========== ERROR ==========")
            print(error)
            print("Check the entered values and try again.")


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()
