import numpy as np
from force import force_function

def random_fuction(n):
    return np.random.normal(0,1.0,size=(n,2))

# Plane dimension

plane_size = 10.0
N = 10 # number of particles

# Time axis settings

dt = 1.0  
steps = 100

# Initial conditions - particles

position = np.random.uniform(low=-plane_size, high=plane_size, size=(N, 2))
momentum = np.zeros((N,2), dtype=np.float64)
type_of_particle = np.zeros((N,), dtype=np.int32)

# Initial conditions - forces

force_matrix = np.array([[1.5]], dtype=np.float64)
cut_off = 1.5

force = force_function(force_matrix=force_matrix, positions=position, r_c=cut_off, types=type_of_particle)
m = 1.0
gamma = 1.0
k_B = 1.0 # Boltzman constant in SI k_B = 1.380649e-23 J/K
T = 1.0

A = np.exp(-gamma * dt)
B = np.sqrt((1-A**2) * k_B * T * m)

# Main loop

for step in range(steps):
    momentum += 0.5*force*dt
    position += 0.5*momentum/m*dt
    momentum *= A
    momentum += B*random_fuction(N)
    position += 0.5*momentum/m*dt
    force = force_function(force_matrix=force_matrix, positions=position, r_c=cut_off, types=type_of_particle)
    momentum += 0.5*force*dt

    if step % 2 == 0:
        print(f"t = {step * dt:.2f}")
        print(f"Position: {position}")
        print(f"Momentum: {momentum}\n")
