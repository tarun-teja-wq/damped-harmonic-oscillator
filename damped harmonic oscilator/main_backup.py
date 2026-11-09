"""
Damped Harmonic Oscillator Analyzer
Main Application
"""

from modules.comparison import get_experiment_inputs

from modules.physics import (
    natural_frequency,
    damping_ratio,
    damped_frequency,
    time_period,
    calculate_displaced_volume,
    fluid_interaction
)


def main():

    experiment = get_experiment_inputs()

    mass = experiment["mass_kg"]
    spring_constant = experiment["spring_constant"]
    density = experiment["fluid_density"]

    print("\n========== EXPERIMENT DETAILS ==========")

    print("Experiment:", experiment["experiment_name"])
    print("Mass:", mass, "kg")
    print("Shape:", experiment["shape"])
    print("Medium:", experiment["fluid"])
    print("Spring constant:", spring_constant, "N/m")
    print("Temperature:", experiment["temperature"], "°C")
    print("Fluid density:", density, "kg/m³")

    print("\n========== OSCILLATION ANALYSIS ==========")

    fn = natural_frequency(mass, spring_constant)

    print("Natural frequency:", round(fn, 5), "Hz")
    print("Natural period:", round(time_period(fn), 5), "s")

    print("\n========== FLUID ANALYSIS ==========")

    volume = calculate_displaced_volume(
        experiment["shape"],
        **experiment["dimensions"]
    )

    result = fluid_interaction(
        mass,
        density,
        volume
    )

    print("Displaced volume:", volume, "m³")
    print("Actual weight:", result["actual_weight_N"], "N")
    print("Buoyant force:", result["buoyant_force_N"], "N")
    print("Apparent weight:", result["apparent_weight_N"], "N")

    if result["apparent_weight_N"] < 0:
        print("Note: Buoyancy exceeds weight; the object may float.")

    print("\n========== DAMPING ANALYSIS ==========")

    damping = float(
        input("Enter damping coefficient (N.s/m): ")
    )

    if damping < 0:
        raise ValueError("Damping coefficient cannot be negative.")

    zeta = damping_ratio(
        mass,
        spring_constant,
        damping
    )

    print("Damping ratio:", round(zeta, 5))

    if zeta < 1:
        fd = damped_frequency(
            mass,
            spring_constant,
            damping
        )

        print("Damped frequency:", round(fd, 5), "Hz")
        print("Damped period:", round(time_period(fd), 5), "s")

    elif zeta == 1:
        print("Critical damping: no oscillation.")

    else:
        print("Overdamped: no oscillation.")

    print("\n========== ANALYSIS COMPLETED ==========")


if __name__ == "__main__":
    main()