"""Modelo de Receta."""

# Conexión con la base de datos
from app.config.mysql_connection import connect_to_mysql


class Receta:
    """Modelo de la clase Receta."""

    def __init__(self, data):
        """Constructor de la clase Receta."""

        self.id_receta = data["id_receta"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.instrucciones = data["instrucciones"]
        self.fecha = data["fecha"]
        self.usuario_id = data["usuario_id"]  # ID del usuario
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def crear_receta(cls, data):
        """Crear una nueva receta."""
        query = """
            INSERT INTO recetas (nombre, descripcion, instrucciones, fecha, usuario_id) 
            VALUES (%(nombre)s, %(descripcion)s, %(instrucciones)s, %(fecha)s, %(usuario_id)s);
        """
        resultado = connect_to_mysql().query_db(query, data)
        return resultado

    @classmethod
    def obtener_todas_las_recetas(cls):
        """Obtener todas las recetas."""

        query = """SELECT * FROM recetas;"""
        resultado = connect_to_mysql().query_db(query)
        return resultado

    @classmethod
    def obtener_receta_por_id(cls, data):
        """Método para obtener una receta por su ID."""

        query = """
            SELECT * FROM recetas
            WHERE id_receta = %(id_receta)s;
        """
        resultado = connect_to_mysql().query_db(query, data)
        return resultado[0]

    @classmethod
    def editar_receta(cls, data):
        """Método para editar una receta por su ID."""
        
        query = """
            UPDATE recetas
            SET nombre = %(nombre)s,
                descripcion = %(descripcion)s,
                instrucciones = %(instrucciones)s,
                fecha = %(fecha)s
            WHERE id_receta = %(id_receta)s;
        """
        resultado = connect_to_mysql().query_db(query, data)
        return resultado
