from crypt import methods
from urllib import response
from flask import Flask, jsonify, redirect, render_template, request, session, url_for,make_response
from flask_socketio import SocketIO, emit,send,join_room, leave_room
import requests
from sqlalchemy import false


app = Flask(__name__)
app.config['SECRET_KEY'] = 'reemplazar_clave_secreta'

# Instancia de SocketIo
socketio = SocketIO(app)

usuarios_lista=[]
#guardamos la sala de lista en un diccionario
salas_de_chat_lista=[{
        'nombre':'Familia',
        'mensaje': [{'enviado_por':'Administrador','contenido_mensaje':'Podras ver un máximo de 100 chats'}]
    },
    {
     'nombre':'Trabajo',
     'mensaje': [{'enviado_por':'Administrador','contenido_mensaje':'Podras ver un máximo de 100 chats'}]   
    },{
        'nombre':'Amigos',
        'mensaje': [{'enviado_por':'Administrador','contenido_mensaje':'Podras ver un máximo de 100 chats'}]
    }
]



@app.route("/")
def index():
    print(usuarios_lista)
    print(request.cookies.get('sesion'))
    if request.cookies.get('sesion') in usuarios_lista :
        
        return redirect(url_for('home'))
    else:    
        return redirect(url_for('agregar_usuario'))

@app.route("/agregarUsuario", methods=['GET','POST'])
def agregar_usuario():
    if request.method=="POST":
        #recatamos el valor del formulario
        usuario=request.form.get("txt_nombre_usuario")
        #validamos si existe un usuario con ese nombre
        if(usuario in usuarios_lista):
            print("Debes de agregar otro nombre de usuario")
            return "Ya existe un usuario con ese nombre"
        else:       
            #creamos la cookie de la sesion
            respuesta=make_response(jsonify({'ingreso': True, 'usuario':usuario}))
            respuesta.set_cookie('sesion',usuario)
            #agregamos el usuario a la lista
            usuarios_lista.append(usuario)
            return respuesta
    else:
        return render_template('nuevo_usuario.html')

@app.route("/home")
def home():
            
    return render_template('home.html',salas_de_chat=salas_de_chat_lista,usuario=request.cookies.get('sesion'))

@app.route("/salir")
def salir():
    #salimos y eliminamos la coockie
    respuesta=make_response(redirect(url_for('agregar_usuario')))
    respuesta.set_cookie('sesion','',expires=0)#borramos la coockie del servidor
    return respuesta

@app.route("/vista_chat/<sala_de_chat>", methods=['GET','POST'])
def vista_chat(sala_de_chat):
    if request.method=="POST":
        mensaje=request.form.get("txt_chat")
        #buscamos el canal
        canal=None
        for sala in salas_de_chat_lista:
            if sala['nombre'] == sala_de_chat:
                canal=sala
                break
        #agregamos el mensaje
        if len(sala['mensaje'])>100:
            return jsonify({'error':'Error has alcanzado el limite de mensajes'})
        else:
            sala['mensaje'].append({'enviado_por': request.cookies.get('sesion'),'contenido_mensaje':mensaje})
            return jsonify({'sin_error':'Mensaje enviado exitosamente'})

    return render_template('vista_chat.html',sala_de_chat=sala_de_chat,usuario=request.cookies.get('sesion'))
    


@socketio.on("entrar")
def entrar_sala(nombre_sala):
    join_room(nombre_sala)
    #emit('mensaje', f'Un usuario ha entrado a la sala {nombre_sala}', broadcast=True, include_self=False, to=nombre_sala)
    canal=None
    for sala in salas_de_chat_lista:
        if sala['nombre'] == nombre_sala:
            canal=sala
            break
       
    emit(nombre_sala, {
        'mensaje': canal['mensaje']
    }, room=nombre_sala)
    
@app.route("/nueva_sala", methods=['GET','POST'])
def nueva_sala():
    if request.method=="POST":
        nombre_sala=request.form.get("txt_nombre_sala")
        if len(nombre_sala)>0:
            #validamos si existe una sala con ese nombre
            existe=False
            for sala in salas_de_chat_lista:
                if sala['nombre'] == nombre_sala:
                    existe=True
                    break
            if(existe):
                return 'Ya existe una sala con ese nombre, agrégala con otro nombre'
            else:
                sala_nueva={
                    'nombre':nombre_sala,
                    'mensaje':[{'enviado_por':'Administrador','contenido_mensaje':'Podras ver un máximo de 100 chats'}]
                }
                salas_de_chat_lista.append(sala_nueva)
                return redirect(url_for('home'))
        else:
            return f'Debes de agregar un nombre a tu sala de chat'


@app.route("/eliminar_sala/<sala_de_chat>", methods=['GET','POST'])
def eliminar_sala(sala_de_chat):
    #ubicamos la sala de chat dentro de la lista
    index=0
    for sala in salas_de_chat_lista:
        if sala['nombre'] == sala_de_chat:
            break
        index=index+1
    
    salas_de_chat_lista.pop(index)
    return redirect(url_for('home'))

#ejecutamos la app
if __name__ == '__main__':
    socketio.run(app)