from flask_app import app
from flask_app.controladores import controlador_usuario
from flask_app.controladores import controlador_message

if __name__ == "__main__":
    app.run( debug = True )