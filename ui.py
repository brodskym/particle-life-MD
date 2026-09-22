import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QDoubleSpinBox
from vispy import scene

class SimulationWindow(QWidget):
    def __init__(self, grid_length, force_matrix, no_of_types):
        super().__init__()
        self.setWindowTitle("Particle Life")
        
        self.force_matrix = force_matrix
        
        # Change to Vertical Layout: Canvas on top, UI on bottom
        main_layout = QVBoxLayout()
        # Remove margins around the canvas to give it absolute maximum space
        main_layout.setContentsMargins(0, 0, 0, 10) 
        self.setLayout(main_layout)

        # 1. VisPy Canvas Setup
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 800))
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(0, 0, grid_length, grid_length), aspect=1.0)
        self.markers = scene.visuals.Markers(parent=self.view.scene)
        
        # Add the canvas to the layout with a stretch factor of 1 so it consumes all extra space
        main_layout.addWidget(self.canvas.native, 1)
        
        # 2. Interactive UI Panel Setup
        ui_panel = QWidget()
        bottom_layout = QHBoxLayout()
        ui_panel.setLayout(bottom_layout)
        
        # Inner widget just for the grid to keep it compact
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
                
                # Force the boxes to be physically smaller so they don't bloat the bottom panel
                box.setFixedWidth(60)
                
                box.valueChanged.connect(lambda val, r=i, c=j: self.update_force(val, r, c))
                
                grid_layout.addWidget(QLabel(f"{i}→{j}:"), i, j*2)
                grid_layout.addWidget(box, i, j*2 + 1)
                
        # Pushes the grid to the center of the bottom panel
        bottom_layout.addStretch()
        bottom_layout.addWidget(grid_widget)
        bottom_layout.addStretch()
        
        main_layout.addWidget(ui_panel)
        
    def update_force(self, val, r, c):
        self.force_matrix[r, c] = val
