import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox
from dulwich import porcelain

REPO_URL = "https://github.com/CHooverShrimp/mareBall.git"

class LauncherUI(QWidget):
    def __init__(self):
        super().__init__()
        self.local_dir = os.path.dirname(sys.executable)  # Default directory
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Software Launcher')
        
        self.layout = QVBoxLayout()
        
        #self.select_dir_button = QPushButton('Select Directory', self)
        #self.select_dir_button.clicked.connect(self.select_directory)
        
        self.update_button = QPushButton('Check for Updates', self)
        self.update_button.clicked.connect(self.check_for_updates)
        
        self.launch_button = QPushButton('Launch', self)
        self.launch_button.clicked.connect(self.launch_software)
        
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        
        #self.layout.addWidget(self.select_dir_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.launch_button)
        self.layout.addWidget(self.output_area)
        
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 600, 400)

    def log(self, message):
        self.output_area.append(message)

    def run_command(self, command):
        try:
            self.log(f"Running command: {command}")
            if command == 'pull':
                porcelain.pull(self.local_dir, REPO_URL)
            elif command == 'clone':
                porcelain.clone(REPO_URL, self.local_dir)
            self.log("Command completed successfully.")
        except Exception as e:
            self.log(f"Error running command: {e}")

    def clone_repo(self):
            self.run_command('clone')

    def update_repo(self):
        if os.path.exists(os.path.join(self.local_dir, ".git")):
            self.log("Checking for updates...")
            self.run_command('pull')
        else:
            self.log("No Git repository found. Please select a valid directory or clone the repository first.")

    def check_for_updates(self):
        # Auto clone if there's no repo
        if not os.path.exists(os.path.join(self.local_dir, ".git")):
            self.clone_repo()
        else:
            self.update_repo()

    def launch_software(self):
        self.update_repo() # Always check for updates before launching

        self.log("Launching software...")
        try:
            os.startfile(os.path.join(self.local_dir, 'test.txt'))
        except Exception as e:
            self.log(f"Error launching software: {e}")
    
    ''' # no need anymore since the scheme is to put the launcher in the right directory, and make a shortcut
    def select_directory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "", options)
        if directory:
            self.local_dir = directory
            self.log(f"Selected directory: {self.local_dir}")
    '''
def main():
    app = QApplication(sys.argv)
    launcher = LauncherUI()
    launcher.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
