##### Reading shader files from disk
[QOpenGLShaderProgram](https://doc.qt.io/qtforpython-6/PySide6/QtOpenGL/QOpenGLShaderProgram.html?highlight=shaderprogram#PySide6.QtOpenGL.PySide6.QtOpenGL.QOpenGLShaderProgram.addShaderFromSourceFile) can read shader source files from disk. We do not need to re-invent the wheel.

        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceFile(QOpenGLShader.Vertex, "vertexShader.glsl")
        self.program.addShaderFromSourceFile(QOpenGLShader.Fragment, "fragmentShader.glsl")
        self.program.link()
