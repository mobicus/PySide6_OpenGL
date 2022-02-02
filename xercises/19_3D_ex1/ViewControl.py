from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel, QSpinBox, QComboBox

from PySide6.QtCore import Qt, Signal

class ViewControl(QWidget):
    """
       Controls for view matrix parameters
    """
    # Signals
    x_changed = Signal(int)
    y_changed = Signal(int)
    z_changed = Signal(int)
    
    # Methods
    def __init__(self, parent):
        super().__init__()
        layout = QGridLayout(self)
        self.setLayout(layout)
        # Label
        labelX = QLabel(self)
        labelX.setText(self.tr("X"))
        layout.addWidget(labelX, 0, 0, alignment=Qt.AlignTop)
        labelY = QLabel(self)
        labelY.setText(self.tr("Y"))
        layout.addWidget(labelY, 1, 0, alignment=Qt.AlignTop)
        labelZ = QLabel(self)
        labelZ.setText(self.tr("Z"))
        layout.addWidget(labelZ, 2, 0, alignment=Qt.AlignTop)
        
        # translate X Y Z
        translateX = QSpinBox( self )
        translateX.setRange(-50, 50)
        translateX.setSingleStep(1)
        translateX.setValue(0)
        translateX.valueChanged.connect(self.x_changed)
        layout.addWidget(translateX, 0, 1, alignment=Qt.AlignTop)
        
        translateY = QSpinBox( self )
        translateY.setRange(-50, 50)
        translateY.setSingleStep(1)
        translateY.setValue(0)
        translateY.valueChanged.connect(self.y_changed)
        layout.addWidget(translateY, 1, 1, alignment=Qt.AlignTop)
        
        translateZ = QSpinBox( self )
        translateZ.setRange(-50, 50)
        translateZ.setSingleStep(1)
        translateZ.setValue(0)
        translateZ.valueChanged.connect(self.z_changed)
        layout.addWidget(translateZ, 2, 1, alignment=Qt.AlignTop)
        
