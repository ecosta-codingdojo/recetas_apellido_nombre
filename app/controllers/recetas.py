"""Controlador de Receta."""

# App
from app import app

# Flask
from flask import render_template, redirect, request, session, flash, url_for

# Modelos
from app.models.recetas import Receta


@app.route("/recetas/nueva/", methods=["GET"])
def receta_formulario():
    """Formulario para crear una nueva receta."""

    # Proteger la ruta. Solo pueden acceder usuarios autenticados.
    if "id_usuario" not in session:
        return redirect(url_for("index"))

    return render_template("recetas/receta_nueva.html")


@app.route("/recetas/crear/", methods=["POST"])
def receta_crear():
    """Controlador para crear una nueva receta."""

    # Datos del formulario
    data = {
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "instrucciones": request.form["instrucciones"],
        "fecha": request.form["fecha"],
        "usuario_id": session["id_usuario"],
    }

    # Crear la receta
    Receta.crear_receta(data)

    # Luego de crear la receta, redirigimos al dashboard
    return redirect(url_for("dashboard"))


@app.route("/recetas/<int:id_receta>/", methods=["GET"])
def receta_detalle(id_receta):
    """Detalle de una receta por su ID."""

    # El ID de la receta se recibe como parámetro en la URL
    data = {"id_receta": id_receta}

    # Obtener la receta por su ID
    receta = Receta.obtener_receta_por_id(data)

    # Crear el contexto para el template
    context = {"receta": receta}

    return render_template("recetas/receta_detalle.html", **context)


@app.route("/recetas/editar/<int:id_receta>/", methods=["GET"])
def receta_editar_formulario(id_receta):
    """Formulario para editar una receta."""

    # El ID de la receta se recibe como parámetro en la URL
    data = {"id_receta": id_receta}

    # Obtener la receta por su ID
    receta = Receta.obtener_receta_por_id(data)

    # Crear el contexto para el template
    context = {"receta": receta}

    return render_template("recetas/receta_editar.html", **context)


@app.route("/recetas/editar/", methods=["POST"])
def receta_editar():
    """Controlador para editar una receta."""

    # Datos del formulario
    data = {
        "id_receta": request.form["id_receta"],
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "instrucciones": request.form["instrucciones"],
        "fecha": request.form["fecha"],
    }

    # Editar la receta
    Receta.editar_receta(data)

    # Luego de editar la receta, redirigimos al dashboard
    return redirect(url_for("dashboard"))