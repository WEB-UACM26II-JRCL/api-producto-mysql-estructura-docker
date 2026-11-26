import os
import time
import mysql.connector
from mysql.connector import Error


def get_connection(retries: int = 5, delay: int = 2):
    """Abre una conexion a MySQL con reintentos breves."""
    last_error = None
    for intento in range(1, retries + 1):
        try:
            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "mysql-productos"),
                user=os.getenv("MYSQL_USER", "web"),
                password=os.environ["MYSQL_PASSWORD"],
                database=os.getenv("MYSQL_DATABASE", "web-dbase"),
            )
        except Error as error:
            last_error = error
            print(f"[DB] Intento {intento} fallido: {error}")
            if intento < retries:
                time.sleep(delay)
    raise last_error
