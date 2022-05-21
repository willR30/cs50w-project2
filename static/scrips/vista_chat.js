//instanciamos el socket
socket=io()

//acedemos a el nombre de la sala mediante la ruta
ruta=location.pathname.split("/")
nombre_sala=decodeURI(ruta[ruta.length-1])
socket.emit('entrar',nombre_sala)

//Cargamos los mensajes dentro del contenedor de mensajes
//trabajamos con las variabels que vamos recibiendo desde el servidor
socket.on(nombre_sala,(variable)=>{
    document.querySelector('#contendor_chats').textContent=""
    //recorremos el arreglo que recibimos 
    for(i of variable.mensaje){
        parrafo=document.createElement('p')
        parrafo.textContent=i.enviado_por+" : "+i.contenido_mensaje
        //los mostramos dentro del contenedor
        document.querySelector('#contendor_chats').append(parrafo)
    }
    
})

document.querySelector('form').addEventListener("submit",(e)=>{
    e.preventDefault()//pra no recarge el usuario
    mensaje= new FormData(
        document.querySelector('#mi_chat')
    )
    if(mensaje!=null){
        fetch("/vista_chat/"+nombre_sala, {method:'POST', body:mensaje})//eviamos el dato y el metodo al servidor
        .then(
            (respuesta)=>{
                return respuesta.json()
            }
        ).then(
            (variable)=>{
                console.log(variable)
                //Ejecutamos de nuevo el mismo emit para cargar nuevamente los mensajes en el historial
                socket.emit('entrar',nombre_sala)

            }
        )
    }else{
        alert("No se admiten campos nulos")
    }
    
})

