import numpy as np

def force_function(r):
    k = 1.5
    return -k * r

# Initial conditions

position = np.array([1.0, 1.0], dtype=np.float64)
velocity = np.array([0.0, 0.0], dtype=np.float64)

# Time axis settings

time_max = 10.0
dt = 1.0  
steps = int(time_max / dt)

force = force_function(position)
velocity += 0.5 * force * dt

# Main loop

for step in range(steps):
    position += velocity * dt
    force = force_function(position)
    velocity += force * dt

    if step % 2 == 0:
        print(f"t = {step * dt:.2f}")
        print(f"Position: {position}")
        print(f"Velocity: {velocity}\n")
