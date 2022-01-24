from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import (QOpenGLBuffer, QOpenGLVertexArrayObject)
from PySide6.QtOpenGL import (QOpenGLShader, QOpenGLShaderProgram)
from PySide6.QtGui import QOpenGLContext

from PySide6.support import VoidPtr

from OpenGL import GL

import numpy as np

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
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, "vertexShader.glsl")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, "fragmentShader.glsl")
        self.program.link()
        
        # Get x_offset location
        self.x_offset = self.program.uniformLocation("x_offset")
        
        #
        # Setup VBO and VAO
        #
        vertices = np.array([
             #// positions    #// colors
             0.5, -0.5, 0.0,  1.0, 1.0, 0.0,  # // bottom right
            -0.5, -0.5, 0.0,  0.0, 1.0, 1.0,  # // bottom left
             0.0,  0.5, 0.0,  1.0, 0.0, 1.0   # // top 
        ], dtype=np.float32)
        
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
        # QOpenGLShaderProgram.setAttributeBuffer(location, type, offset, tupleSize[, stride=0])
        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3, 6 * vertices.itemsize )
        self.program.setAttributeBuffer(1, GL.GL_FLOAT, 3 * vertices.itemsize, 3, 6 * vertices.itemsize )
        self.program.enableAttributeArray(0)
        self.program.enableAttributeArray(1)
        
        # Release VBO
        self.vbo.release()
        vao_binder.release()

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
        # update x_offset in shader
        f.glUniform1f(self.x_offset, 0.5)
        f.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self.program.release()

