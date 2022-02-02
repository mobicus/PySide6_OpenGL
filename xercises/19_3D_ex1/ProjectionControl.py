from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLabel, QSpinBox, QComboBox

from PySide6.QtCore import Qt, Signal

class ProjectionControl(QWidget):
    """
       Control projection parameters
    """
    # signals
    fovChanged = Signal(int)
    aspectRatioChanged = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        # label FoV | number input 30-90

        # layout
        layout = QGridLayout(self)
        self.setLayout(layout)
        # Label
        labelFoV = QLabel(self)
        labelFoV.setText(self.tr("FoV"))
        layout.addWidget(labelFoV, 0, 0, alignment=Qt.AlignTop)
        
        # angle input
        angleInput = QSpinBox( self )
        angleInput.setRange(20, 120)
        angleInput.setSingleStep(1)
        angleInput.setValue(45)
        layout.addWidget(angleInput, 0, 1, alignment=Qt.AlignTop)
        angleInput.valueChanged.connect(self.fovChanged)
        
        # aspect ratio
        labelAspect = QLabel(self)
        labelAspect.setText(self.tr("Aspect Ratio"))
        layout.addWidget(labelAspect, 1, 0, alignment=Qt.AlignTop)
        
        aspectSelect = QComboBox(self)
        aspectSelect.addItem(self.tr("4:3"))
        aspectSelect.addItem(self.tr("16:9"))
        aspectSelect.currentIndexChanged(self.aspectRatioChanged)
        layout.addWidget(aspectSelect, 1, 1, alignment=Qt.AlignTop)
        
