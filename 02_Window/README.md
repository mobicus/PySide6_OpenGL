## New to PySide6?
If you are new to PySide6 (Qt6 for Python), here are the basics.

Qt6 is a multi-platform Graphical User Interface (GUI) development library. 
It provides GUI components like windows, buttons, textedits, text areas, canvas to draw to etc.
The basic GUI component in Qt6 is a "widget." For example, a button is a widget.
Widgets have properties and methods; and Qt provides them with two additional sets of "specialized" methods, namely, "signals" and "slots."

A widget can be configured to "emit" a "signal" when one of its properties change.
And a widget can receive a signal from another widget through one of its "slot" methods.

PySide6 offers three ways to render OpenGL.

1. QOpenGLWidget
2. QWindow; and
3. QOpenGLWindow


QWindow and its convenient class QOpenGLWindow 
