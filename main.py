import numpy as np

def force_function(r):
    k = 1.5
    return -k * r

def random_fuction(n):
    return np.random.normal(0,1.0,size=(n,2))

# Plane dimension

plane_size = 10.0
N = 100 # number of particles

# Time axis settings

dt = 1.0  
steps = 100

# Initial conditions

position = np.random.uniform(low=-plane_size, high=plane_size, size=(N, 2))
momentum = np.zeros((N,2), dtype=np.float64)
force = force_function(position)
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
    force = force_function(position)
    momentum += 0.5*force*dt

    if step % 2 == 0:
        print(f"t = {step * dt:.2f}")
        print(f"Position: {position}")
        print(f"Momentum: {momentum}\n")
