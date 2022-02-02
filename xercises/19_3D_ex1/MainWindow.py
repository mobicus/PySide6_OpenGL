from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QDockWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtGui import QAction

from RenderWidget import RenderWidget

from ProjectionControl import ProjectionControl
from ViewControl import ViewControl

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
        self.setWindowTitle("Hello 3D")
        # Create menu
        self.createMenu()
        # Add the OpenGL Widget here
        renderWidget = RenderWidget(QSurfaceFormat())
        self.setCentralWidget(renderWidget)
        
        # Add Dock Widgets
        modelControl = QDockWidget("Model", self)
        modelControl.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, modelControl)
                      
        viewControl = QDockWidget("View", self)
        viewControl.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        vCtrl = ViewControl(self)
        viewControl.setWidget(vCtrl)
        self.addDockWidget(Qt.RightDockWidgetArea, viewControl)

        vCtrl.x_changed.connect(renderWidget.updateViewX)
        vCtrl.y_changed.connect(renderWidget.updateViewY)
        vCtrl.z_changed.connect(renderWidget.updateViewZ)
        
        projWidget = QDockWidget("Projection", self)
        projWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        projControl = ProjectionControl(projWidget)
        projWidget.setWidget(projControl)
        self.addDockWidget(Qt.RightDockWidgetArea, projWidget)

        projControl.fovChanged.connect(renderWidget.updateFoV)
        projControl.aspectRatioChanged.connect(renderWidget.updateAspectRatio)
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
