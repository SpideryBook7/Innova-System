// Obtén todas las galerías de imágenes
const galerias = document.querySelectorAll('.galeria');

// Agrega el evento de clic a cada imagen de la galería
galerias.forEach((galeria) => {
  const imagenes = galeria.querySelectorAll('img');
  imagenes.forEach((imagen) => {
    imagen.addEventListener('click', mostrarImagen);
  });
});

// Función para mostrar la imagen seleccionada
function mostrarImagen(event) {
  const imagenSeleccionada = event.target.src;
  // Aquí puedes agregar la lógica para mostrar la imagen en un modal o en otro lugar de tu preferencia
  console.log('Imagen seleccionada:', imagenSeleccionada);
}
