from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QSurfaceFormat

from RenderWidget import RenderWidget

class MainWindow(QMainWindow):
    """
    Main App Window
    """
    def __init__(self):
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        # set geometry
        self.setGeometry(100, 100, 800, 450)
        # set title
        self.setWindowTitle("Hello Window")
        # Add the penGL Widget here
        renderWidget = RenderWidget(QSurfaceFormat())
        self.setCentralWidget(renderWidget)
        # <<<
        # <<<  More UI goes here
        # <<<
        self.show()
