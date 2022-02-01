from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:
    def __init__( self, id, first_name, last_name, email, password ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


    @classmethod
    def createUser(cls, dataUser): #no puedo enviar un objeto porque estaría incompleto, sino que le mando un dic con los datos que tengo
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"        
        resultado = connectToMySQL( "private_wall" ).query_db( query, dataUser )
        return resultado # Devuelve un ID
    
    @classmethod
    def getUserById( cls, user_id ):
        user = {
            "id" : user_id
        }

        query = "SELECT * FROM users WHERE id = %(id)s;"
        resultado = connectToMySQL( "private_wall" ).query_db( query, user)
        usuarioResultado = Usuario( resultado[0]["id"], resultado[0]["first_name"], resultado[0]["last_name"], resultado[0]["email"], resultado[0]["password"] )
        return usuarioResultado #Retorna un diccionario con la info del usuario
    
    @classmethod
    def getUserByEmail( cls, user_email ):
        user = {
            "email" : user_email
        }

        query = "SELECT * FROM users WHERE email = %(email)s;"
        resultado = connectToMySQL( "private_wall" ).query_db( query, user)
        print(resultado)
        if resultado == ():
            return False
        else:
            usuarioResultado = Usuario( resultado[0]["id"], resultado[0]["first_name"], resultado[0]["last_name"], resultado[0]["email"], resultado[0]["password"] )
            return usuarioResultado #Retorna un obj usuario o False en su defecto
        
    
    @classmethod
    def get_all(cls):      
        query = "SELECT * FROM users;"
        resultado = connectToMySQL( "private_wall" ).query_db( query)
        listaUsuarios=[]
        for user in resultado:
            listaUsuarios.append(Usuario( user["id"], user["first_name"], user["last_name"], user["email"], user["password"] ))
        return listaUsuarios #Retorna un diccionario con la info del usuario