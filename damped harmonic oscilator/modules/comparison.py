"""
Experiment Configuration and Comparison Module
"""

FLUIDS = ["air", "water", "shampoo_water"]
SHAPES = ["sphere", "disc", "cylinder", "cuboid"]


def get_positive_input(prompt):
    value = float(input(prompt))

    if value <= 0:
        raise ValueError("Value must be positive.")

    return value


def get_experiment_inputs():

    print("\n===== DAMPED OSCILLATOR EXPERIMENT =====")

    experiment_name = input("Experiment name: ").strip()

    mass = get_positive_input("Mass (grams): ") / 1000

    spring_constant = get_positive_input(
        "Spring constant (N/m): "
    )

    shape = input(
        "Shape (sphere/disc/cylinder/cuboid): "
    ).strip().lower()

    fluid = input(
        "Medium (air/water/shampoo_water): "
    ).strip().lower()

    if shape not in SHAPES:
        raise ValueError("Invalid shape.")

    if fluid not in FLUIDS:
        raise ValueError("Invalid medium.")

    temperature = float(input("Fluid temperature (°C): "))

    print("\nEnter fluid density in kg/m³.")
    print("Approximate reference values: air 1.225, water 1000.")
    print("For shampoo mixture, enter a measured or estimated value.")

    if fluid == "air":
        default_density = 1.225
    elif fluid == "water":
        default_density = 1000.0
    else:
        default_density = 1030.0

    print("Reference value:", default_density, "kg/m³")

    density = get_positive_input("Enter fluid density: ")

    dimensions = {}

    print("\nEnter object dimensions in millimetres.")

    if shape in ("sphere", "disc", "cylinder"):
        dimensions["radius"] = get_positive_input(
            "Radius (mm): "
        ) / 1000

    if shape == "sphere":
        fraction = float(input("Submerged fraction (0 to 1): "))

        if not 0 < fraction <= 1:
            raise ValueError("Fraction must be above 0 and at most 1.")

        dimensions["submerged_fraction"] = fraction

    elif shape == "disc":
        dimensions["thickness"] = get_positive_input(
            "Thickness (mm): "
        ) / 1000

    elif shape == "cylinder":
        dimensions["submerged_height"] = get_positive_input(
            "Submerged height (mm): "
        ) / 1000

    elif shape == "cuboid":
        dimensions["length"] = get_positive_input(
            "Length (mm): "
        ) / 1000

        dimensions["width"] = get_positive_input(
            "Width (mm): "
        ) / 1000

        dimensions["submerged_height"] = get_positive_input(
            "Submerged height (mm): "
        ) / 1000

    return {
        "experiment_name": experiment_name,
        "mass_kg": mass,
        "spring_constant": spring_constant,
        "shape": shape,
        "fluid": fluid,
        "fluid_density": density,
        "temperature": temperature,
        "dimensions": dimensions
    }


def compare_trials(first_period, second_period):

    if first_period <= 0 or second_period <= 0:
        raise ValueError("Periods must be positive.")

    difference = second_period - first_period

    return {
        "period_difference": difference,
        "percentage_change": difference / first_period * 100
    }