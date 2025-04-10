import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QPushButton, QLabel, QLineEdit, QGridLayout,
    QStatusBar, QAction, QMessageBox
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Set the window properties
        self.setWindowTitle("PyQt5 Application")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Add a label
        self.label = QLabel("Welcome to PyQt5 Application")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Add a text input field
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text here")
        self.layout.addWidget(self.text_input)
        
        # Add a button
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)
        
        # Add some space
        self.layout.addStretch()
        
        # Create a grid layout for demonstrating more complex layouts
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        
        # Add buttons to the grid
        for i in range(3):
            for j in range(3):
                btn = QPushButton(f"Button {i+1},{j+1}")
                grid_layout.addWidget(btn, i, j)
                
        self.layout.addWidget(grid_widget)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # Add actions to file menu
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def button_clicked(self):
        """Handle button click event"""
        text = self.text_input.text()
        if text:
            self.label.setText(f"You entered: {text}")
            self.status_bar.showMessage("Button clicked")
        else:
            self.status_bar.showMessage("Please enter some text")
    
    def new_file(self):
        """Create a new file"""
        self.status_bar.showMessage("New file created")
    
    def open_file(self):
        """Open a file"""
        self.status_bar.showMessage("Open file dialog would appear here")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About PyQt5 Template",
            "This is a template PyQt5 application.\n\nUse this as a starting point for your GUI applications."
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()