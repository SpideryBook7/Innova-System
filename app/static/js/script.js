

function reservar(cabanaId) {
    // Aquí puedes implementar la lógica para procesar la reservación de la cabaña seleccionada
}

// Esto es opcional, pero puedes ajustar la velocidad de la animación aquí
const velocidadAnimacion = 2; // 2 segundos

const texto = document.getElementById('miTexto');
const duracionAnimacion = velocidadAnimacion * 1000; // Convertir segundos a milisegundos

// Obtén el estilo actual del elemento
const estiloActual = window.getComputedStyle(texto);

// Obtén la duración actual de la animación
const duracionActual = parseFloat(estiloActual.getPropertyValue('animation-duration'));

// Verifica si la duración actual es diferente a la deseada
if (duracionActual !== duracionAnimacion) {
  // Establece la nueva duración de la animación
  texto.style.animationDuration = `${duracionAnimacion}ms`;
}

