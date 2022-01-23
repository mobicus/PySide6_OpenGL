from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import (QOpenGLBuffer, QOpenGLVertexArrayObject)
from PySide6.QtOpenGL import (QOpenGLShader, QOpenGLShaderProgram)
from PySide6.QtGui import QOpenGLContext

from PySide6.support import VoidPtr

from OpenGL import GL

import numpy as np

from textwrap import dedent

vertexShader = dedent("""
    #version 330 core
    layout (location = 0) in vec2 vPosition;

    void main()
    {
        gl_Position = vec4(vPosition.x, vPosition.y, 0.0, 1.0);
    }
    """)

fragmentShader1 = dedent("""
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    } 
    """)

fragmentShader2 = dedent("""
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f);
    } 
    """)


class RenderWidget(QOpenGLWidget):
    def __init__(self, fmt):
        super().__init__()
        self.setFormat(fmt)
        self.context = QOpenGLContext(self)
        
        self.program = None
        
        if not self.context.create():
            raise Exception("Unable to create GL context")
        
    def initializeGL(self):
        # Set up the rendering context, load shaders and other resources, etc.:
        f = self.context.functions()
        f.glClearColor(0.2, 0.3, 0.3, 1.0);
        #
        # Load and compile shaders; and link program1
        #
        self.program1 = QOpenGLShaderProgram(self)
        self.program1.addShaderFromSourceCode(QOpenGLShader.Vertex, vertexShader)
        self.program1.addShaderFromSourceCode(QOpenGLShader.Fragment, fragmentShader1)
        self.program1.link()
        #
        # Setup VBO and VAO
        #
        vertices1 = np.array([  0.5, -0.5,
                                0.5,  0.5,
                               -0.5,  0.5  ], dtype=np.float32)
        
        vertices2 = np.array([ -0.5,  0.5,
                               -0.5, -0.5,
                                0.5, -0.5 ], dtype=np.float32)
        # Create and bind VBO
        self.vbo1 = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo1.create()
        self.vbo1.bind()
        # Allocate VBO with copying in initial data
        vertices1_data = vertices1.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo1.allocate( VoidPtr(vertices1_data), (4 * vertices1.size) )

        # Setup VAO
        self.vao1 = QOpenGLVertexArrayObject()
        vao1_binder = QOpenGLVertexArrayObject.Binder(self.vao1)
        # Setup vertex attributes
        self.program1.setAttributeBuffer(0, GL.GL_FLOAT, 0, 2)
        self.program1.enableAttributeArray(0)
        # Release VBO. Safe to do so after setAttributeBuffer
        self.vbo1.release()

        #
        # Load and compile shaders; and link program1
        #
        self.program2 = QOpenGLShaderProgram(self)
        self.program2.addShaderFromSourceCode(QOpenGLShader.Vertex, vertexShader)
        self.program2.addShaderFromSourceCode(QOpenGLShader.Fragment, fragmentShader2)
        self.program2.link()

        self.vbo2 = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo2.create()
        self.vbo2.bind()
        # Allocate VBO with copying in initial data
        vertices2_data = vertices2.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo2.allocate( VoidPtr(vertices2_data), (4 * vertices2.size) )
 
        # Setup VAO
        self.vao2 = QOpenGLVertexArrayObject()
        vao2_binder = QOpenGLVertexArrayObject.Binder(self.vao2)
        # Setup vertex attributes
        self.program2.setAttributeBuffer(0, GL.GL_FLOAT, 0, 2)
        self.program2.enableAttributeArray(0)
        # Release VBO. Safe to do so after setAttributeBuffer
        self.vbo2.release()
        
    def resizeGL(self, w, h):
        # Update projection matrix and other size related settings:
        f = self.context.functions()
        retina_scale = self.devicePixelRatio()
        f.glViewport(0, 0, self.width() * retina_scale, self.height() * retina_scale)
    
    def paintGL(self):
        # Draw the scene:
        f = self.context.functions()
        f.glClear(GL.GL_COLOR_BUFFER_BIT)
        # start painting
        
        self.program1.bind()
        vao1_binder = QOpenGLVertexArrayObject.Binder(self.vao1)
        #GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        f.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        #vao1_binder.release()
        self.program1.release()
        
        self.program2.bind()
        vao2_binder = QOpenGLVertexArrayObject.Binder(self.vao2)
        #GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        f.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        # vao2_binder.release()
        self.program2.release()

