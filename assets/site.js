/* Comportamiento común de la página de propuestas: tema claro y oscuro, idioma (ENG por defecto y ESP) y filtros de la lista.
   El tema y el idioma se guardan en localStorage; si no se puede escribir (modo privado), la página funciona igual con los valores por defecto. */
(function () {
  function leer(clave) {
    try { return localStorage.getItem(clave); } catch (error) { return null; }
  }
  function guardar(clave, valor) {
    try { localStorage.setItem(clave, valor); } catch (error) { /* sin almacenamiento: no pasa nada */ }
  }

  // Tema
  var botonTema = document.querySelector('.boton-tema');
  var temaGuardado = leer('gpw-tema');
  if (temaGuardado) document.documentElement.setAttribute('data-theme', temaGuardado);
  if (botonTema) {
    botonTema.addEventListener('click', function () {
      var actual = document.documentElement.getAttribute('data-theme');
      var siguiente = actual === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', siguiente);
      guardar('gpw-tema', siguiente);
    });
  }

  // Idioma: solo 'en' y 'es'; cualquier otro valor guardado se ignora
  var botonesIdioma = document.querySelectorAll('.opcion-idioma');
  function aplicarIdioma(idioma) {
    document.documentElement.setAttribute('data-lang', idioma);
    document.documentElement.setAttribute('lang', idioma);
    botonesIdioma.forEach(function (boton) {
      boton.classList.toggle('activa', boton.getAttribute('data-lang-opcion') === idioma);
    });
    document.querySelectorAll('[data-placeholder-es]').forEach(function (campo) {
      campo.setAttribute('placeholder', campo.getAttribute('data-placeholder-' + idioma));
    });
    document.dispatchEvent(new CustomEvent('gpw-idioma', { detail: idioma }));
  }
  var idiomaGuardado = leer('gpw-idioma');
  aplicarIdioma(idiomaGuardado === 'es' ? 'es' : 'en');
  botonesIdioma.forEach(function (boton) {
    boton.addEventListener('click', function () {
      var idioma = boton.getAttribute('data-lang-opcion') === 'es' ? 'es' : 'en';
      guardar('gpw-idioma', idioma);
      aplicarIdioma(idioma);
    });
  });

  // Copiar la huella SHA-256 (página de descarga); sin portapapeles, el texto sigue siendo seleccionable
  document.querySelectorAll('.copiar').forEach(function (boton) {
    boton.addEventListener('click', function () {
      var origen = document.getElementById(boton.getAttribute('data-copiar'));
      if (!origen || !navigator.clipboard) return;
      var original = boton.textContent;
      var indice = document.documentElement.getAttribute('data-lang') === 'es' ? 1 : 0;
      navigator.clipboard.writeText(origen.textContent.trim()).then(function () {
        boton.textContent = boton.getAttribute('data-ok').split(' / ')[indice];
        setTimeout(function () { boton.textContent = original; }, 1500);
      }, function () { /* sin permiso: no pasa nada */ });
    });
  });

  // Filtros de la lista: por estado y por categoría (se combinan)
  var tarjetas = document.querySelectorAll('.propuesta');
  var botonesFiltro = document.querySelectorAll('.filtro');
  var cifrasContador = document.querySelectorAll('.contador-resultados .cifra');
  var filtroEstado = 'all';
  var filtroCategoria = 'all';
  function aplicarFiltros() {
    var visibles = 0;
    tarjetas.forEach(function (tarjeta) {
      var coincideEstado = filtroEstado === 'all' || tarjeta.getAttribute('data-estado') === filtroEstado;
      var coincideCategoria = filtroCategoria === 'all' || tarjeta.getAttribute('data-categoria') === filtroCategoria;
      var mostrar = coincideEstado && coincideCategoria;
      tarjeta.hidden = !mostrar;
      if (mostrar) visibles += 1;
    });
    cifrasContador.forEach(function (cifra) { cifra.textContent = String(visibles); });
  }
  botonesFiltro.forEach(function (boton) {
    boton.addEventListener('click', function () {
      var tipo = boton.getAttribute('data-filtro-tipo');
      var valor = boton.getAttribute('data-filtro-valor');
      if (tipo === 'estado') filtroEstado = valor; else filtroCategoria = valor;
      document.querySelectorAll('.filtro[data-filtro-tipo="' + tipo + '"]').forEach(function (otro) {
        otro.classList.toggle('activo', otro === boton);
      });
      aplicarFiltros();
    });
  });
})();
