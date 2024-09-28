"""Modelo de Usuario."""

# Conexión con la base de datos
from app.config.mysql_connection import connect_to_mysql

# Flask
from flask import flash


class Usuario:
    """Clase del modelo de Usuario."""

    def __init__(self, data):
        self.id_usuario = data["id_usuario"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.correo_electronico = data["correo_electronico"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def crear_usuario(cls, data):
        """Método que permite crear un nuevo usuario."""

        query = """
            INSERT INTO usuarios (nombre, apellido, correo_electronico, contrasena)
            VALUES (%(nombre)s, %(apellido)s, %(correo_electronico)s, %(contrasena)s);
        """
        resultado = connect_to_mysql().query_db(query, data)
        return resultado

    @classmethod
    def obtener_usuario_por_email(cls, data):
        """Método que permite consultar si el usuario está registrado."""

        query = """
            SELECT * FROM usuarios
            WHERE correo_electronico = %(correo_electronico)s;
        """
        resultado = connect_to_mysql().query_db(query, data)

        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_usuario_por_id(cls, data):
        """Método que permite obtener un usuario por su ID."""

        query = """
            SELECT * FROM usuarios
            WHERE id_usuario = %(id_usuario)s;
        """
        resultado = connect_to_mysql().query_db(query, data)

        if not resultado:
            return None
        return cls(resultado[0])

    @staticmethod
    def validar_registro(data):
        """Método que permite validar el registro de un usuario."""

        es_valido = True

        # Validar que el nombre tenga al menos 2 caracteres
        if len(data["nombre"]) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger")
            es_valido = False
            return es_valido

        # Validar que el apellido tenga al menos 2 caracteres
        if len(data["apellido"]) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "danger")
            es_valido = False
            return es_valido

        # Validar que el correo electrónico no esté registrado
        if Usuario.obtener_usuario_por_email(data):
            flash("El correo electrónico ya está registrado.", "danger")
            es_valido = False
            return es_valido

        # Validar que las contraseñas coincidan
        if data["contrasena"] != data["confirmar_contrasena"]:
            flash("Las contraseñas no coinciden.", "danger")
            es_valido = False
            return es_valido

        # Validar que la contraseña tenga al menos 8 caracteres
        if len(data["contrasena"]) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "danger")
            es_valido = False
            return es_valido

        return es_valido
