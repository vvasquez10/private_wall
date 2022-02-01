from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

class Message:
    def __init__( self, id, text, emisor_id, emisor_fname, emisor_lname, receiver_id, created_at ):
        self.id = id
        self.text = text
        self.emisor_id = emisor_id    
        self.emisor_fname = emisor_fname    
        self.emisor_lname = emisor_lname  
        self.receiver_id = receiver_id
        self.created_at = created_at

    @classmethod
    def getMessagesFromUser(cls, id_user): #Devuelve una lista de objetos mensaje
        userData = {
            'receiver_id' : id_user
        }
        query = "select messages.id, text, emisor_id, receiver_id, messages.created_at, first_name as em_first_name, last_name as em_last_name from messages join users on messages.emisor_id = users.id where receiver_id = %(receiver_id)s;"
        resultado = connectToMySQL( "private_wall" ).query_db( query, userData )
        listaMensajes = []
        for message in resultado:
            listaMensajes.append( Message( message["id"], message["text"], message["emisor_id"], message["em_first_name"], message["em_last_name"], message["receiver_id"], message["created_at"]) )

        return listaMensajes

    @classmethod
    def sendMessage(cls, text, emisor_id, receiver_id ): #Devuelve una lista de objetos mensaje
        userData = {
                    'emisor_id': int(emisor_id),
                    'receiver_id' : int(receiver_id),
                    'text' : text
        }
        query = "INSERT INTO messages (text, emisor_id, receiver_id) VALUES (%(text)s, %(emisor_id)s, %(receiver_id)s);"
        resultado = connectToMySQL( "private_wall" ).query_db( query, userData )
        return resultado

    @classmethod
    def deleteMessage(cls, message_id ): 
        msgeData = {
                    'id': int(message_id)                    
        }

        query = "delete from messages where id = %(id)s;"
        resultado = connectToMySQL( "private_wall" ).query_db( query, msgeData )
        return resultado
    
    def convertidorTiempo(self):
        now = datetime.now()
        msgeAge = now - self.created_at        
        if msgeAge.days > 0:
            return f"{msgeAge.days} days ago"
        elif (math.floor(msgeAge.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(msgeAge.total_seconds() / 60)/60)} hours ago"
        elif msgeAge.total_seconds() >= 60:
            return f"{math.floor(msgeAge.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(msgeAge.total_seconds())} seconds ago"
