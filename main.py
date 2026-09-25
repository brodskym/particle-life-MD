import sys
import numpy as np
from vispy import app
from vispy.color import ColorArray
from PyQt6.QtWidgets import QApplication

from force import force_function
from build_grid import build_grid
from ui import SimulationWindow
from force_matrix_suggestions import cell_interaction_matrix, slime_interaction_matrix, snake_interaction_matrix, spiral_galaxy_interaction_matrix

def random_function(n):
    return np.random.normal(0, 1.0, size=(n, 2))

class ParticleSimulation:
    def __init__(self):
        # Physics Parameters
        self.cut_off = 10.0
        self.no_of_rows = 4 
        self.grid_length = self.no_of_rows * self.cut_off
        self.N = 2500 # Number of particles

        self.dt = 0.001
        self.m = 1.0
        self.gamma = 10.0
        self.gamma_noise = 0.0
        self.k_B = 1.0
        self.T = 1.0
        self.beta = 1.0

        # State Arrays
        self.cell_list = np.zeros((self.no_of_rows**2,), dtype=np.int32)
        self.particle_list = np.zeros((self.N,), dtype=np.int32)
        self.momentum = np.zeros((self.N, 2), dtype=np.float64)

        #  Initial Conditions
        self.position = np.random.uniform(low=-self.grid_length/2, high=self.grid_length/2, size=(self.N, 2))
        self.position = self.position % self.grid_length

        self.no_of_types = 3
        self.type_of_particle = np.random.randint(0, self.no_of_types, size=self.N, dtype=np.int32)
        
        self.force_matrix = slime_interaction_matrix

        #self.force_matrix = np.array([
        #   [0.4,  -0.8,  -0.1],
        #    [ -0.7, 1.0, -0.7],
        #    [ 0.6, -0.2, 0.1]
        #], dtype=np.float64)

        # Bootstrap the First Frame
        build_grid(self.cell_list, self.particle_list, self.N, self.no_of_rows, self.position, self.cut_off)
        self.force = force_function(
            positions=self.position, types=self.type_of_particle, force_matrix=self.force_matrix,
            r_c=self.cut_off, grid_length=self.grid_length, cell_list=self.cell_list,
            particle_list=self.particle_list, no_of_rows=self.no_of_rows, beta=self.beta
        )

        # Integration Constants
        self.A = np.exp(-self.gamma * self.dt)
        self.A_2 = np.exp(-self.gamma_noise * self.dt)
        self.B = np.sqrt((1 - self.A**2) * self.k_B * self.T * self.m)

        # Colors (Mapped to the 2 types)
        self.color_palette = np.array([
            [1.0, 0.2, 0.2, 1.0], # Red
            [0.2, 1.0, 0.2, 1.0], # Green
            [0.2, 0.5, 1.0, 1.0], # Blue
        ], dtype=np.float32)
        self.particle_colors = ColorArray(self.color_palette[self.type_of_particle])

        # Rendering & Timing Variables
        self.window = None
        self.timer = app.Timer('auto', connect=self.update, start=False)
    
    def update_gammas(self, new_gamma, new_gamma_noise):
        self.gamma = new_gamma
        self.gamma_noise = new_gamma_noise
        
        self.A = np.exp(-self.gamma * self.dt)
        self.A_2 = np.exp(-self.gamma_noise * self.dt)
        
        self.B = np.sqrt((1 - self.A**2) * self.k_B * self.T * self.m)

    def toggle_timer(self, is_paused):
        if is_paused:
            self.timer.stop()
        else:
            self.timer.start()

    def update(self, ev):
        self.momentum += 0.5 * self.force * self.dt
        self.position += 0.5 * self.momentum / self.m * self.dt
        self.momentum *= self.A * self.A_2
        self.momentum += self.B * random_function(self.N)
        self.position += 0.5 * self.momentum / self.m * self.dt

        self.position = self.position % self.grid_length 
        
        build_grid(self.cell_list, self.particle_list, self.N, self.no_of_rows, self.position, self.cut_off)

        self.force = force_function(
            positions=self.position, types=self.type_of_particle, force_matrix=self.force_matrix,
            r_c=self.cut_off, grid_length=self.grid_length, cell_list=self.cell_list,
            particle_list=self.particle_list, no_of_rows=self.no_of_rows, beta=self.beta
        )
        
        self.momentum += 0.5 * self.force * self.dt

        if self.window is not None:
            self.window.markers.set_data(
                pos=self.position.astype(np.float32), 
                face_color=self.particle_colors, 
                size=4, 
                edge_width=0
            ) # type: ignore

def main():
    app.use_app('pyqt6')
    qt_app = QApplication(sys.argv)

    sim = ParticleSimulation()
    
    sim.window = SimulationWindow(
        grid_length=sim.grid_length, 
        force_matrix=sim.force_matrix, 
        no_of_types=sim.no_of_types,
        pause_callback=sim.toggle_timer,
        color_palette=sim.color_palette,
        gamma_init=sim.gamma,             
        gamma_noise_init=sim.gamma_noise, 
        gamma_callback=sim.update_gammas  
    )

    sim.window.show()
    
    sim.timer.start()

    app.run()

if __name__ == '__main__':
    main()
