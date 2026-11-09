# Archivo: run.py (en la raíz de mi_proyecto/)
from app import create_app
from flask_debugtoolbar import DebugToolbarExtension ##tambien se añade el debuger auque no este en los apuntes

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

toolbar = DebugToolbarExtension(app)