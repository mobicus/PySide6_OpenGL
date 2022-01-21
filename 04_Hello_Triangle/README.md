So far, we created a Window and added an OpenGL widget to it. We also re-implemented the methods we need to render OpenGL. <br>
Now we try to port the triangle example.<br>

First, we will implement [QOpenGLWidget.initializeGL()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGLWidgets/QOpenGLWidget.html?highlight=openglwidget#PySide6.QtOpenGLWidgets.PySide6.QtOpenGLWidgets.QOpenGLWidget.initializeGL)

Then, we will implement the [QOpenGLWidget.paintGL()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGLWidgets/QOpenGLWidget.html?highlight=openglwidget#PySide6.QtOpenGLWidgets.PySide6.QtOpenGLWidgets.QOpenGLWidget.paintGL) method to render the triangle.

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

Here, we created and bound a Vertex Buffer Object. The [allocate()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLBuffer.html#PySide6.QtOpenGL.PySide6.QtOpenGL.QOpenGLBuffer.allocate) method allocates the requested bytes of space and initializes it with the data provided. We have the data copied into the VBO, now. To copy in more data from a different VoidPtr, allocate() the additional space and, then,  use the [write()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLBuffer.html#PySide6.QtOpenGL.PySide6.QtOpenGL.QOpenGLBuffer.write) method.

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

dedent() removes leading whitespaces; and allows us to present the shader in a more readable way.

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
[QOpenGLShaderProgram](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLShaderProgram.html?highlight=qopenglshaderprogram) loads, compiles and links shaders.

        # Load and compile shaders and link program
        #
        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertexShader)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragmentShader)
        self.program.link()

##### Verted Array Objects
The following code creates and binds a [QOpenGLVertexArrayObject](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLVertexArrayObject.html). QOpenGLVertexArrayObject.Binder() is [recommended](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/Binder.html) over VAO "create(), bind(), release()" sequence.

        self.vao = QOpenGLVertexArrayObject()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)
        
##### Link Vertex Attributes
Now that we have the VAO, we will setup the Vertex Attributes

        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 2)
        self.program.enableAttributeArray(0)
        # Release VBO
        self.vbo.release()

Alternatively,
        posAttr = self.program.attributeLocation("vPosition")
        self.program.setAttributeBuffer(posAttr, GL.GL_FLOAT, 0, 2)
        self.program.enableAttributeArray(posAttr)
        # Release VBO
        self.vbo.release()

That wraps our [QOpenGLWidget.initializeGL()](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGLWidgets/QOpenGLWidget.html?highlight=openglwidget#PySide6.QtOpenGLWidgets.PySide6.QtOpenGLWidgets.QOpenGLWidget.initializeGL) method.

No modifications are required for resizeGL() yet.
Now we will update the paintGL() method to render the triangle.

##### And, the triangle!

    def paintGL(self):
        # Draw the scene:
        f = self.context.functions()
        f.glClear(GL.GL_COLOR_BUFFER_BIT)
        # start painting
        self.program.bind()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)
        f.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self.program.release()


We have NOT used error/exception handling code for brevity.
