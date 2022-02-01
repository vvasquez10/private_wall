from flask import render_template, request, redirect, session, flash
import re
from flask_app import app
from flask_app.modelos.Usuario import Usuario
from flask_app.modelos.Message import Message


from flask_bcrypt import Bcrypt

#Regex:
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #At least 8 character, 1 number, 1 upper and 1 letter


bcrypt = Bcrypt( app )

@app.route( '/', methods=['GET'] )
def despliegaInicio():
    return render_template( "index.html" )

@app.route( '/createUser', methods=['POST'] )
def creaUser():

    validationApproved = True
    print("Esta entrando aquí")
    if request.form['password'] != request.form['conf_password']:
        flash("Ambas contraseñas no coinciden.", "registration")
        validationApproved = False    

    if EMAIL_REGEX.match( request.form["email"]) == None :
        flash("Email incorrecto.", "registration")
        validationApproved = False
    
    if PASSWORD_REGEX.match( request.form["password"] ) == None :
        flash("La contraseña debe tener al menos 8 caracteres, 1 letra y 1 número.", "registration") 
        validationApproved = False 
    
    # Validador final
    if not validationApproved:
        return redirect("/")
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password']) #Encriptando la contraseña aceptada

        newUser = {
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password": pw_hash        
        }

        resultado = Usuario.createUser( newUser )
        print("este es el id", resultado, newUser)
        session["logged"] = True
        session["id_user"] = resultado
        session["first_name"] = Usuario.getUserById(resultado).first_name #Se pasa solo el ID del usuario y retorna un obj Usuario
    
        return redirect("/dashboard")
    
@app.route( '/dashboard', methods=["GET"] )
def despliegaDashboard():
    if 'id_user' in session:
        user_name = session["first_name"]
        listaMensajes = Message.getMessagesFromUser(session["id_user"]) # Captura todos los mensajes en la BD segun el usuario actual
        users = Usuario.get_all()

        return render_template( "dashboard.html", user_name = user_name, listaMensajes=listaMensajes, users=users)
    else:
        return redirect( '/' )

    
@app.route( '/login', methods=["POST"] )
def login():
    usuario = Usuario.getUserByEmail(request.form["email"])
    validationApproved = True

    if EMAIL_REGEX.match( request.form["email"]) == None :
        flash("Email incorrecto", "login")
        validationApproved = False
    
    if usuario == False:
        flash("Usuario no encontrado, verifique sus credenciales", "login")
        validationApproved = False     
              
    if PASSWORD_REGEX.match( request.form["password"] ) == None :
        flash("Contraseña incorrecta", "login") 
        validationApproved = False 
    
    # Validador final
    if not validationApproved:
        return redirect("/")

    else:
        if not bcrypt.check_password_hash( usuario.password, request.form['password'] ):
            flash( "El password es incorrecto", "login" )
            return redirect( '/' )
        else:
            session["logged"] = True
            session["id_user"] = usuario.id
            session["first_name"] =usuario.first_name #Se pasa solo el ID del usuario y retorna un obj Usuario
        
            return redirect("/dashboard")

@app.route( '/logout', methods=["GET"] )
def logoutUsuario():
    session.clear()
    return redirect( '/' )
