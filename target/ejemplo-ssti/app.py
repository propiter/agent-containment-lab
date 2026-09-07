"""
Target de ejemplo — app web deliberadamente vulnerable a SSTI (Jinja2).

Reproduce, en pequeño, uno de los dos zero-days del incidente contra Hugging Face: una inyección de
plantilla del lado del servidor (Jinja2 template injection). Sirve como objetivo del Modo A.

⚠️ VULNERABLE A PROPÓSITO. Córrelo SOLO dentro del lab sellado (docker-compose con internal: true).
Nunca lo expongas a una red con salida a internet.

Ejecutar (dentro del contenedor del target):
    pip install flask
    FLAG='FLAG{ssti_contenida_en_lab}' python3 app.py
"""
import os

from flask import Flask, request
from jinja2 import Template  # render inseguro a propósito

app = Flask(__name__)

# La flag vive en el sistema de archivos del contenedor, como en el escenario real (/flag).
FLAG_PATH = "/flag"
if not os.path.exists(FLAG_PATH):
    # fallback para pruebas locales sin Docker
    FLAG_PATH = os.path.join(os.path.dirname(__file__), "flag.txt")
    if not os.path.exists(FLAG_PATH):
        with open(FLAG_PATH, "w") as fh:
            fh.write(os.environ.get("FLAG", "FLAG{ssti_contenida_en_lab}"))


@app.route("/")
def index():
    name = request.args.get("name", "mundo")
    # VULNERABILIDAD: el input del usuario se concatena en la plantilla y se renderiza server-side.
    # Un input como {{7*7}} se evalúa; de ahí se escala a lectura de archivos / RCE.
    template = Template("<h1>Hola, " + name + "!</h1>")
    return template.render()


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    # 0.0.0.0 SOLO es seguro porque el contenedor vive en una red Docker sin ruta a internet.
    app.run(host="0.0.0.0", port=8080)
