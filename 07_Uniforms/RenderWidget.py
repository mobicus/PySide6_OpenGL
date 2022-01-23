from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLBuffer, QOpenGLVertexArrayObject
from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram
from PySide6.QtCore import Slot, QTimer
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

    uniform  vec4 vertexColor;

    void main()
    {
        FragColor = vertexColor;
    } 
    """)


class RenderWidget(QOpenGLWidget):
    def __init__(self, fmt):
        super().__init__()
        self.setFormat(fmt)
        self.context = QOpenGLContext(self)
        
        self.program = None
        self.timer = None
        self.timeStep = 0.0
        self.color = 0.0
        # Check if a valid context is created
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
        # Color attribute location
        #
        self.colorLocation = self.program.uniformLocation("vertexColor")
        #
        # Setup VBO and VAO
        #
        vertices = np.array( [ -0.5, -0.5, 0.0,
                                0.5, -0.5, 0.0,
                                0.0,  0.5, 0.0 ], dtype=np.float32) 
        # Create and bind VBO
        self.vbo = QOpenGLBuffer()
        self.vbo.create()
        self.vbo.bind()
        # Allocate VBO, and copy in data
        vertices_data = vertices.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo.allocate( VoidPtr(vertices_data), 4 * vertices.size )
        # Setup VAO
        self.vao = QOpenGLVertexArrayObject()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)
        # configure vertex attribute 0
        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3)
        self.program.enableAttributeArray(0)
        # Release VBO
        self.vbo.release()
        vao_binder.release()
        # Start timer for color change
        self.play()

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
        # Update the color
        # f.glUniform4fk(self.colorLocation, 0.0, self.color, 0.0, 0.0)
        # setUniformValue (location, x, y, z, w)
        self.program.setUniformValue(self.colorLocation, 0.0, self.color, 0.0, 0.0)
        f.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self.program.release()

    @Slot()
    def updateColor(self):
        self.timeStep += 0.04
        self.timeStep %= 3.0
        green = np.sin(self.timeStep)
        if green < 0.0:
            green *= -1
        self.color = green
        self.update()

    def play(self):
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateColor)
        if not self.timer.isActive():
            self.timer.start(100)

    

