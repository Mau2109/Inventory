from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget
import psycopg2

class VentanaTecnicos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Técnico")
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campo de entrada para el nombre
        self.nombre_label = QLabel("Nombre Completo*", self)
        self.nombre_input = QLineEdit(self)
        self.nombre_input.setPlaceholderText("Nombre Completo")
        self.nombre_input.setFixedHeight(30)

        # Campo de entrada para el teléfono
        self.telefono_label = QLabel("Teléfono*", self)
        self.telefono_input = QLineEdit(self)
        self.telefono_input.setPlaceholderText("Teléfono (10 dígitos)")
        self.telefono_input.setMaxLength(10)

        # Botón para agregar técnico
        self.btn_agregar = QPushButton("Agregar Técnico", self)
        self.btn_agregar.setFixedHeight(40)
        self.btn_agregar.setStyleSheet("background-color: #007BFF; color: white; font-weight: bold;")
        self.btn_agregar.clicked.connect(self.agregar_tecnico)

        # Agregar widgets al layout
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)
        layout.addWidget(self.telefono_label)
        layout.addWidget(self.telefono_input)
        layout.addWidget(self.btn_agregar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def agregar_tecnico(self):
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()

        if not nombre.strip() or not telefono.strip():
            print("Todos los campos son obligatorios.")
            return

        try:
            conn = psycopg2.connect(
                dbname="SERVIPCC",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            cursor = conn.cursor()
            query = """
                INSERT INTO TECNICO (Nombre_completo, Telefono) VALUES (%s, %s)
            """
            cursor.execute(query, (nombre, telefono))
            conn.commit()
            cursor.close()
            conn.close()
            print("Técnico agregado con éxito.")

            # Limpiar los campos
            self.nombre_input.clear()
            self.telefono_input.clear()
        except Exception as e:
            print(f"Error al agregar el técnico: {e}")
