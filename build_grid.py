from numba import njit

@njit(fastmath=True)
def get_cell_index(position_i, no_of_rows, cut_off):
    x = int(position_i[0]/cut_off)
    y = int(position_i[1]/cut_off)

    x = min(x, no_of_rows - 1)
    y = min(y, no_of_rows - 1)

    return x*no_of_rows + y

@njit(fastmath=True)
def build_grid(cell_list, particle_list, N, no_of_rows, position, cut_off):
    cell_list[:] = -1
    
    for i in range(N):
        cell_id = get_cell_index(position[i], no_of_rows, cut_off)

        particle_list[i] = cell_list[cell_id]
        cell_list[cell_id] = i
