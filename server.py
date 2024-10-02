"""Server app."""

# Importar la aplicación
from app import app

# Importar los controladores de la aplicación
from app.controllers.usuarios import index, dashboard, registrar_usuario, iniciar_sesion, cerrar_sesion
from app.controllers.recetas import receta_formulario, receta_crear, receta_detalle, receta_editar_formulario, receta_eliminar

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(debug=True, port=5001)
