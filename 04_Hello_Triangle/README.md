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

        # Create and bind VBO, with default type.
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        
        # Allocate VBO, with copying in initial data
        vertices_data = vertices.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo.allocate( VoidPtr(vertices_data), 4 * vertices.size )

Here, we created and bound a Vertex Buffer Object. The [allocate()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLBuffer.html#PySide6.QtOpenGL.PySide6.QtOpenGL.QOpenGLBuffer.allocate) method allocated the requested bytes of space and initializes it with the data provided. We have the data copied into the VBO, now. To copy in more data from a different VoidPtr, allocate() the additional space and, then,  use the [write()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLBuffer.html#PySide6.QtOpenGL.PySide6.QtOpenGL.QOpenGLBuffer.write) method.

##### Vertex Shader

    from textwrap import dedent

    vertexShader = dedent("""
        #version 330 core
        layout (location = 0) in vec2 vPosition;
        
        void main()
        {
            gl_Position = vec4(vPosition.x, vPosition.y, 0.0, 1.0);
        }
    """)

##### Fragment Shader
    from textwrap import dedent

    fragmentShader = dedent("""
        #version 330 core
        out vec4 FragColor;
        
        void main()
        {
            FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
        } 
    """)

##### Shader Program

##### Verted Array Objects

##### And, the triangle!
