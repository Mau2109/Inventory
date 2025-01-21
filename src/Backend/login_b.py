import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, dbname="postgres", user="postgres", password="admin", host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def check_user_credentials(self, email, password):
        conn = self.connect()
        if conn:
            cursor = conn.cursor()

            # Consulta SQL para verificar las credenciales del usuario
            query = "SELECT * FROM login WHERE correo_electronico = %s AND contraseña = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()  # Obtener el primer resultado (si existe)

            cursor.close()
            conn.close()

            return user is not None
        else:
            print("No se pudo conectar a la base de datos.")
            return False

    def add_guest_user(self):
        # Lógica para insertar un "usuario invitado" en la base de datos si es necesario
        pass


class Backend:
    def __init__(self):
        self.db = Database()

    def validate_login(self, email, password):
        # Verificar las credenciales de inicio de sesión
        return self.db.check_user_credentials(email, password)

    def guest_login(self):
        # Lógica para el inicio de sesión de invitado, si se requiere alguna acción en la base de datos
        self.db.add_guest_user()
        return True