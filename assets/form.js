/* Formulario de propuestas: validación, textos de las listas en el idioma elegido y envío a la hoja de Google (formResponse) en segundo plano.
   Medidas contra el spam: campo trampa, tiempo mínimo desde la carga, límite de longitud y un envío por minuto desde este navegador. */
(function () {
  var formulario = document.getElementById('formulario-propuesta');
  if (!formulario) return;
  var configuracion = window.GPW_FORM || null;
  var cargadoEn = Date.now();
  var SEGUNDOS_MINIMOS = 5;
  var MILISEGUNDOS_ENTRE_ENVIOS = 60000;

  var campoTitulo = document.getElementById('titulo');
  var campoDescripcion = document.getElementById('descripcion');
  var campoCategoria = document.getElementById('categoria');
  var campoNombre = document.getElementById('nombre');
  var contenedorNombre = document.getElementById('campo-nombre');
  var campoApoyo = document.getElementById('apoyo');
  var campoTrampa = document.getElementById('sitio_web');
  var mensajeExito = document.getElementById('mensaje-exito');
  var mensajeError = document.getElementById('mensaje-error');
  var botonEnviar = formulario.querySelector('.boton-enviar');

  function figuraElegida() {
    var elegida = formulario.querySelector('input[name="figura"]:checked');
    return elegida ? elegida.value : '';
  }
  function esAnonimo() {
    return configuracion ? figuraElegida() === configuracion.opcion_anonimo : figuraElegida().indexOf('Anonymous') === 0;
  }

  // Los textos de las listas desplegables cambian con el idioma
  function traducirOpciones(idioma) {
    [campoCategoria, campoApoyo].forEach(function (lista) {
      Array.prototype.forEach.call(lista.options, function (opcion) {
        var texto = opcion.getAttribute('data-' + idioma);
        if (texto) opcion.textContent = texto;
      });
    });
  }
  document.addEventListener('gpw-idioma', function (evento) { traducirOpciones(evento.detail); });
  traducirOpciones(document.documentElement.getAttribute('data-lang') || 'en');

  // El nombre solo se pide si la persona no quiere ser anónima
  function actualizarNombre() {
    contenedorNombre.hidden = esAnonimo();
    if (esAnonimo()) campoNombre.value = '';
  }
  formulario.querySelectorAll('input[name="figura"]').forEach(function (radio) {
    radio.addEventListener('change', actualizarNombre);
  });
  actualizarNombre();

  function mostrarError() { mensajeError.hidden = false; mensajeExito.hidden = true; botonEnviar.disabled = false; }

  formulario.addEventListener('submit', function (evento) {
    evento.preventDefault();
    mensajeError.hidden = true;
    mensajeExito.hidden = true;

    var titulo = campoTitulo.value.trim();
    var descripcion = campoDescripcion.value.trim();
    if (!titulo || !descripcion || !campoCategoria.value || !figuraElegida()) { mostrarError(); return; }
    if (campoTrampa.value) { mensajeExito.hidden = false; return; }                       // un robot rellenó la trampa: se finge que ha ido bien
    if (Date.now() - cargadoEn < SEGUNDOS_MINIMOS * 1000) { mostrarError(); return; }     // demasiado rápido para una persona
    var ultimoEnvio = 0;
    try { ultimoEnvio = parseInt(localStorage.getItem('gpw-ultimo-envio') || '0', 10); } catch (error) { ultimoEnvio = 0; }
    if (Date.now() - ultimoEnvio < MILISEGUNDOS_ENTRE_ENVIOS) { mostrarError(); return; }
    if (!configuracion) { mostrarError(); return; }                                       // el formulario aún no está conectado a la hoja

    var datos = new URLSearchParams();
    datos.append(configuracion.entradas.titulo, titulo);
    datos.append(configuracion.entradas.descripcion, descripcion);
    datos.append(configuracion.entradas.categoria, campoCategoria.value);
    datos.append(configuracion.entradas.figura, figuraElegida());
    if (!esAnonimo() && campoNombre.value.trim()) datos.append(configuracion.entradas.nombre, campoNombre.value.trim());
    if (campoApoyo.value) datos.append(configuracion.entradas.apoyo, campoApoyo.value);

    botonEnviar.disabled = true;
    fetch(configuracion.accion, { method: 'POST', mode: 'no-cors', body: datos })
      .then(function () {
        try { localStorage.setItem('gpw-ultimo-envio', String(Date.now())); } catch (error) { /* sin almacenamiento */ }
        formulario.reset();
        actualizarNombre();
        mensajeExito.hidden = false;
        botonEnviar.disabled = false;
      })
      .catch(mostrarError);
  });
})();
