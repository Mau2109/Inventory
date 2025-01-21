import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from servi import *
sys.path.append("C:/Users/PC977/OneDrive/Documentos/Proyecto/SERVIPCC/Backend")
from Backend.login_b import *


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("background-color: #f4f4f9;")  # Color de fondo general
        self.backend = Backend()  # Instanciamos el Backend
        self.initUI()

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)  # Márgenes de la ventana

        # Título
        self.title_label = QLabel('Iniciar sesión', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2e3b4e;")
        layout.addWidget(self.title_label)

        # Etiqueta y campo de texto para el usuario
        self.username_label = QLabel('Email:', self)
        self.username_label.setStyleSheet("font-size: 14px; color: #333;")
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Introduce tu correo electrónico")
        self.username_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc; font-size: 14px;")

        # Etiqueta y campo de texto para la contraseña
        self.password_label = QLabel('Password:', self)
        self.password_label.setStyleSheet("font-size: 14px; color: #333;")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Introduce tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)  # Para mostrar los caracteres como estrellas
        self.password_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ccc; font-size: 14px;")

        # Botón de login
        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            font-size: 16px; 
            padding: 10px;
            border: none;
            border-radius: 5px;
        """)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.check_login)

        # Botón de inicio de sesión como invitado
        self.guest_button = QPushButton('Iniciar sesión como invitado', self)
        self.guest_button.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            font-size: 12px; 
            padding: 5px 10px;
            border: none;
            border-radius: 5px;
        """)
        self.guest_button.setCursor(Qt.PointingHandCursor)
        self.guest_button.clicked.connect(self.login_as_guest)

        # Añadir widgets al layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.guest_button)  # Añadir el botón de invitado

        # Establecer layout
        self.setLayout(layout)    

    def check_login(self):
        # Obtener valores de usuario y contraseña
        username = self.username_input.text()
        password = self.password_input.text()

        # Validar las credenciales
        if self.backend.validate_login(username, password):
            print("Login Successful")
            self.open_main_window()
        else:
            print("Invalid Email or Password")

    def login_as_guest(self):
        # Lógica para ingresar como invitado (sin necesidad de usuario/contraseña)
        print("Login as guest")
        self.open_main_window()
        
    def open_main_window(self):
        # Cerrar la ventana de login y abrir la ventana principal
        self.close()  # Cerrar ventana de login
        self.main_window = MainWindow()  # Crear nueva ventana
        self.main_window.show()  # Mostrar nueva ventana