import numpy as np
from force import force_function
from build_grid import build_grid

def random_fuction(n):
    return np.random.normal(0,1.0,size=(n,2))

# Grid dimension

cut_off = 1.5
no_of_rows = 10
grid_length = no_of_rows * cut_off
N = 10 # number of particles

cell_list = np.zeros((no_of_rows**2,), dtype=np.int32)
particle_list = np.zeros((N,), dtype=np.int32)

# Time axis settings

dt = 1.0  
steps = 100

# Initial conditions - particles

position = np.random.uniform(low=-grid_length/2, high=grid_length/2, size=(N, 2))
position = position % grid_length

momentum = np.zeros((N,2), dtype=np.float64)
type_of_particle = np.zeros((N,), dtype=np.int32)


# Initial conditions - forces

force_matrix = np.array([[1.5]], dtype=np.float64)

build_grid(cell_list, particle_list, N, no_of_rows, position, cut_off)

force = force_function(
    positions=position,
    types=type_of_particle,
    force_matrix=force_matrix,
    r_c=cut_off,
    grid_length=grid_length,
    cell_list=cell_list,
    particle_list=particle_list,
    no_of_rows=no_of_rows
)

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

    position = position % grid_length # PBC - moving everything into one plane
    
    build_grid(cell_list, particle_list, N, no_of_rows, position, cut_off)

    force = force_function(
                positions=position,
                types=type_of_particle,
                force_matrix=force_matrix,
                r_c=cut_off,
                grid_length=grid_length,
                cell_list=cell_list,
                particle_list=particle_list,
                no_of_rows=no_of_rows
            )
    
    momentum += 0.5*force*dt

    if step % 2 == 0:
        print(f"t = {step * dt:.2f}")
        print(f"Position: {position}")
        print(f"Momentum: {momentum}\n")
