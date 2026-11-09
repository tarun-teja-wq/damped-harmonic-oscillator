
from modules.physics import *

# Example experimental values
mass = 0.050
spring_constant = 10
damping = 0.10

print("\n===== OSCILLATOR TEST =====")

# Frequency calculations
fn = natural_frequency(mass, spring_constant)
zeta = damping_ratio(mass, spring_constant, damping)
fd = damped_frequency(mass, spring_constant, damping)

print("Natural frequency:", fn, "Hz")
print("Damping ratio:", zeta)
print("Damped frequency:", fd, "Hz")
print("Time period:", time_period(fd), "seconds")

# Sphere calculations
volume = object_volume("sphere", radius=0.01)

print("\n===== WATER ANALYSIS =====")

buoyancy = buoyant_force(1000, volume)

print("Sphere volume:", volume, "m³")
print("Buoyant force:", buoyancy, "N")
print("Apparent weight:", apparent_weight(mass, buoyancy), "N")

# Amplitude decay
print("\n===== AMPLITUDE ANALYSIS =====")

amplitude = amplitude_after_time(0.05, 0.2, 5)

print("Amplitude after 5 seconds:", amplitude, "m")
