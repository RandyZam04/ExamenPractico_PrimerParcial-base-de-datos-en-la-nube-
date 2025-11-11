import mysql.connector
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bcrypt
from getpass import getpass
import os
from dotenv import load_dotenv
import time
from datetime import datetime
from utilidades import *

load_dotenv()

class SistemaAutenticacion:
    def __init__(self):
        self.mysql_conexion = None
        self.mysql_cursor = None
        self.connection_string = os.getenv('MONGO_URI')
        self.database_name = "ExamenPractico"
        pass

    def conectar_mysql(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="LunesDomingo69",
                database="examen_practico"
            )
            print("Conexión exitosa a MySQL.")
            return conexion
        except mysql.connector.Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None

    def conectar(self):
        try:
            client = MongoClient(self.connection_string)
            client.admin.command('ping')
            db = client[self.database_name]
            print("Conexión exitosa a MongoDB")
            return db
        except ConnectionFailure as e:
            print(f"Error de conexión: {e}")
            return None

    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verificar_password(self, password, password_hash):
        import bcrypt
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            print(f"Error al verificar contraseña: {e}")
            return False

    def registrar_usuario(self, usuario):
        mongo_db = self.conectar()
        if mongo_db is not None:
            try:
                resultado = mongo_db.usuarios.insert_one(usuario)
                print(f"\nUsuario insertado correctamente con ID: {resultado.inserted_id}")
                self.registrar_log(usuario, "exitoso")
            except Exception as e:
                print(f"\nError al registrar usuario en MongoDB: {e}")
                self.registrar_log(usuario, "fallido")
        else:
            print("\nNo se pudo establecer conexión con MongoDB.")
            self.registrar_log(usuario, "fallido")

    def login(self,username):
        mongo_db = self.conectar()
        if mongo_db is None:
            print("\nNo se pudo conectar con MongoDB.")
            return False

        usuario = mongo_db.usuarios.find_one({"username": username})

        if usuario is None:
            print("\nUsuario no encontrado.")
            time.sleep(2)
            return False

        password = getpass.getpass("Ingrese su contraseña: ").strip()

        if bcrypt.checkpw(password.encode('utf-8'), usuario["password_hash"].encode('utf-8')):
            limpiar_consola()
            print(f"\nBienvenido {username}! Inicio de sesión exitoso.")
            self.usuario_actual = usuario
            self.registrar_log(usuario, "exitoso")
            time.sleep(2)
            
            return True
        else:
            print("\nContraseña incorrecta.")
            time.sleep(2)
            self.registrar_log(usuario, "fallido")
            return False
        
    def recuperar_clave(self):

        mongo_db = self.conectar()
        if mongo_db is None:
            print("\nNo se pudo conectar con MongoDB.")
            return False

        print("\nRECUPERACIÓN DE CONTRASEÑA")
        print("──────────────────────────────────────────")

        usuario = input("Ingresa tu nombre de usuario: ").strip()

        usuario = mongo_db.usuarios.find_one({"username": usuario})
        if usuario is None:
            print("\nNo existe ningún usuario con ese nombre.")
            time.sleep(2)
            return False

        email = input("Ingresa el correo asociado a tu cuenta: ").strip()

        if email != usuario["email"]:
            print("\nEl correo no coincide con el registrado.")
            time.sleep(2)
            return False

        print("\n📨 Le enviamos un correo con un código de verificación.")
        time.sleep(2)

        codigo = input("Ingrese el código recibido (simulado): ").strip()

        if codigo != "123456":
            print("\nCódigo incorrecto. No se puede continuar.")
            time.sleep(2)
            return False

        print("\nCódigo verificado correctamente.")
        time.sleep(1)

        nueva_clave = getpass("Ingrese su nueva contraseña: ").strip()
        conf_clave = getpass("Confirme su nueva contraseña: ").strip()

        if nueva_clave != conf_clave:
            print("\nLas contraseñas no coinciden.")
            time.sleep(2)
            return False

        password_hash = self.hash_password(nueva_clave)

        mongo_db.usuarios.update_one(
            {"username": usuario},
            {"$set": {"password_hash": password_hash}}
        )

        print("\nContraseña actualizada correctamente.")
        time.sleep(2)
        return True

    def login_admin(self):
        conexion = self.conectar_mysql()
        if conexion is None:
            print("\nNo se pudo conectar con MySQL.")
            return False

        try:
            cursor = conexion.cursor(dictionary=True)

            print("\nINICIO DE SESIÓN ADMINISTRADOR")
            print("────────────────────────────────────────────")

            username = input("Nombre de administrador: ").strip()
            password = getpass("Contraseña: ").strip()

            cursor.execute("SELECT * FROM usuarios WHERE username = %s AND activo = TRUE", (username,))
            admin = cursor.fetchone()

            if admin is None:
                print("\nUsuario administrador no encontrado.")
                return False

            if bcrypt.checkpw(password.encode('utf-8'), admin["password_hash"].encode('utf-8')):
                print(f"\nBienvenido, {username}! Acceso de administrador concedido.")
                time.sleep(2)
                return True
            else:
                print("\nContraseña incorrecta.")
                time.sleep(2)
                return False

        except mysql.connector.Error as e:
            print(f"\nError al intentar iniciar sesión en MySQL: {e}")
            return False

        finally:
            try:
                if cursor is not None:
                    cursor.close()
                if conexion is not None and conexion.is_connected():
                    conexion.close()
            except:
                pass


    def registrar_log(self, username, estado):
        from datetime import datetime
        mongo_db = self.conectar()
        if mongo_db is not None:
            mongo_db.logs.insert_one({
                "username": username,
                "estado": estado,  # "exitoso" o "fallido"
                "fecha": datetime.utcnow()
            })



