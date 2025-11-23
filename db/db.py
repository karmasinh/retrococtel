import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASS', '')
        self.database = os.getenv('DB_NAME', 'cocktails_db')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None

    def connect(self):
        """Establece conexión con MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            st.error(f"Error al conectar con MySQL: {e}")
            return None

    def disconnect(self):
        """Cierra la conexión con MySQL"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None, fetch=True):
        """Ejecuta una consulta SQL"""
        connection = self.connect()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
            else:
                connection.commit()
                first_token = query.strip().split()[0].upper() if isinstance(query, str) else ""
                if first_token == 'INSERT':
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount
            
            cursor.close()
            return result
        except Error as e:
            st.error(f"Error en la consulta: {e}")
            return None
        finally:
            self.disconnect()

    def execute_procedure(self, procedure_name, params=None):
        """Ejecuta un procedimiento almacenado"""
        connection = self.connect()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.callproc(procedure_name, params)
            
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            cursor.close()
            return results
        except Error as e:
            st.error(f"Error en el procedimiento: {e}")
            return None
        finally:
            self.disconnect()

    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            connection = self.connect()
            if connection and connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.close()
                self.disconnect()
                return f"Conexión exitosa - MySQL versión: {version[0]}"
            else:
                return "No se pudo conectar a MySQL"
        except Error as e:
            return f"Error de conexión: {e}"

# Función auxiliar para obtener conexión
def get_db_connection():
    """Obtiene una instancia de conexión a la base de datos"""
    return DatabaseConnection()
