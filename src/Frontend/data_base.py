import psycopg2

def conectar_bd():
    """
    Crea y retorna una conexión a la base de datos PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            dbname="SERVIPCC",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Error al conectar a la base de datos: {e}")