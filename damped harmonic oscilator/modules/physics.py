"""
Physics Engine for Damped Harmonic Oscillator
"""

import math

G = 9.80665


def natural_angular_frequency(mass, spring_constant):
    if mass <= 0 or spring_constant <= 0:
        raise ValueError("Mass and spring constant must be positive.")

    return math.sqrt(spring_constant / mass)


def natural_frequency(mass, spring_constant):
    return natural_angular_frequency(mass, spring_constant) / (2 * math.pi)


def damping_ratio(mass, spring_constant, damping_coefficient):
    if mass <= 0 or spring_constant <= 0:
        raise ValueError("Mass and spring constant must be positive.")

    if damping_coefficient < 0:
        raise ValueError("Damping coefficient cannot be negative.")

    return damping_coefficient / (2 * math.sqrt(mass * spring_constant))


def damped_angular_frequency(mass, spring_constant, damping_coefficient):
    zeta = damping_ratio(mass, spring_constant, damping_coefficient)

    if zeta >= 1:
        return 0.0

    omega_n = natural_angular_frequency(mass, spring_constant)
    return omega_n * math.sqrt(1 - zeta**2)


def damped_frequency(mass, spring_constant, damping_coefficient):
    return damped_angular_frequency(
        mass, spring_constant, damping_coefficient
    ) / (2 * math.pi)


def time_period(frequency):
    if frequency <= 0:
        raise ValueError("Frequency must be positive.")

    return 1 / frequency


def object_volume(shape, **dimensions):
    if shape == "sphere":
        r = dimensions["radius"]
        return (4 / 3) * math.pi * r**3

    if shape == "cylinder":
        r = dimensions["radius"]
        h = dimensions["height"]
        return math.pi * r**2 * h

    if shape == "disc":
        r = dimensions["radius"]
        t = dimensions["thickness"]
        return math.pi * r**2 * t

    if shape == "cuboid":
        return (
            dimensions["length"]
            * dimensions["width"]
            * dimensions["height"]
        )

    raise ValueError("Unsupported object shape.")


def calculate_displaced_volume(shape, **dimensions):
    if shape == "sphere":
        volume = object_volume("sphere", **dimensions)
        fraction = dimensions.get("submerged_fraction", 1.0)

        if not 0 < fraction <= 1:
            raise ValueError("Submerged fraction must be between 0 and 1.")

        return volume * fraction

    if shape == "cylinder":
        return (
            math.pi
            * dimensions["radius"]**2
            * dimensions["submerged_height"]
        )

    if shape == "disc":
        return object_volume("disc", **dimensions)

    if shape == "cuboid":
        return (
            dimensions["length"]
            * dimensions["width"]
            * dimensions["submerged_height"]
        )

    raise ValueError("Unsupported object shape.")


def buoyant_force(fluid_density, displaced_volume):
    if fluid_density <= 0 or displaced_volume < 0:
        raise ValueError("Invalid density or displaced volume.")

    return fluid_density * displaced_volume * G


def apparent_weight(mass, buoyancy):
    return mass * G - buoyancy


def fluid_interaction(mass, fluid_density, displaced_volume):
    weight = mass * G
    buoyancy = buoyant_force(fluid_density, displaced_volume)

    return {
        "actual_weight_N": weight,
        "buoyant_force_N": buoyancy,
        "apparent_weight_N": apparent_weight(mass, buoyancy)
    }


def amplitude_after_time(initial_amplitude, decay_constant, time):
    if initial_amplitude < 0 or decay_constant < 0 or time < 0:
        raise ValueError("Amplitude, decay constant and time must be non-negative.")

    return initial_amplitude * math.exp(-decay_constant * time)