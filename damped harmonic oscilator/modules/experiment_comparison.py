
"""
Advanced Experiment Comparison
Damped Harmonic Oscillator

Medium-dependent theoretical estimates using
Stokes' drag approximation.

IMPORTANT:
The equivalent-sphere approximation is used for
non-spherical objects. Results are estimates, not
measured experimental damping values.
"""

import pandas as pd
from pathlib import Path
import math

from modules.physics import (
    natural_frequency,
    damping_ratio,
    damped_frequency,
    time_period
)


# ==========================================
# FLUID PROPERTIES
# ==========================================

FLUIDS = {
    "air": {
        "density": 1.225,
        "viscosity": 1.81e-5
    },

    "water": {
        "density": 998.2,
        "viscosity": 1.002e-3
    },

    "shampoo_water": {
        "density": 1050.0,
        "viscosity": 1.0e-2
    }
}


SHAPES = [
    "sphere",
    "disc",
    "cylinder",
    "cuboid"
]


# ==========================================
# INPUT VALIDATION
# ==========================================

def get_positive_input(prompt):

    value = float(input(prompt))

    if value <= 0:
        raise ValueError("Value must be positive.")

    return value


def get_shape_dimensions(shape):

    print("\nEnter object dimensions in millimetres.")

    if shape == "sphere":

        radius = get_positive_input("Radius (mm): ") / 1000

        return {"radius": radius}

    elif shape == "disc":

        radius = get_positive_input("Radius (mm): ") / 1000

        thickness = get_positive_input(
            "Thickness (mm): "
        ) / 1000

        return {
            "radius": radius,
            "thickness": thickness
        }

    elif shape == "cylinder":

        radius = get_positive_input("Radius (mm): ") / 1000

        height = get_positive_input(
            "Height (mm): "
        ) / 1000

        return {
            "radius": radius,
            "height": height
        }

    elif shape == "cuboid":

        length = get_positive_input(
            "Length (mm): "
        ) / 1000

        width = get_positive_input(
            "Width (mm): "
        ) / 1000

        height = get_positive_input(
            "Height (mm): "
        ) / 1000

        return {
            "length": length,
            "width": width,
            "height": height
        }


# ==========================================
# OBJECT VOLUME
# ==========================================

def calculate_volume(shape, dimensions):

    if shape == "sphere":

        r = dimensions["radius"]

        return (4 / 3) * math.pi * r**3

    elif shape == "disc":

        r = dimensions["radius"]
        h = dimensions["thickness"]

        return math.pi * r**2 * h

    elif shape == "cylinder":

        r = dimensions["radius"]
        h = dimensions["height"]

        return math.pi * r**2 * h

    elif shape == "cuboid":

        return (
            dimensions["length"]
            * dimensions["width"]
            * dimensions["height"]
        )

    raise ValueError("Unknown shape.")


# ==========================================
# EQUIVALENT SPHERE RADIUS
# ==========================================

def equivalent_radius(volume):

    return (
        (3 * volume) / (4 * math.pi)
    ) ** (1 / 3)


# ==========================================
# ESTIMATED FLUID DAMPING
# ==========================================

def estimate_damping(viscosity, radius):

    # Stokes' drag approximation for a sphere:
    # F = 6 * pi * viscosity * radius * velocity
    #
    # Therefore:
    # Damping coefficient = 6 * pi * viscosity * radius

    return 6 * math.pi * viscosity * radius


# ==========================================
# GET EXPERIMENT DETAILS
# ==========================================

def get_case_details(case_number):

    print(f"\n========== CASE {case_number} ==========")

    name = input("Case name: ").strip()

    if not name:
        name = f"Case {case_number}"

    mass = get_positive_input(
        "Mass (grams): "
    ) / 1000

    spring = get_positive_input(
        "Spring constant (N/m): "
    )

    shape = input(
        "Shape (sphere/disc/cylinder/cuboid): "
    ).strip().lower()

    if shape not in SHAPES:
        raise ValueError("Invalid shape.")

    medium = input(
        "Medium (air/water/shampoo_water): "
    ).strip().lower().replace(" ", "_")

    if medium not in FLUIDS:
        raise ValueError(
            "Invalid medium. Choose air, water or shampoo_water."
        )

    dimensions = get_shape_dimensions(shape)

    return {
        "name": name,
        "mass_kg": mass,
        "spring_constant": spring,
        "shape": shape,
        "medium": medium,
        "dimensions": dimensions
    }


# ==========================================
# ANALYZE ONE CASE
# ==========================================

def analyze_case(case):

    mass = case["mass_kg"]
    spring = case["spring_constant"]

    fluid = FLUIDS[case["medium"]]

    density = fluid["density"]
    viscosity = fluid["viscosity"]

    volume = calculate_volume(
        case["shape"],
        case["dimensions"]
    )

    radius = equivalent_radius(volume)

    damping = estimate_damping(
        viscosity,
        radius
    )

    fn = natural_frequency(
        mass,
        spring
    )

    zeta = damping_ratio(
        mass,
        spring,
        damping
    )

    buoyancy = density * volume * 9.81

    actual_weight = mass * 9.81

    apparent_weight = actual_weight - buoyancy

    if zeta < 1:

        fd = damped_frequency(
            mass,
            spring,
            damping
        )

        period = time_period(fd)

        regime = "Underdamped"

    elif zeta == 1:

        fd = None
        period = None

        regime = "Critically damped"

    else:

        fd = None
        period = None

        regime = "Overdamped"

    return {
        "case": case["name"],
        "mass_g": mass * 1000,
        "spring_constant_N_m": spring,
        "shape": case["shape"],
        "medium": case["medium"],
        "fluid_density_kg_m3": density,
        "viscosity_Pa_s": viscosity,
        "volume_m3": volume,
        "equivalent_radius_m": radius,
        "estimated_damping_N_s_m": damping,
        "natural_frequency_Hz": fn,
        "damping_ratio": zeta,
        "damped_frequency_Hz": fd,
        "damped_period_s": period,
        "actual_weight_N": actual_weight,
        "buoyant_force_N": buoyancy,
        "apparent_weight_N": apparent_weight,
        "regime": regime
    }


# ==========================================
# COMPARE EXPERIMENTS
# ==========================================

def compare_experiments():

    print("\n===== ADVANCED EXPERIMENT COMPARISON =====")

    print("\nAvailable mediums:")

    for medium in FLUIDS:
        print("-", medium)

    number_of_cases = int(
        input("\nNumber of cases to compare: ")
    )

    if number_of_cases < 2:
        raise ValueError("Enter at least two cases.")

    results = []

    for i in range(number_of_cases):

        case = get_case_details(i + 1)

        result = analyze_case(case)

        results.append(result)

    return pd.DataFrame(results)


# ==========================================
# DISPLAY RESULTS
# ==========================================

def display_comparison(comparison):

    print("\n========== COMPARISON RESULTS ==========")

    print(comparison.to_string(index=False))

    print("\n========== OBSERVATIONS ==========")

    highest_frequency = comparison.loc[
        comparison["natural_frequency_Hz"].idxmax()
    ]

    highest_damping = comparison.loc[
        comparison["estimated_damping_N_s_m"].idxmax()
    ]

    highest_buoyancy = comparison.loc[
        comparison["buoyant_force_N"].idxmax()
    ]

    print(
        "Highest natural frequency:",
        highest_frequency["case"]
    )

    print(
        "Highest estimated damping:",
        highest_damping["case"]
    )

    print(
        "Highest buoyant force:",
        highest_buoyancy["case"]
    )

    print("\nOscillation behaviour:")

    for _, row in comparison.iterrows():

        print(
            row["case"],
            "->",
            row["regime"]
        )

    print(
        "\nNOTE: Damping values are theoretical estimates."
    )


# ==========================================
# SAVE RESULTS
# ==========================================

def save_comparison(comparison):

    Path("results").mkdir(exist_ok=True)

    filename = "results/experiment_comparison.csv"

    comparison.to_csv(
        filename,
        index=False
    )

    print("\nComparison saved to:", filename)


# ==========================================
# STANDALONE EXECUTION
# ==========================================

if __name__ == "__main__":

    comparison = compare_experiments()

    display_comparison(comparison)

    save_comparison(comparison)
