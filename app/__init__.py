"""Archivo de configuración de nuestra aplicación."""

# Standard libraries
import os

# Flask
from flask import Flask

# Python-dotenv
from dotenv import load_dotenv  # ¡Esto es nuevo!

# Es necesario para cargar las variables de entorno
load_dotenv()

# Instancia de Flask
app = Flask(__name__)

# Secret key
app.secret_key = os.getenv("SECRET_KEY")
