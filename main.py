import numpy as np
from vispy import app, scene
from vispy.color import ColorArray
from force import force_function
from build_grid import build_grid

def random_fuction(n):
    return np.random.normal(0,1.0,size=(n,2))

# Grid dimension

cut_off = 2.5
no_of_rows = 10
grid_length = no_of_rows * cut_off
N = 2500 # number of particles

cell_list = np.zeros((no_of_rows**2,), dtype=np.int32)
particle_list = np.zeros((N,), dtype=np.int32)

# Time axis settings

dt = 0.05  

# Initial conditions - particles

m = 1.0
gamma = 2.5
k_B = 1.0 # Boltzman constant in SI k_B = 1.380649e-23 J/K
T = 0

position = np.random.uniform(low=-grid_length/2, high=grid_length/2, size=(N, 2))
position = position % grid_length

momentum = np.zeros((N,2), dtype=np.float64)

no_of_types = 3
type_of_particle = np.random.randint(0, no_of_types, size=N, dtype=np.int32)


# Initial conditions - forces

force_matrix = np.array(
                [
                 [1.5, 1.0, 1.0],
                 [1.5, -1.2, 1.0],
                 [1.0, -2.0, -1.0]
                ]
                , dtype=np.float64)

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

A = np.exp(-gamma * dt)
B = np.sqrt((1-A**2) * k_B * T * m)

# --- VISPY SETUP ----

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 800))
view = canvas.central_widget.add_view()

view.camera = scene.PanZoomCamera(rect=(0, 0, grid_length, grid_length), aspect=1.0)

markers = scene.visuals.Markers(parent=view.scene)

color_palette = np.array([
    [1.0, 0.2, 0.2, 1.0], # Red
    [0.2, 1.0, 0.2, 1.0], # Green
    [0.2, 0.5, 1.0, 1.0], # Blue
], dtype=np.float32)
particle_colors = ColorArray(color_palette[type_of_particle])

# Main loop

def update(ev):
    global position, momentum, force

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

    markers.set_data(pos=position, face_color=particle_colors, size=4, edge_width=0)

timer = app.Timer('auto', connect=update, start=True)

if __name__ == '__main__':
    app.run()

