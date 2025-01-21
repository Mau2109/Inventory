from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
import psycopg2
from data_base import conectar_bd


class VentanaCategorias(QMainWindow):
    categoria_agregada_signal = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nueva Categoría")
        self.setGeometry(200, 200, 400, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campo de entrada para el nombre
        self.nombre_label = QLabel("Nombre*", self)
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre")
        self.nombre_input.setFixedHeight(30)

        # Campo de entrada para la descripción
        self.descripcion_label = QLabel("Descripción*", self)
        self.descripcion_input = QTextEdit(self)
        self.descripcion_input.setPlaceholderText("Descripción de la categoría")
        self.descripcion_input.setFixedHeight(60)

        # Botón para agregar categoría
        self.btn_agregar = QPushButton("Agregar Categoría", self)
        self.btn_agregar.setFixedHeight(40)
        self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        self.btn_agregar.clicked.connect(self.agregar_categoria)

        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)
        layout.addWidget(self.descripcion_label)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(self.btn_agregar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def agregar_categoria(self):
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.toPlainText()

        if not nombre.strip() or not descripcion.strip():
            print("Todos los campos son obligatorios.")
            return

        # Conectar a la base de datos y agregar la categoría
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            query = """
                INSERT INTO CATEGORIA (Nombre, Descripcion) VALUES (%s, %s)
            """
            cursor.execute(query, (nombre, descripcion))
            conn.commit()
            cursor.close()
            conn.close()
            print("Categoría agregada con éxito.")
            
            
            self.categoria_agregada_signal.emit(nombre)

           
            self.nombre_input.clear()
            self.descripcion_input.clear()

            
            self.close()

        except Exception as e:
            print(f"Error al agregar la categoría: {e}")
