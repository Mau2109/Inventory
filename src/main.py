import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
sys.path.append("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend")
from Frontend.login import LoginWindow


app = QApplication(sys.argv)
login_window = LoginWindow()
login_window.show()
sys.exit(app.exec_())
