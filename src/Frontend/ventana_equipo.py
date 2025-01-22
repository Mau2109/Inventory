import psycopg2
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)
from data_base import conectar_bd


class VentanaEquipo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Nuevo Equipo")
        self.setGeometry(100, 100, 400, 300)

        # Widget principal
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Layout principal
        layout = QVBoxLayout(main_widget)

        # Campos del formulario
        self.num_serie = QLineEdit()
        self.num_serie.setPlaceholderText("Número de Serie")
        layout.addWidget(QLabel("Número de Serie:"))
        layout.addWidget(self.num_serie)

        self.imei = QLineEdit()
        self.imei.setPlaceholderText("IMEI")
        imei_regex = QRegularExpression(r"^\d{15}$")  # Validación para 15 dígitos
        self.imei.setValidator(QRegularExpressionValidator(imei_regex))
        layout.addWidget(QLabel("IMEI:"))
        layout.addWidget(self.imei)

        self.marca = QLineEdit()
        self.marca.setPlaceholderText("Marca")
        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.marca)

        self.modelo = QLineEdit()
        self.modelo.setPlaceholderText("Modelo")
        layout.addWidget(QLabel("Modelo:"))
        layout.addWidget(self.modelo)

        self.estado = QComboBox()
        self.estado.addItems(["Disponible", "En reparación", "Entregado"])
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.estado)

        # Botón para agregar equipo
        self.btn_agregar = QPushButton("Agregar Equipo",self)
        self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        self.btn_agregar.clicked.connect(self.agregar_equipo)
        layout.addWidget(self.btn_agregar)

    def agregar_equipo(self):
        # Obtener valores de los campos
        num_serie = self.num_serie.text().strip()
        imei = self.imei.text().strip()
        marca = self.marca.text().strip()
        modelo = self.modelo.text().strip()
        estado = self.estado.currentText()

        # Validar campos obligatorios
        if not num_serie or not imei or not marca or not modelo:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return
# Conexión a la base de datos
        try:
            conn = conectar_bd()
            cursor = conn.cursor()

            # Consulta SQL para insertar el equipo
            insert_query = """
                INSERT INTO EQUIPO (Num_serie, IMEI, Marca, Modelo, Estado)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (num_serie, imei, marca, modelo, estado))
            conn.commit()

            QMessageBox.information(self, "Éxito", "Equipo agregado correctamente.")
            self.limpiar_formulario()

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el equipo: {e}")

    def limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.num_serie.clear()
        self.imei.clear()
        self.marca.clear()
        self.modelo.clear()
        self.estado.setCurrentIndex(0)

