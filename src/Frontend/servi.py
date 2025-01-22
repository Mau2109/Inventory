import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from ventana_clientes import VentanaClientes
from ventana_categorias import VentanaCategorias
from ventana_tecnicos import VentanaTecnicos
from ventana_repuestos import VentanaRepuestos
from ventana_servicios import VentanaServicios
from ventana_equipo import VentanaEquipo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema PCC")
        self.setGeometry(100, 100, 1024, 768)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Barra superior
        self.barra_superior = QLabel(self)
        self.barra_superior.setStyleSheet("background-color: #1C5CA0;")
        self.barra_superior.setGeometry(0, 0, self.width(), 70)  #para que cambie de acuerdo al tamaño de la ventana

        # Barra lateral derecha
        self.barra_lateral = QLabel(self)
        self.barra_lateral.setStyleSheet("background-color: #1C5CA0;")
        self.barra_lateral.setGeometry(0, 70, 150, self.height() - 70)

        # Agregar logo en la barra superior
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/logo.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(800, 10, 224, 50)

        # Botones en la barra lateral
        self.initBotones()

    def initBotones(self):
        layout = QVBoxLayout()

        # Botón para Clientes
        self.btn_clientes = QPushButton(self)
        self.btn_clientes.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/clientes.png"))
        self.btn_clientes.setIconSize(QSize(64, 64))
        self.btn_clientes.setGeometry(20, 100, 100, 80)
        self.btn_clientes.setStyleSheet("background-color: transparent;")
        self.btn_clientes.clicked.connect(self.abrir_ventana_clientes)

        # Botón para Categorías
        self.btn_categorias = QPushButton(self)
        self.btn_categorias.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/categoria.png"))
        self.btn_categorias.setIconSize(QSize(64, 64))
        self.btn_categorias.setGeometry(20, 200, 100, 80)
        self.btn_categorias.setStyleSheet("background-color: transparent;")
        self.btn_categorias.clicked.connect(self.abrir_ventana_categorias)

        # Botón para Técnicos
        self.btn_tecnicos = QPushButton(self)
        self.btn_tecnicos.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/tecnico.png"))
        self.btn_tecnicos.setIconSize(QSize(64, 64))
        self.btn_tecnicos.setGeometry(20, 300, 100, 80)
        self.btn_tecnicos.setStyleSheet("background-color: transparent;")
        self.btn_tecnicos.clicked.connect(self.abrir_ventana_tecnicos)

        # Botón para Repuestos
        self.btn_repuestos = QPushButton(self)
        self.btn_repuestos.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/repuesto.png"))
        self.btn_repuestos.setIconSize(QSize(64, 64))
        self.btn_repuestos.setGeometry(20, 400, 100, 80)
        self.btn_repuestos.setStyleSheet("background-color: transparent;")
        self.btn_repuestos.clicked.connect(self.abrir_ventana_repuestos)

        # Botón para Servicios
        self.btn_servicios = QPushButton(self)
        self.btn_servicios.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/servicio.png"))
        self.btn_servicios.setIconSize(QSize(64, 64))
        self.btn_servicios.setGeometry(20, 500, 100, 80)
        self.btn_servicios.setStyleSheet("background-color: transparent;")
        self.btn_servicios.clicked.connect(self.abrir_ventana_servicios)

        # Botón para Equipos
        self.btn_equipos = QPushButton(self)
        self.btn_equipos.setIcon(QIcon("C:/Users/PC977/OneDrive/Documentos/Proyecto/Inventory/src/Frontend/equipo.png"))
        self.btn_equipos.setIconSize(QSize(64, 64))
        self.btn_equipos.setGeometry(20, 600, 100, 80)
        self.btn_equipos.setStyleSheet("background-color: transparent;")
        self.btn_equipos.clicked.connect(self.abrir_ventana_equipos)

    def abrir_ventana_clientes(self):
        self.ventana_clientes = VentanaClientes()
        self.ventana_clientes.show()

    def abrir_ventana_categorias(self):
        self.ventana_categorias = VentanaCategorias()
        self.ventana_categorias.show()

    def abrir_ventana_tecnicos(self):
        self.ventana_tecnicos = VentanaTecnicos()
        self.ventana_tecnicos.show()

    def abrir_ventana_repuestos(self):
        self.ventana_repuestos = VentanaRepuestos()
        self.ventana_repuestos.show()

    def abrir_ventana_servicios(self):
        self.ventana_servicios = VentanaServicios()
        self.ventana_servicios.show()

    def abrir_ventana_equipos(self):
        self.ventana_equipos = VentanaEquipo()
        self.ventana_equipos.show()

    #Funcion para que los elementos cambien de tamaño de acuerdo a la ventana
    def resizeEvent(self, event):
        """
        Ajusta las dimensiones de los elementos cuando se cambia el tamaño de la ventana.
        """

        self.barra_superior.setGeometry(0, 0, self.width(), 70)

        self.barra_lateral.setGeometry(0, 70, 150, self.height() - 70)

        self.logo_label.setGeometry(20, 10, 224, 50)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
