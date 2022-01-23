
from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

import sys
import os

if __name__ == "__main__":
    #
    # Main
    #
    
    # Create the Qt App
    app = QApplication(sys.argv)
    
    # Create the window
    mainWindow = MainWindow()
    
    # enter ui main loop 
    sys.exit( app.exec_() )
    
