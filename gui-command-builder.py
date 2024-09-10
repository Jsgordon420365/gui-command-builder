# ver 20240910160000.0
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget

class CommandBuilderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Command Builder")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.setup_ui()

    def setup_ui(self):
        # Left panel for command selection
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.command_search = QLineEdit()
        self.command_search.setPlaceholderText("Search commands...")
        self.command_list = QListWidget()
        left_layout.addWidget(self.command_search)
        left_layout.addWidget(self.command_list)

        # Middle panel for command building
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        self.option_list = QListWidget()
        middle_layout.addWidget(QLabel("Options:"))
        middle_layout.addWidget(self.option_list)

        # Right panel for command preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        self.copy_button = QPushButton("Copy to Clipboard")
        right_layout.addWidget(QLabel("Command Preview:"))
        right_layout.addWidget(self.command_preview)
        right_layout.addWidget(self.copy_button)

        # Add panels to main layout
        self.layout.addWidget(left_panel)
        self.layout.addWidget(middle_panel)
        self.layout.addWidget(right_panel)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommandBuilderGUI()
    window.show()
    sys.exit(app.exec_())

# Version History
# 20240910160000.0 - Initial version of the GUI Command Builder
