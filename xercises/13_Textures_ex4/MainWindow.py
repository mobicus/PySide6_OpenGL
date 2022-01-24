from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtGui import QAction

from RenderWidget import RenderWidget

class MainWindow(QMainWindow):
    """
    Main App Window
    """
    # signals
    keyPressed = Signal(int)
    
    # methods
    def __init__(self):
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        # set geometry
        self.setGeometry(100, 100, 800, 450)
        # set title
        self.setWindowTitle("More Attributes")
        # Create menu
        self.createMenu()
        # Add the OpenGL Widget here
        renderWidget = RenderWidget(QSurfaceFormat())
        self.setCentralWidget(renderWidget)
        self.keyPressed.connect(renderWidget.setMixRatio)
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

    # event handlers
    def keyPressEvent(self, event):
        """
            event handler for key presses
        """
        self.keyPressed.emit(event.key())
