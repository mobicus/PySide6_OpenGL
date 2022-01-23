##### QOpenGLWidget.update() Vs. glfwWindowShouldClose(window)
In the book we use "!glfwWindowShouldClose(window)" to continously render the scene. But QOpenGLWidget has no such busy waiting loop. 
It has an event-driven architechture. Whenever we want to render an update to the scene, we call QOpenGLWidget.update(). 

To illustrate the update to a "uniform" shader variable, the [author uses continuous updates to the scene with the vertex colors changed over time.](https://learnopengl.com/Getting-started/Shaders)

  float timeValue = glfwGetTime();
  float greenValue = (sin(timeValue) / 2.0f) + 0.5f;
  int vertexColorLocation = glGetUniformLocation(shaderProgram, "ourColor");
  glUseProgram(shaderProgram);
  glUniform4f(vertexColorLocation, 0.0f, greenValue, 0.0f, 1.0f);
  
To update the color over time, we will use a timer in PySide6 - [QTimer](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html).

##### A digression to QWidgets

PySide6 has an event-driven architecture to invoke its GUI controls aka "widgets."
