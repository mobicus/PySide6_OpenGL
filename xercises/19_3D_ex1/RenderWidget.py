from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import (QOpenGLBuffer, QOpenGLVertexArrayObject)
from PySide6.QtOpenGL import (QOpenGLShader, QOpenGLShaderProgram)
from PySide6.QtOpenGL import (QOpenGLTexture)
from PySide6.QtCore import Slot, QTimer
from PySide6.QtGui import QOpenGLContext
from PySide6.QtGui import QMatrix4x4, QVector3D
from PySide6.QtGui import QImage

from PySide6.support import VoidPtr

from OpenGL import GL

import numpy as np

class RenderWidget(QOpenGLWidget):
    def __init__(self, fmt):
        super().__init__()
        self.setFormat(fmt)
        self.context = QOpenGLContext(self)
        
        self.program = None
        self.angle = 0.0
        self.timer = None
        self.FoV = 45.0
        
        self.viewX = 0.0
        self.viewY = 0.0
        self.viewZ = -3.0

        self.xAspect = 16.0
        self.yAspect = 9.0
        
        if not self.context.create():
            raise Exception("Unable to create GL context")
        
    def initializeGL(self):
        # Set up the rendering context, load shaders and other resources, etc.:
        f = self.context.functions()
        f.glEnable(GL.GL_DEPTH_TEST)
        f.glClearColor(0.2, 0.3, 0.3, 1.0);
        #
        # Load and compile shaders; and link program
        #
        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, "vertexShader.glsl")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, "fragmentShader.glsl")
        self.program.link()
        #
        # Setup VBO and VAO
        #
        vertices = np.array([
            -0.5, -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5, -0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5,  0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 0.0,
            
            -0.5, -0.5,  0.5,  0.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            
            -0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5, -0.5,  1.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5,  0.5,  1.0, 0.0,
            
             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5,  0.5,  0.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
            
            -0.5, -0.5, -0.5,  0.0, 1.0,
             0.5, -0.5, -0.5,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
             0.5, -0.5,  0.5,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0,
            
            -0.5,  0.5, -0.5,  0.0, 1.0,
             0.5,  0.5, -0.5,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
             0.5,  0.5,  0.5,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0
        ],  dtype=np.float32 )

        # Setup VAO
        self.vao = QOpenGLVertexArrayObject()
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)

        # Create and bind VBO
        self.vbo = QOpenGLBuffer()
        self.vbo.create()
        self.vbo.bind()
        # Allocate VBO, and copy in data
        vertices_data = vertices.tobytes()
        # self.vbo.allocate( data_to_initialize , data_size_to_allocate )
        self.vbo.allocate( VoidPtr(vertices_data), 4 * vertices.size )
        
        # configure vertex attribute 0 and 1
        # QOpenGLShaderProgram.setAttributeBuffer(location, type, offset, tupleSize[, stride=0])
        self.program.setAttributeBuffer(0, GL.GL_FLOAT, 0, 3, 5 * vertices.itemsize )
        self.program.setAttributeBuffer(1, GL.GL_FLOAT, 3 * vertices.itemsize, 2, 5 * vertices.itemsize )
        self.program.enableAttributeArray(0)
        self.program.enableAttributeArray(1)
        
        # Release VBO
        self.vbo.release()
        
        # Setup texture1
        self.texture1 = QOpenGLTexture(QImage("../../images/container.jpg").mirrored())
        self.texture1.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        self.texture1.setMagnificationFilter(QOpenGLTexture.Linear)
        # Setup texture2
        self.texture2 = QOpenGLTexture(QImage("../../images/awesomeface.png").mirrored())
        self.texture2.setMinificationFilter(QOpenGLTexture.LinearMipMapLinear)
        self.texture2.setMagnificationFilter(QOpenGLTexture.Linear)

        # Start rotation
        self.play()

    def resizeGL(self, w, h):
        # Update projection matrix and other size related settings:
        f = self.context.functions()
        retina_scale = self.devicePixelRatio()
        f.glViewport(0, 0, self.width() * retina_scale, self.height() * retina_scale)
    
    def paintGL(self):
        # Draw the scene:
        f = self.context.functions()
        f.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        cubePositions = [
            QVector3D( 0.0,  0.0,  0.0), 
            QVector3D( 2.0,  5.0, -15.0), 
            QVector3D(-1.5, -2.2, -2.5),  
            QVector3D(-3.8, -2.0, -12.3),  
            QVector3D( 2.4, -0.4, -3.5),  
            QVector3D(-1.7,  3.0, -7.5),  
            QVector3D( 1.3, -2.0, -2.5),  
            QVector3D( 1.5,  2.0, -2.5), 
            QVector3D( 1.5,  0.2, -1.5), 
            QVector3D(-1.3,  1.0, -1.5)  
        ]

        # start painting
        # Bind program
        self.program.bind()
       
        # Setup texture locations
        tex1 = self.program.uniformLocation("vTexture1")
        self.program.setUniformValue(tex1, 0)
        tex2 = self.program.uniformLocation("vTexture2")
        self.program.setUniformValue(tex2, 1)
 
        model = self.program.uniformLocation("model")
        view = self.program.uniformLocation("view")
        projection = self.program.uniformLocation("projection")
        
        M_view  = QMatrix4x4()
        M_view.translate( self.viewX, self.viewY, self.viewZ )

        M_projection = QMatrix4x4()
        M_projection.perspective( self.FoV, self.xAspect / self.yAspect, 0.1, 100.0)
                
        # Bind VAO
        vao_binder = QOpenGLVertexArrayObject.Binder(self.vao)

        # bind textures
        self.texture1.bind(0)
        self.texture2.bind(1)
        
        # update the transform matrix
        self.program.setUniformValue(view, M_view)
        self.program.setUniformValue(projection, M_projection)

        for idx, position in enumerate( cubePositions ):
            M_model = QMatrix4x4()
            M_model.translate( position )
            M_model.rotate( 20.0 * idx , 1.0, 0.3, 0.5 )
            
            self.program.setUniformValue(model, M_model)
            f.glDrawArrays(GL.GL_TRIANGLES, 0, 36)


        self.texture1.release()
        self.texture2.release()
        # Release program
        self.program.release()

    @Slot(int)
    def updateFoV(self, fov):
        self.FoV = float(fov)
        self.update()
    
    @Slot()
    def updateAngle(self):
        self.angle += 1.0
        self.angle %= 360.0
        self.update()

    @Slot()
    def play(self):
        if self.timer is None:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateAngle)

        if not self.timer.isActive():
                self.timer.start(10)

    @Slot()
    def updateViewX(self, x):
        self.viewX = float(x)
        self.update()

    @Slot()
    def updateViewY(self, y):
        self.viewY = float(y)
        self.update()

    @Slot()
    def updateViewZ(self, z):
        self.viewZ = float(z)
        self.update()
    
    @Slot()
    def updateAspectRatio(self, aspect):
        if( aspect == 0):
            self.xAspect = float(4.0)
            self.yAspect = float(3.0)
        else:
            self.xAspect = float(16.0)
            self.yAspect = float(9.0)
        self.update()

    
