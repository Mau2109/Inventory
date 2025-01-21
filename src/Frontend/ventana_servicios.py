from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QTextEdit, QComboBox, QHBoxLayout, QDateEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt5.QtCore import Qt, QRegularExpression
from data_base import conectar_bd
import psycopg2


class VentanaServicios(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Servicio")
        self.setGeometry(200, 200, 400, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campo para el equipo
        self.equipo_label = QLabel("Equipo*", self)
        self.equipo_input = QLineEdit(self)
        self.equipo_input.setPlaceholderText("Equipo asociado al servicio")
        self.equipo_input.setFixedHeight(30)

        # Campo para la descripción
        self.descripcion_label = QLabel("Descripción*", self)
        self.descripcion_input = QLineEdit(self)
        self.descripcion_input.setPlaceholderText("Descripción del servicio")
        self.descripcion_input.setFixedHeight(30)

        # Campo para el tipo
        self.tipo_label = QLabel("Tipo*", self)
        self.tipo_input = QLineEdit(self)
        self.tipo_input.setPlaceholderText("Tipo de servicio")
        self.tipo_input.setFixedHeight(30)

        # Campo para el estado
        self.estado_label = QLabel("Estado*", self)
        self.estado_input = QLineEdit(self)
        self.estado_input.setPlaceholderText("Estado del servicio")
        self.estado_input.setFixedHeight(30)

        # Campo para la fecha de recepción
        self.recepcion_label = QLabel("Recepción*", self)
        self.recepcion_input = QDateEdit(self)
        self.recepcion_input.setCalendarPopup(True)

        # Campo para la fecha de entrega
        self.entrega_label = QLabel("Entrega*", self)
        self.entrega_input = QDateEdit(self)
        self.entrega_input.setCalendarPopup(True)

        # Campo para la solución
        self.solucion_label = QLabel("Solución*", self)
        self.solucion_input = QLineEdit(self)
        self.solucion_input.setPlaceholderText("Solución aplicada")
        self.solucion_input.setFixedHeight(30)

        # Campo para el abono
        self.abono_label = QLabel("Abono $*", self)
        self.abono_input = QLineEdit(self)
        self.abono_input.setPlaceholderText("Abono realizado")
        self.abono_input.setFixedHeight(30)
        abono_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,10}(\.\d{1,2})?$"))
        self.abono_input.setValidator(abono_validator)

        # Campo para el servicio
        self.servicio_label = QLabel("Servicio*", self)
        self.servicio_input = QLineEdit(self)
        self.servicio_input.setPlaceholderText("Nombre del servicio")
        self.servicio_input.setFixedHeight(30)

        # Campo para el total
        self.total_label = QLabel("Total $*", self)
        self.total_input = QLineEdit(self)
        self.total_input.setPlaceholderText("Total a pagar $")
        self.total_input.setFixedHeight(30)
        total_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,10}(\.\d{1,2})?$"))
        self.total_input.setValidator(total_validator)

        # Campo para el cliente
        self.cliente_label = QLabel("Cliente*", self)
        self.cliente_combo = QComboBox(self)
        self.cliente_combo.addItem("-- SELECCIONAR --")
        self.clientes_map = {}
        self.cargar_clientes()

        # Botón para agregar servicio
        self.btn_agregar = QPushButton("Agregar Servicio", self)
        self.btn_agregar.setFixedHeight(40)
        self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        self.btn_agregar.clicked.connect(self.agregar_servicio)

        # Agregar widgets al layout
        layout.addWidget(self.equipo_label)
        layout.addWidget(self.equipo_input)
        layout.addWidget(self.descripcion_label)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(self.tipo_label)
        layout.addWidget(self.tipo_input)
        layout.addWidget(self.estado_label)
        layout.addWidget(self.estado_input)
        layout.addWidget(self.recepcion_label)
        layout.addWidget(self.recepcion_input)
        layout.addWidget(self.entrega_label)
        layout.addWidget(self.entrega_input)
        layout.addWidget(self.solucion_label)
        layout.addWidget(self.solucion_input)
        layout.addWidget(self.abono_label)
        layout.addWidget(self.abono_input)
        layout.addWidget(self.servicio_label)
        layout.addWidget(self.servicio_input)
        layout.addWidget(self.total_label)
        layout.addWidget(self.total_input)
        layout.addWidget(self.cliente_label)
        layout.addWidget(self.cliente_combo)
        layout.addWidget(self.btn_agregar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cargar_clientes(self):
        """
        Carga los clientes desde la base de datos y los agrega al combo box.
        """
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT ID_cliente, Nombre FROM CLIENTE")
            clientes = cursor.fetchall()
            for id_cliente, nombre in clientes:
                self.cliente_combo.addItem(nombre)
                self.clientes_map[nombre] = id_cliente
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al cargar los clientes: {e}")

    def agregar_servicio(self):
        equipo = self.equipo_input.text()
        descripcion = self.descripcion_input.text()
        tipo = self.tipo_input.text()
        estado = self.estado_input.text()
        recepcion = self.recepcion_input.date().toString("yyyy-MM-dd")
        entrega = self.entrega_input.date().toString("yyyy-MM-dd")
        solucion = self.solucion_input.text()
        abono = self.abono_input.text()
        servicio = self.servicio_input.text()
        total = self.total_input.text()
        cliente_nombre = self.cliente_combo.currentText()

        if not equipo.strip() or not descripcion.strip() or not tipo.strip() or not estado.strip() or not solucion.strip() or not abono.strip() or not servicio.strip() or not total.strip() or cliente_nombre == "-- SELECCIONAR --":
            print("Todos los campos son obligatorios.")
            return

        id_cliente = self.clientes_map.get(cliente_nombre, None)
        if not id_cliente:
            print("Error: No se encontró el ID del cliente seleccionado.")
            return

        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            query = """
                INSERT INTO SERVICIO (Descripcion, Tipo, Estado, Recepcion, Entrega, Solucion, Abono, Servicio, Total, ID_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, tipo, estado, recepcion, entrega, solucion, abono, servicio, total, id_cliente))
            conn.commit()
            cursor.close()
            conn.close()
            print("Servicio agregado con éxito.")

            # Limpiar los campos
            self.equipo_input.clear()
            self.descripcion_input.clear()
            self.tipo_input.clear()
            self.estado_input.clear()
            self.recepcion_input.clear()
            self.entrega_input.clear()
            self.solucion_input.clear()
            self.abono_input.clear()
            self.servicio_input.clear()
            self.total_input.clear()
            self.cliente_combo.setCurrentIndex(0)
        except Exception as e:
            print(f"Error al agregar el servicio: {e}")