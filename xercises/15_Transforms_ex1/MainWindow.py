from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtGui import QAction

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
        self.setWindowTitle("Scale by 0.5 and rotate by 45 deg")
        # Create menu
        self.createMenu()
        # Add the OpenGL Widget here
        renderWidget = RenderWidget(QSurfaceFormat())
        self.setCentralWidget(renderWidget)
        # <<<
        # <<<  More UI goes here
        # <<<
        self.show()

    def createMenu(self):
        """
        Set up menus for the application
        """
        exitAction = QAction("Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(exitAction)
