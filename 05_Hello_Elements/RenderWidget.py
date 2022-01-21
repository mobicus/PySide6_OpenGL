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

fragmentShader = dedent("""
    #version 330 core
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
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
        # Load and compile shaders; and link program
        #
        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertexShader)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragmentShader)
        self.program.link()
        #
        # Setup VBO and VAO
        #
                
        vertices = np.array([  0.5,  0.5, 0.0,  # top right
                               0.5, -0.5, 0.0,  # bottom right
                              -0.5, -0.5, 0.0,  # bottom left
                              -0.5,  0.5, 0.0   # top left 
                             ], dtype=np.float32 )
        
        indices = np.array([  # note that we start from 0!
                              0, 1, 3,   # first triangle
                              1, 2, 3    # second triangle
                            ], dtype=np.uint32 )
        
        # Create and bind VBO
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.vbo.create()
        self.vbo.bind()
        # Allocate VBO with copying in initial data
        vertices_data = vertices.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo.allocate( VoidPtr(vertices_data), (4 * vertices.size) )
 
        # Setup VAO
        self.vao = QOpenGLVertexArrayObject()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)
        # Setup vertex attributes
        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        self.program.enableAttributeArray(0)
        # Release VBO. Safe to do so after setAttributeBuffer
        self.vbo.release()
        
        # create and bind the EBO
        self.ebo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        self.ebo.create()
        self.ebo.bind()
        self.indices_data = indices.tobytes()
        self.ebo.allocate( VoidPtr(self.indices_data), 4 * indices.size )
        

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
        self.program.bind()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)
        #GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL);
        f.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, VoidPtr(0))
        self.program.release()

