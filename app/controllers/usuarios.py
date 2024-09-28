"""Controlador de Usuario."""
from time import process_time

# App
from app import app

# Flask
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt

# Modelos
from app.models.usuarios import Usuario
from app.models.recetas import Receta

# Variable para encriptar contraseñas
bcrypt = Bcrypt(app)


@app.route("/", methods=["GET"])
def index():
    """Ruta inicial dónde se muestran los formularios."""

    # Validar si el usuario ya inició sesión, lo redirigimos al dashboard
    if "id_usuario" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/dashboard/", methods=["GET"])
def dashboard():
    """Ruta del dashboard luego de iniciar sesión."""

    # Validar si el usuario no ha iniciado sesión, lo redirigimos al index
    if "id_usuario" not in session:
        return redirect(url_for("index"))

    # Obtener el usuario por su ID. El ID se encuentra en la sesión.
    id_usuario = session["id_usuario"]
    data = {"id_usuario": id_usuario}
    usuario = Usuario.obtener_usuario_por_id(data)

    # Obtener todas las recetas
    recetas = Receta.obtener_todas_las_recetas()

    # Creamos un contexto para enviar los datos al template
    context = {
        "usuario": usuario,
        "recetas": recetas,
    }

    return render_template("dashboard.html", **context)


@app.route("/registrar/", methods=["POST"])
def registrar_usuario():
    """Registrar un nuevo usuario."""

    # Datos del formulario
    data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "correo_electronico": request.form["correo_electronico"],
        "contrasena": request.form["contrasena"],
        "confirmar_contrasena": request.form["confirmar_contrasena"],
    }
    print(data)

    # Validar el registro
    if not Usuario.validar_registro(data):
        return redirect(url_for("index"))

    # Encriptar la contraseña
    data["contrasena"] = bcrypt.generate_password_hash(data["contrasena"])

    print(data)

    # Mostar mensaje de éxito
    flash("Usuario registrado correctamente", "success")
    # Crear el usuario en la base de datos
    Usuario.crear_usuario(data)
    return redirect(url_for("index"))


@app.route("/iniciar-sesion/", methods=["POST"])
def iniciar_sesion():
    """Ruta para iniciar sesión."""

    # Datos del formulario
    data = {
        "correo_electronico": request.form["correo_electronico"],
        "contrasena": request.form["contrasena"],
    }

    # Obtenemos el usuario por correo electrónico
    usuario = Usuario.obtener_usuario_por_email(data)

    if not usuario:
        # Si no existe el usuario mostramos un mensaje de error
        flash("El usuario no existe", "danger")
        return redirect(url_for("index"))

    # Desencriptamos la contraseña
    contrasena_valida = bcrypt.check_password_hash(usuario.contrasena, data["contrasena"])

    if not contrasena_valida:
        # Si la contraseña no coincide mostramos un mensaje de error
        flash("La contraseña es incorrecta", "danger")
        return redirect(url_for("index"))

    # Guardamos el ID del usuario en la sesión
    session["id_usuario"] = usuario.id_usuario
    return redirect(url_for("dashboard"))


@app.route("/cerrar-sesion/", methods=["GET"])
def cerrar_sesion():
    """Cerrar sesión del usuario."""

    # Limpiar la sesión
    session.clear()
    # Mostrar mensaje de éxito
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("index"))
