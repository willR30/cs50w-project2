/**
 * Aqui se manejara todo lo relacionado con el nuevo usuario del formulario
 * */

document.querySelector('form').addEventListener("submit",(e)=>{
    e.preventDefault()//indicamos que no recarge al usuario
    dato=new FormData(document.querySelector('#nuevoUsuario'))//rescatamos el dato desde el formulario
    fetch("/agregarUsuario", {method:'POST', body:dato})//eviamos el dato y el metodo al servidor
    .then(
        (respuesta)=>{
             return respuesta.json()   
        }
    ).then(
        (variable)=>{
            console.log(variable)
            window.location.pathname="/home"
        }
    )
}
)