A minimal PySide (Qt for Python) application looks like below: <br>

    import sys 
    import os
    
    from PySide6.QtWidgets import QApplication
    
    if __name__ == "__main__":
        #
        # Main
        #
        app = QApplication(sys.argv)
    
        # To kill this app, kill the following pid
        print( "Process ID: ", os.getpid() )
    
        # enter ui main loop 
        sys.exit( app.exec_() )
    
