import numpy as np
from numba import njit

@njit(fastmath=True)
def force_type(k, r, beta):
    if (r < beta):
        return k*(r/beta - 1)
    elif (r <= 1):
        return k*(1 - (r - beta)/(1 - beta))
    return 0

@njit(fastmath=True)
def force_function(positions, types, force_matrix, r_c, grid_length, cell_list, particle_list, no_of_rows, beta):
    N = positions.shape[0]
    total_forces = np.zeros((N, 2), dtype=np.float64)

    for cx in range(no_of_rows):
        for cy in range(no_of_rows):
            cell_id = cx * no_of_rows + cy
            p_i = cell_list[cell_id]
            
            while p_i != -1:
                for dx_cell in range(-1, 2):
                    for dy_cell in range(-1, 2):
                        nx = (cx + dx_cell) % no_of_rows
                        ny = (cy + dy_cell) % no_of_rows
                        neighbor_cell_id = nx * no_of_rows + ny
                        
                        p_j = cell_list[neighbor_cell_id]
                        
                        while p_j != -1:
                            
                            if p_i < p_j:
                                dx = positions[p_j, 0] - positions[p_i, 0]
                                dx = dx - grid_length * round(dx / grid_length) # PBC minium distance
                                
                                dy = positions[p_j, 1] - positions[p_i, 1]
                                dy = dy - grid_length * round(dy / grid_length) # PBC minimum distance
                                
                                distance = np.sqrt(dx**2 + dy**2)
                                
                                if 0 < distance < r_c:
                                    force_magnitude_i = force_type(k=force_matrix[types[p_i], types[p_j]], 
                                                                   beta=beta,
                                                                   r=distance)/distance
                                    force_magnitude_j = force_type(k=force_matrix[types[p_j], types[p_i]],
                                                                   beta=beta,
                                                                   r=distance)/distance
                                    
                                    total_forces[p_i, 0] += force_magnitude_i * dx 
                                    total_forces[p_i, 1] += force_magnitude_i * dy
                                    
                                    total_forces[p_j, 0] -= force_magnitude_j * dx
                                    total_forces[p_j, 1] -= force_magnitude_j * dy
                                    
                            p_j = particle_list[p_j]
                            
                p_i = particle_list[p_i]

    return total_forces

