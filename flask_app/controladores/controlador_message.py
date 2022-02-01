from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.modelos.Message import Message


# Tareas
#### Mensaje de peligro
#### Controlar cuantos cuadros de mensajeria salen y que pasa si no hay mensajes recibidos



@app.route( '/sendMessage', methods=['POST'] )
def enviaMensaje():
    resultado = Message.sendMessage(request.form['messageText'], session["id_user"], request.form['destinatary'])
    return redirect( "/dashboard")


@app.route( '/deleteMessage', methods=['POST'] )
def eliminaMensaje():
    resultado = Message.deleteMessage(request.form['messageId'])
    return redirect( "/dashboard")
