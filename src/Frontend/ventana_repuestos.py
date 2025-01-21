from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QTextEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt5.QtCore import Qt, QRegularExpression
import psycopg2

class VentanaRepuestos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Repuesto / Accesorio")
        self.setGeometry(200, 200, 400, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campo para el nombre
        self.nombre_label = QLabel("Nombre*", self)
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre del repuesto o accesorio")
        self.nombre_input.setFixedHeight(30)

        # Campo para la descripción
        self.descripcion_label = QLabel("Descripción*", self)
        self.descripcion_input = QTextEdit(self)
        self.descripcion_input.setPlaceholderText("Descripción del repuesto o accesorio")
        self.descripcion_input.setFixedHeight(60)

        # Campo para la marca
        self.marca_label = QLabel("Marca*", self)
        self.marca_input = QLineEdit(self)
        self.marca_input.setPlaceholderText("Marca del repuesto o accesorio")
        self.marca_input.setFixedHeight(30)

        # Campo para la categoría
        self.categoria_label = QLabel("Categoría*", self)
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.addItem("-- SELECCIONAR --")
        self.categorias_map = {}
        self.cargar_categorias()

        # Campo para el precio de compra
        self.compra_label = QLabel("Precio de Compra $*", self)
        self.compra_input = QLineEdit(self)
        self.compra_input.setPlaceholderText("Precio de compra del repuesto")
        self.compra_input.setFixedHeight(30)
        compra_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,10}(\.\d{1,2})?$"))
        self.compra_input.setValidator(compra_validator)

        # Campo para el precio de venta
        self.venta_label = QLabel("Precio de Venta $*", self)
        self.venta_input = QLineEdit(self)
        self.venta_input.setPlaceholderText("Precio de venta del repuesto")
        self.venta_input.setFixedHeight(30)
        venta_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{1,10}(\.\d{1,2})?$"))
        self.venta_input.setValidator(venta_validator)

        # Crear un layout horizontal para el campo de stock y los botones
        stock_layout = QHBoxLayout()

        # Campo para el stock (solo se modificará con los botones)
        self.stock_label = QLabel("Stock*", self)
        self.stock_input = QLineEdit(self)
        self.stock_input.setPlaceholderText("Cantidad en stock")
        self.stock_input.setFixedHeight(30)
        self.stock_input.setReadOnly(True)  # Deshabilitar la edición manual

        # Botones de incremento y decremento
        self.btn_incrementar = QPushButton("+", self)
        self.btn_decrementar = QPushButton("-", self)

        # Conectar los botones a sus métodos
        self.btn_incrementar.clicked.connect(self.incrementar_stock)
        self.btn_decrementar.clicked.connect(self.decrementar_stock)

        # Agregar widgets al layout del stock
        stock_layout.addWidget(self.stock_input)
        stock_layout.addWidget(self.btn_decrementar)
        stock_layout.addWidget(self.btn_incrementar)

        # Agregar el label y el layout del stock al layout principal
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)
        layout.addWidget(self.descripcion_label)
        layout.addWidget(self.descripcion_input)
        layout.addWidget(self.marca_label)
        layout.addWidget(self.marca_input)
        layout.addWidget(self.categoria_label)
        layout.addWidget(self.categoria_combo)
        layout.addWidget(self.compra_label)
        layout.addWidget(self.compra_input)
        layout.addWidget(self.venta_label)
        layout.addWidget(self.venta_input)
        layout.addWidget(self.stock_label)
        layout.addLayout(stock_layout)
        
        # Botón para agregar repuesto
        self.btn_agregar = QPushButton("Agregar Repuesto / Accesorio", self)
        self.btn_agregar.setFixedHeight(40)
        self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        self.btn_agregar.clicked.connect(self.agregar_repuesto)
        layout.addWidget(self.btn_agregar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def cargar_categorias(self):
        """
        Carga las categorías desde la base de datos y las agrega al combo box.
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
            print(f"Error al cargar las categorías: {e}")

    def agregar_repuesto(self):
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        marca = self.marca_input.text()
        categoria_nombre = self.categoria_combo.currentText()
        compra = self.compra_input.text()
        venta = self.venta_input.text()
        stock = self.stock_input.text()

        if not nombre.strip() or not descripcion.strip() or not marca.strip() or categoria_nombre == "-- SELECCIONAR --" or not compra.strip() or not venta.strip() or not stock.strip():
            print("Todos los campos son obligatorios.")
            return

        id_categoria = self.categorias_map.get(categoria_nombre, None)
        if not id_categoria:
            print("Error: No se encontró el ID de la categoría seleccionada.")
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
            query = """
                INSERT INTO REPUESTO (Nombre, Descripcion, Marca, ID_categoria, Compra, Venta, Stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, descripcion, marca, id_categoria, compra, venta, stock))
            conn.commit()
            cursor.close()
            conn.close()
            print("Repuesto / Accesorio agregado con éxito.")

            # Limpiar los campos
            self.nombre_input.clear()
            self.descripcion_input.clear()
            self.marca_input.clear()
            self.categoria_combo.setCurrentIndex(0)
            self.compra_input.clear()
            self.venta_input.clear()
            self.stock_input.clear()
        except Exception as e:
            print(f"Error al agregar el repuesto: {e}")

    def incrementar_stock(self):
        try:
            stock_actual = int(self.stock_input.text())
            self.stock_input.setText(str(stock_actual + 1))
        except ValueError:
            self.stock_input.setText("0")

    def decrementar_stock(self):
        try:
            stock_actual = int(self.stock_input.text())
            if stock_actual > 0:
                self.stock_input.setText(str(stock_actual - 1))
        except ValueError:
            self.stock_input.setText("0")