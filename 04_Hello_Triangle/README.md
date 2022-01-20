So far, we created a Window and added an OpenGL widget to it. We also re-implemented the methods we need to render OpenGL. <br>
Now we try to port the triangle example.<br>

##### Vertices
We define the vertices using a float32 numpy array.<br>

    import numpy as np
    vertices = np.array( [ -0.5, -0.5, 0.0,
                            0.5, -0.5, 0.0,
                            0.0,  0.5, 0.0 ], dtype=np.float32) 
                            
##### Vertex Buffer Object
PySide6 provides for OpenGL buffers through the [QOpenGLBuffer](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLBuffer.html) class.


##### Vertex Shader

##### Fragment Shader

##### Shader Program

##### Verted Array Objects

##### And, the triangle!
