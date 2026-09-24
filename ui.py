import os
from datetime import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QDoubleSpinBox, QPushButton
from vispy import scene
from vispy.io import write_png

class SimulationWindow(QWidget):
    def __init__(self, grid_length, force_matrix, no_of_types, pause_callback, color_palette, gamma_init, gamma_noise_init, gamma_callback):
        super().__init__()
        self.setWindowTitle("Particle Life")
        
        self.force_matrix = -force_matrix
        self.pause_callback = pause_callback
        self.gamma_callback = gamma_callback
        self.is_paused = False
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 10) 
        self.setLayout(main_layout)

        # VisPy Canvas Setup
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 800))
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, grid_length, grid_length), aspect=1.0)
        self.markers = scene.visuals.Markers(parent=self.view.scene)
        
        main_layout.addWidget(self.canvas.native, 1)
        
        # Interactive UI Panel Setup
        ui_panel = QWidget()
        bottom_layout = QHBoxLayout()
        ui_panel.setLayout(bottom_layout)
        
        # --- Action Buttons ---
        btn_layout = QVBoxLayout()
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        
        self.pic_btn = QPushButton("Take Picture")
        self.pic_btn.clicked.connect(self.take_picture)
        
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.pic_btn)
        bottom_layout.addLayout(btn_layout)

        gamma_layout = QGridLayout()
        
        gamma_layout.addWidget(QLabel("γ (Friction):"), 0, 0)
        self.gamma_box = QDoubleSpinBox()
        self.gamma_box.setRange(0.0, 200.0)
        self.gamma_box.setValue(gamma_init)
        self.gamma_box.valueChanged.connect(self.update_gammas)
        gamma_layout.addWidget(self.gamma_box, 0, 1)
        
        gamma_layout.addWidget(QLabel("γ_noise:"), 1, 0)
        self.gamma_noise_box = QDoubleSpinBox()
        self.gamma_noise_box.setRange(0.0, 200.0)
        self.gamma_noise_box.setValue(gamma_noise_init)
        self.gamma_noise_box.valueChanged.connect(self.update_gammas)
        gamma_layout.addWidget(self.gamma_noise_box, 1, 1)

        bottom_layout.addSpacing(15)
        bottom_layout.addLayout(gamma_layout)
        bottom_layout.addSpacing(15)
        # ---------------------------

        # --- Force Matrix Grid ---
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0) 
        grid_widget.setLayout(grid_layout)
        
        for i in range(no_of_types):
            for j in range(no_of_types):
                box = QDoubleSpinBox()
                box.setRange(-10.0, 10.0)
                box.setSingleStep(0.1)
                box.setValue(self.force_matrix[i, j])
                box.setFixedWidth(60)
                box.valueChanged.connect(lambda val, r=i, c=j: self.update_force(val, r, c))
                
                hex_i = f"#{int(color_palette[i][0]*255):02x}{int(color_palette[i][1]*255):02x}{int(color_palette[i][2]*255):02x}"
                hex_j = f"#{int(color_palette[j][0]*255):02x}{int(color_palette[j][1]*255):02x}{int(color_palette[j][2]*255):02x}"
                
                label = QLabel(f"<span style='color:{hex_i}; font-size:18pt;'>●</span> → <span style='color:{hex_j}; font-size:18pt;'>●</span>")
                
                grid_layout.addWidget(label, i, j*2)
                grid_layout.addWidget(box, i, j*2 + 1)
                
        bottom_layout.addStretch()
        bottom_layout.addWidget(grid_widget)
        bottom_layout.addStretch()
        
        main_layout.addWidget(ui_panel)
        
    def update_force(self, val, r, c):
        self.force_matrix[r, c] = val

    def update_gammas(self):
        self.gamma_callback(self.gamma_box.value(), self.gamma_noise_box.value())

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_btn.setText("Play" if self.is_paused else "Pause")
        self.pause_callback(self.is_paused)

    def take_picture(self):
        os.makedirs("screenshots", exist_ok=True)
        img = self.canvas.render()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/sim_{timestamp}.png"
        write_png(filename, img)
        print(f"Simulation saved to {filename}")
