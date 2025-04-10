import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QHBoxLayout, QGridLayout,
    QStatusBar, QAction, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.setMinimumSize(400, 400)
        self.rotation = [0, 0, 0]
        
    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / height
        gluPerspective(45, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Position camera
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        
        # Apply rotations
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        # Draw coordinate axes
        glBegin(GL_LINES)
        # X axis (red)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        # Y axis (green)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        # Z axis (blue)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()
        
        # Draw a simple colored cube as a placeholder
        self.draw_cube()
        
    def draw_cube(self):
        glBegin(GL_QUADS)
        # Top face (y = 0.5)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        
        # Bottom face (y = -0.5)
        glColor3f(1.0, 0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        
        # Front face (z = 0.5)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        
        # Back face (z = -0.5)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        
        # Left face (x = -0.5)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        
        # Right face (x = 0.5)
        glColor3f(1.0, 0.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glEnd()
        
    def rotate(self, x, y, z):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z
        self.updateGL()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Set the window properties
        self.setWindowTitle("PyQt5 with OpenGL")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Top label
        self.label = QLabel("OpenGL 3D Viewer")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Create a horizontal layout for the central section
        self.center_layout = QHBoxLayout()
        
        # Left panel for controls
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        
        # Add controls to left panel
        self.rotate_x_plus = QPushButton("Rotate X+")
        self.rotate_x_plus.clicked.connect(lambda: self.gl_widget.rotate(10, 0, 0))
        self.left_layout.addWidget(self.rotate_x_plus)
        
        self.rotate_y_plus = QPushButton("Rotate Y+")
        self.rotate_y_plus.clicked.connect(lambda: self.gl_widget.rotate(0, 10, 0))
        self.left_layout.addWidget(self.rotate_y_plus)
        
        self.rotate_z_plus = QPushButton("Rotate Z+")
        self.rotate_z_plus.clicked.connect(lambda: self.gl_widget.rotate(0, 0, 10))
        self.left_layout.addWidget(self.rotate_z_plus)
        
        self.left_layout.addStretch()
        self.center_layout.addWidget(self.left_panel)
        
        # Create and add the OpenGL widget in the center
        self.gl_widget = GLWidget()
        self.gl_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.center_layout.addWidget(self.gl_widget, 4)  # Give it more stretch
        
        # Right panel for more controls
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        
        # Add controls to right panel
        self.rotate_x_minus = QPushButton("Rotate X-")
        self.rotate_x_minus.clicked.connect(lambda: self.gl_widget.rotate(-10, 0, 0))
        self.right_layout.addWidget(self.rotate_x_minus)
        
        self.rotate_y_minus = QPushButton("Rotate Y-")
        self.rotate_y_minus.clicked.connect(lambda: self.gl_widget.rotate(0, -10, 0))
        self.right_layout.addWidget(self.rotate_y_minus)
        
        self.rotate_z_minus = QPushButton("Rotate Z-")
        self.rotate_z_minus.clicked.connect(lambda: self.gl_widget.rotate(0, 0, -10))
        self.right_layout.addWidget(self.rotate_z_minus)
        
        self.right_layout.addStretch()
        self.center_layout.addWidget(self.right_panel)
        
        # Add the center layout to the main layout
        self.layout.addLayout(self.center_layout)
        
    # Status bar at bottom
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("OpenGL initialized")
        
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # Add actions to file menu
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About PyQt5 OpenGL Template",
            "This is a template PyQt5 application with OpenGL integration.\n\n"
            "Use this as a starting point for 3D visualizations."
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()