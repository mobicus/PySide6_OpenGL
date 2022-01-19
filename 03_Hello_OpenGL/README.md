Widgets have properties and methods; and Qt provides them with two additional sets of "specialized" methods, namely, "signals" and "slots."

A widget can be configured to "emit" a "signal" when one of its properties change.
And a widget can receive a signal from another widget through one of its "slot" methods when the signal and slot are connected.
For example, consider a video player. The play button's "clicked" signal is connected to "play()" slot of the video player.
When the play button is clicked, the video player play()s the video. The pause button's "clicked" signal is connected to "pause()" slot of video player. When the pause button is clicked, the video player pause()s the video.

PySide6 offers three ways to render OpenGL.

1. QOpenGLWidget
2. QWindow; and
3. QOpenGLWindow


QWindow and its convenient class QOpenGLWindow 