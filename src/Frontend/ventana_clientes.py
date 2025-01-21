from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QMessageBox
import psycopg2
from ventana_categorias import VentanaCategorias  # Importar ventana_categorias.py


class VentanaClientes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Nuevo Cliente")
        self.setGeometry(200, 200, 500, 600)
        self.initUI()

    def initUI(self):
       
        layout = QVBoxLayout()

        
        self.nombres_label = QLabel("Nombres*", self)
        self.nombres_input = QLineEdit(self)
        self.nombres_input.setPlaceholderText("Nombre")
        self.nombres_input.textChanged.connect(self.verificar_campos)

        self.apellidos_label = QLabel("Apellidos*", self)
        self.apellidos_input = QLineEdit(self)
        self.apellidos_input.setPlaceholderText("Apellidos")
        self.apellidos_input.textChanged.connect(self.verificar_campos)

        self.cuit_label = QLabel("RFC*", self)
        self.cuit_input = QLineEdit(self)
        self.cuit_input.setPlaceholderText("RFC (Máximo 13 caracteres)")
        self.cuit_input.setMaxLength(13)
        rfc_validator = QRegularExpressionValidator(QRegularExpression(r"^[A-Za-z0-9]{0,13}$"))
        self.cuit_input.setValidator(rfc_validator)
        self.cuit_input.textChanged.connect(self.verificar_campos)

        self.direccion_label = QLabel("Dirección*", self)
        self.direccion_input = QLineEdit(self)
        self.direccion_input.setPlaceholderText("Dirección del cliente")
        self.direccion_input.textChanged.connect(self.verificar_campos)

        self.telefono_label = QLabel("Teléfono*", self)
        self.telefono_input = QLineEdit(self)
        self.telefono_input.setPlaceholderText("Teléfono (10 dígitos)")
        self.telefono_input.setMaxLength(10)
        telefono_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{0,10}$"))
        self.telefono_input.setValidator(telefono_validator)
        self.telefono_input.textChanged.connect(self.verificar_campos)

        
        self.categoria_label = QLabel("Categoría*", self)
        categoria_layout = QHBoxLayout()

        self.categoria_combo = QComboBox(self)
        self.categoria_combo.addItem("-- SELECCIONAR --")
        self.categorias_map = {}
        self.cargar_categorias()
        self.categoria_combo.currentIndexChanged.connect(self.verificar_campos)

        self.btn_agregar_categoria = QPushButton("Agregar Categoría", self)
        self.btn_agregar_categoria.clicked.connect(self.abrir_ventana_categorias)

        categoria_layout.addWidget(self.categoria_combo)
        categoria_layout.addWidget(self.btn_agregar_categoria)

        # Botón de agregar cliente
        self.btn_agregar = QPushButton("Agregar Cliente", self)
        self.btn_agregar.setStyleSheet("background-color: lightgray; color: white; font-weight: bold;")
        self.btn_agregar.setEnabled(False)  # Deshabilitado por defecto
        self.btn_agregar.clicked.connect(self.agregar_cliente)

        
        self.estado_label = QLabel("", self)
        self.estado_label.setStyleSheet("color: red;")

        # Agregar widgets al layout
        layout.addWidget(self.nombres_label)
        layout.addWidget(self.nombres_input)
        layout.addWidget(self.apellidos_label)
        layout.addWidget(self.apellidos_input)
        layout.addWidget(self.cuit_label)
        layout.addWidget(self.cuit_input)
        layout.addWidget(self.direccion_label)
        layout.addWidget(self.direccion_input)
        layout.addWidget(self.telefono_label)
        layout.addWidget(self.telefono_input)
        layout.addWidget(self.categoria_label)
        layout.addLayout(categoria_layout)
        layout.addWidget(self.btn_agregar)
        layout.addWidget(self.estado_label)

        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def verificar_campos(self):
        """
        Verifica si todos los campos están completos y habilita/deshabilita el botón Agregar.
        """
        nombres = self.nombres_input.text().strip()
        apellidos = self.apellidos_input.text().strip()
        rfc = self.cuit_input.text().strip()
        direccion = self.direccion_input.text().strip()
        telefono = self.telefono_input.text().strip()
        categoria_seleccionada = self.categoria_combo.currentText() != "-- SELECCIONAR --"

        
        if nombres and apellidos and rfc and direccion and len(telefono) == 10 and categoria_seleccionada:
            self.btn_agregar.setEnabled(True)
            self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        else:
            self.btn_agregar.setEnabled(False)
            self.btn_agregar.setStyleSheet("background-color: lightgray; color: white; font-weight: bold;")

    def cargar_categorias(self):
        """
        Carga las categorías desde la base de datos.
        """
        try:
            conn = psycopg2.connect(
                dbname="SERVIPCC",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT ID_categoria, Nombre FROM CATEGORIA")
            categorias = cursor.fetchall()
            for id_categoria, nombre in categorias:
                self.categoria_combo.addItem(nombre)
                self.categorias_map[nombre] = id_categoria
            cursor.close()
            conn.close()
        except Exception as e:
            self.estado_label.setText(f"Error al cargar categorías: {e}")

    def agregar_cliente(self):
        """
        Agrega un cliente a la base de datos después de realizar todas las validaciones.
        """
        nombres = self.nombres_input.text()
        apellidos = self.apellidos_input.text()
        rfc = self.cuit_input.text()
        direccion = self.direccion_input.text()
        telefono = self.telefono_input.text()
        categoria_nombre = self.categoria_combo.currentText()

        id_categoria = self.categorias_map.get(categoria_nombre, None)
        if not id_categoria:
            self.estado_label.setText("Categoría seleccionada no es válida.")
            return

        try:
            conn = psycopg2.connect(
                dbname="SERVIPCC",
                user="postgres",
                password="mau",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()

            # Verificar si el teléfono ya existe
            cursor.execute("SELECT Telefono FROM CLIENTE WHERE Telefono = %s", (telefono,))
            if cursor.fetchone():
                self.estado_label.setText(f"Ya existe cliente con el número de teléfono {telefono}.")
                cursor.close()
                conn.close()
                return

            # Insertar el cliente
            query = """
                INSERT INTO CLIENTE (Nombre, Apellido, RFC, Direccion, Telefono, ID_categoria)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombres, apellidos, rfc, direccion, telefono, id_categoria))
            conn.commit()
            cursor.close()
            conn.close()

            #self.estado_label.setStyleSheet("color: green;")
            #self.estado_label.setText("Cliente agregado exitosamente.")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)  # Ícono de información
            msg.setWindowTitle("Informacion")
            msg.setText("Cliente agregado exitosamente.")
            msg.setStandardButtons(QMessageBox.Ok)  # Botón de OK
            msg.exec_()  # Mostrar el cuadro de mensaje
            self.limpiar_campos()
        except Exception as e:
            self.estado_label.setText(f"Error al agregar el cliente: {e}")

    def abrir_ventana_categorias(self):
        """
        Abre la ventana de categorías y selecciona automáticamente la nueva categoría agregada.
        """
        self.ventana_categorias = VentanaCategorias()
        self.ventana_categorias.categoria_agregada_signal.connect(self.seleccionar_categoria_nueva)
        self.ventana_categorias.show()

    def seleccionar_categoria_nueva(self, categoria_nombre):
        """
        Selecciona la nueva categoría agregada automáticamente y verifica los campos.
        """
        
        if categoria_nombre not in self.categorias_map:
            # Conectar a la base de datos para obtener el ID de la categoría recién agregada
            try:
                conn = psycopg2.connect(
                    dbname="SERVIPCC",
                    user="postgres",
                    password="mau",
                    host="localhost",
                    port="5432"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT ID_categoria FROM CATEGORIA WHERE Nombre = %s", (categoria_nombre,))
                result = cursor.fetchone()
                if result:
                    id_categoria = result[0]
                    self.categorias_map[categoria_nombre] = id_categoria
                    self.categoria_combo.addItem(categoria_nombre)
                cursor.close()
                conn.close()
            except Exception as e:
                self.estado_label.setText(f"Error al actualizar categorías: {e}")

        
        index = self.categoria_combo.findText(categoria_nombre)
        if index != -1:
            self.categoria_combo.setCurrentIndex(index)

        
        self.verificar_campos()

    def limpiar_campos(self):
        """
        Limpia todos los campos del formulario.
        """
        self.nombres_input.clear()
        self.apellidos_input.clear()
        self.cuit_input.clear()
        self.direccion_input.clear()
        self.telefono_input.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.estado_label.setText("")
        self.btn_agregar.setEnabled(False)
        self.btn_agregar.setStyleSheet("background-color: lightgray; color: white; font-weight: bold;")
