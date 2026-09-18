import numpy as np

def force_function(positions, types, force_matrix, r_c):
    N = positions.shape[0]
    total_forces = np.zeros((N,2), dtype=np.float64)

    for i in range(N):
        for j in range(i):
            dx = positions[j][0]-positions[i][0]
            dy = positions[j][1]-positions[i][1]
            distance = np.sqrt(dx**2 + dy**2)

            if 0 < distance < r_c:
                force_magnitude_i = force_matrix[types[i], types[j]]/distance**3
                force_magnitude_j = force_matrix[types[j], types[i]]/distance**3

                total_forces[i, 0] += force_magnitude_i * dx 
                total_forces[i, 1] += force_magnitude_i * dy

                total_forces[j, 0] -= force_magnitude_j * dx
                total_forces[j, 1] -= force_magnitude_j * dy

    return total_forces

