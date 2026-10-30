# Genera la página pública de propuestas de GPW Evolution '98 (lista + formulario), bilingüe (ENG por defecto y ESP), a partir de lista.json.
# Salida: index.html (la lista, con encabezado y detalle por propuesta), propose.html (el formulario) y assets/ (estilo, JavaScript y banderas).
# Los apoyos de cada propuesta se cuentan del CSV saneado «publico.csv» (si existe): columna «apoya», que empieza por el número de la propuesta.
# El formulario envía a la hoja de Google por el mismo canal que el formulario de Google; sus datos salen de form_config.json (si falta, la página
# enseña un aviso y enlaza el formulario de Google como alternativa).
# Uso: python generar_pagina.py [carpeta_de_salida]
import csv
import html
import json
import os
import shutil
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(CARPETA, "..", ".."))
RUTA_LISTA = os.path.join(CARPETA, "lista.json")
RUTA_CONFIG_FORMULARIO = os.path.join(CARPETA, "form_config.json")
RUTA_MOD = os.path.join(CARPETA, "mod.json")
CARPETA_PAQUETE = os.path.join(RAIZ, "datos", "paquete_mod", "evolution_98_v0.1")
RUTA_PUBLICO_CSV = os.environ.get("GPW_PUBLICO_CSV", os.path.join(RAIZ, "datos", "propuestas", "publico.csv"))
CARPETA_SITIO = os.path.join(CARPETA, "sitio")
CARPETA_SALIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "datos", "propuestas", "sitio_publico")

# Textos del formulario de Google tal como están en sus opciones (deben coincidir al enviar)
OPCION_NOMBRE = "With my name / Con mi nombre"
OPCION_ALIAS = "With my forum or Discord alias / Con mi alias del foro o de Discord"
OPCION_ANONIMO = "Anonymous / Anónimo"


def texto(ingles, espanol):
    """Un texto en línea con las dos lenguas; el CSS muestra solo la elegida."""
    return '<span class="i18n-en">%s</span><span class="i18n-es">%s</span>' % (html.escape(ingles), html.escape(espanol))


def bloque(ingles, espanol):
    """Igual que texto(), pero como bloque (para párrafos)."""
    return '<span class="i18n-en bloque">%s</span><span class="i18n-es bloque">%s</span>' % (html.escape(ingles), html.escape(espanol))


def cabecera_pagina(titulo_ingles, titulo_espanol, miga_ingles, miga_espanol, enlace_accion, texto_accion_ingles, texto_accion_espanol,
                    clase_body="", enlace_descarga=True):
    return """<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="Community proposals for GPW Evolution '98, a Grand Prix World 1998 mod.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body class="%(clase_body)s">

<header class="sitio">
  <div>
    <div class="marca"><a href="index.html">GPW Evolution '98</a></div>
    <div class="migas">%(miga)s</div>
  </div>
  <div class="acciones">
    %(descarga)s<a class="boton-accion" href="%(enlace_accion)s">%(texto_accion)s</a>
    <div class="selector-idioma">
      <button class="opcion-idioma" data-lang-opcion="en" type="button"><img class="bandera-boton" src="assets/flags/gb.svg" alt="EN"> ENG</button>
      <button class="opcion-idioma" data-lang-opcion="es" type="button"><img class="bandera-boton" src="assets/flags/es.svg" alt="ES"> ESP</button>
    </div>
    <button class="boton-tema" type="button">%(tema)s</button>
  </div>
</header>

<main>
""" % {
        "titulo": html.escape("GPW Evolution '98 · " + titulo_ingles + " | " + titulo_espanol),
        "miga": texto(miga_ingles, miga_espanol),
        "enlace_accion": enlace_accion,
        "texto_accion": texto(texto_accion_ingles, texto_accion_espanol),
        "tema": texto("Light / Dark", "Claro / oscuro"),
        "clase_body": clase_body,
        "descarga": ('<a class="enlace-nav" href="mod.html">%s</a>' % texto("Download", "Descarga")) if enlace_descarga else "",
    }


def pie_pagina(extra_script=""):
    return """
</main>

<footer class="pie">
  %(aviso)s
</footer>

<script src="assets/site.js"></script>
%(extra)s
</body>
</html>
""" % {
        "aviso": bloque(
            "Unofficial fan project for Grand Prix World. Proposals are reviewed by hand; nothing goes into the mod without the author's approval.",
            "Proyecto de aficionados para Grand Prix World, sin carácter oficial. Las propuestas se revisan a mano; nada entra en el mod sin la aprobación del autor.",
        ),
        "extra": extra_script,
    }


def cargar_lista():
    with open(RUTA_LISTA, encoding="utf-8") as fichero:
        return json.load(fichero)


def contar_apoyos():
    """Cuenta, por número de propuesta, las filas del CSV saneado cuya columna «apoya» empieza por ese número."""
    apoyos = {}
    if not os.path.exists(RUTA_PUBLICO_CSV):
        return apoyos
    with open(RUTA_PUBLICO_CSV, encoding="utf-8-sig", newline="") as fichero:
        for fila in csv.DictReader(fichero):
            valor = (fila.get("apoya") or "").strip()
            digitos = ""
            for caracter in valor:
                if caracter.isdigit():
                    digitos += caracter
                else:
                    break
            if digitos:
                numero = int(digitos)
                apoyos[numero] = apoyos.get(numero, 0) + 1
    return apoyos


def generar_lista(datos, apoyos):
    categorias = datos["categorias"]
    estados = datos["estados"]
    propuestas = datos["propuestas"]
    categorias_usadas = []
    for propuesta in propuestas:
        if propuesta["categoria"] not in categorias_usadas:
            categorias_usadas.append(propuesta["categoria"])

    partes = [cabecera_pagina("Community proposals", "Propuestas de la comunidad", "Proposals", "Propuestas",
                              "propose.html", "Send a proposal", "Enviar una propuesta")]
    partes.append("  <h1>%s</h1>\n" % texto("Community proposals", "Propuestas de la comunidad"))
    partes.append('  <p class="subtitulo">%s</p>\n' % bloque(
        "Ideas gathered from the Grand Prix World community for GPW Evolution '98. Check the list before you send yours: if it is already here, support it instead of repeating it.",
        "Ideas recogidas en la comunidad de Grand Prix World para GPW Evolution '98. Mira la lista antes de enviar la tuya: si ya está, apóyala en lugar de repetirla."))

    # Filtros
    partes.append('  <div class="filtros" aria-label="Status / Estado">\n')
    partes.append('    <button class="filtro activo" type="button" data-filtro-tipo="estado" data-filtro-valor="all">%s</button>\n' % texto("All", "Todas"))
    for clave, etiqueta in estados.items():
        partes.append('    <button class="filtro" type="button" data-filtro-tipo="estado" data-filtro-valor="%s">%s</button>\n' % (clave, texto(etiqueta["en"], etiqueta["es"])))
    partes.append("  </div>\n")
    partes.append('  <div class="filtros" aria-label="Category / Categoría">\n')
    partes.append('    <button class="filtro activo" type="button" data-filtro-tipo="categoria" data-filtro-valor="all">%s</button>\n' % texto("All topics", "Todos los temas"))
    for clave in categorias_usadas:
        etiqueta = categorias[clave]
        partes.append('    <button class="filtro" type="button" data-filtro-tipo="categoria" data-filtro-valor="%s">%s</button>\n' % (clave, texto(etiqueta["en"], etiqueta["es"])))
    partes.append("  </div>\n")
    partes.append('  <p class="contador-resultados"><span class="i18n-en">Showing <span class="cifra">%d</span> proposals</span>'
                  '<span class="i18n-es">Mostrando <span class="cifra">%d</span> propuestas</span></p>\n' % (len(propuestas), len(propuestas)))

    # Tarjetas
    partes.append('  <div class="lista-propuestas">\n')
    for propuesta in propuestas:
        numero = propuesta["numero"]
        estado = estados[propuesta["estado"]]
        categoria = categorias[propuesta["categoria"]]
        partes.append('<article class="propuesta" id="p%d" data-estado="%s" data-categoria="%s">\n' % (numero, propuesta["estado"], propuesta["categoria"]))
        partes.append('  <div class="cabecera-propuesta"><span class="numero">%s</span> <span class="estado %s">%s</span> <span class="categoria">· %s</span></div>\n' % (
            texto("No. %d" % numero, "N.º %d" % numero), propuesta["estado"], texto(estado["en"], estado["es"]), texto(categoria["en"], categoria["es"])))
        partes.append("  <h3>%s</h3>\n" % texto(propuesta["titulo"]["en"], propuesta["titulo"]["es"]))
        partes.append("  <ul>\n")
        partes.append('    <li><span class="etiqueta-detalle">%s</span> %s</li>\n' % (texto("What it asks:", "Qué pide:"), texto(propuesta["pide"]["en"], propuesta["pide"]["es"])))
        partes.append('    <li><span class="etiqueta-detalle">%s</span> %s</li>\n' % (texto("Where it stands:", "Cómo está:"), texto(propuesta["hoy"]["en"], propuesta["hoy"]["es"])))
        partes.append("  </ul>\n")
        cantidad = apoyos.get(numero, 0)
        if cantidad:
            partes.append('  <div class="apoyos">%s</div>\n' % texto("Supporters: %d" % cantidad, "Apoyos: %d" % cantidad))
        partes.append("</article>\n")
    partes.append("  </div>\n")
    partes.append(pie_pagina())
    return "".join(partes)


def cargar_config_formulario():
    if not os.path.exists(RUTA_CONFIG_FORMULARIO):
        return None
    with open(RUTA_CONFIG_FORMULARIO, encoding="utf-8") as fichero:
        return json.load(fichero)


def generar_formulario(datos):
    categorias = datos["categorias"]
    propuestas = datos["propuestas"]
    configuracion = cargar_config_formulario()

    partes = [cabecera_pagina("Send a proposal", "Enviar una propuesta", "Send a proposal", "Enviar una propuesta",
                              "index.html", "See the list", "Ver la lista")]
    partes.append("  <h1>%s</h1>\n" % texto("Send a proposal", "Enviar una propuesta"))
    partes.append('  <p class="subtitulo">%s</p>\n' % bloque(
        "One proposal per submission. You can write in English or Spanish. Check the list first: if your idea is already there, pick it in the last field to support it.",
        "Una propuesta por envío. Puedes escribir en inglés o en español. Mira primero la lista: si tu idea ya está, elígela en el último campo para apoyarla."))

    partes.append('  <form class="formulario" id="formulario-propuesta" novalidate>\n')
    partes.append('    <div class="campo"><label for="titulo">%s</label><input type="text" id="titulo" maxlength="120" required>'
                  '<span class="ayuda">%s</span></div>\n' % (
                      texto("Short title", "Título corto"),
                      texto("One line, for example: \"Favourite circuits for drivers\".", "Una línea, por ejemplo: «Circuitos favoritos para los pilotos».")))
    partes.append('    <div class="campo"><label for="descripcion">%s</label><textarea id="descripcion" maxlength="2000" required></textarea>'
                  '<span class="ayuda">%s</span></div>\n' % (
                      texto("Description", "Descripción"),
                      texto("What would you change or add, and why? Please do not write your email address here.",
                            "¿Qué cambiarías o añadirías, y por qué? Por favor, no escribas aquí tu correo electrónico.")))

    partes.append('    <div class="campo"><label for="categoria">%s</label><select id="categoria" required>\n' % texto("Category", "Categoría"))
    for clave, etiqueta in categorias.items():
        valor = "%s / %s" % (etiqueta["en"], etiqueta["es"])
        partes.append('      <option value="%s" data-en="%s" data-es="%s">%s</option>\n' % (
            html.escape(valor, quote=True), html.escape(etiqueta["en"], quote=True), html.escape(etiqueta["es"], quote=True), html.escape(etiqueta["en"])))
    partes.append("    </select></div>\n")

    partes.append('    <div class="campo"><span class="rotulo">%s</span><div class="opciones">\n' % texto("How do you want to appear?", "¿Cómo quieres que figure?"))
    partes.append('      <label><input type="radio" name="figura" value="%s" required> %s</label>\n' % (
        html.escape(OPCION_NOMBRE, quote=True), texto("With my name", "Con mi nombre")))
    partes.append('      <label><input type="radio" name="figura" value="%s"> %s</label>\n' % (
        html.escape(OPCION_ALIAS, quote=True), texto("With my forum or Discord alias", "Con mi alias del foro o de Discord")))
    partes.append('      <label><input type="radio" name="figura" value="%s" checked> %s</label>\n' % (
        html.escape(OPCION_ANONIMO, quote=True), texto("Anonymous", "Anónimo")))
    partes.append("    </div></div>\n")

    partes.append('    <div class="campo" id="campo-nombre" hidden><label for="nombre">%s</label><input type="text" id="nombre" maxlength="60">'
                  '<span class="ayuda">%s</span></div>\n' % (
                      texto("Name or alias", "Nombre o alias"),
                      texto("Only shown if you did not choose anonymous.", "Solo se muestra si no has elegido anónimo.")))

    partes.append('    <div class="campo"><label for="apoyo">%s</label><select id="apoyo">\n' % texto("Do you support a proposal that is already on the list?", "¿Apoyas alguna propuesta que ya esté en la lista?"))
    partes.append('      <option value="" data-en="No: this is a new idea" data-es="No: es una idea nueva">No: this is a new idea</option>\n')
    partes.append('      <option value="not sure" data-en="I am not sure whether mine is already there" data-es="No estoy seguro de si la mía ya está">I am not sure whether mine is already there</option>\n')
    for propuesta in propuestas:
        if not propuesta.get("apoyable", True):
            continue        # p. ej. la propia lista de propuestas: no tiene sentido apoyarla
        valor = "%d - %s" % (propuesta["numero"], propuesta["titulo"]["en"])
        partes.append('      <option value="%s" data-en="%s" data-es="%s">%s</option>\n' % (
            html.escape(valor, quote=True),
            html.escape("No. %d · %s" % (propuesta["numero"], propuesta["titulo"]["en"]), quote=True),
            html.escape("N.º %d · %s" % (propuesta["numero"], propuesta["titulo"]["es"]), quote=True),
            html.escape("No. %d · %s" % (propuesta["numero"], propuesta["titulo"]["en"]))))
    partes.append("    </select></div>\n")

    partes.append('    <div class="trampa" aria-hidden="true"><label for="sitio_web">Website</label><input type="text" id="sitio_web" tabindex="-1" autocomplete="off"></div>\n')
    partes.append('    <button class="boton-enviar" type="submit">%s</button>\n' % texto("Send proposal", "Enviar propuesta"))
    partes.append("  </form>\n")

    partes.append('  <div class="mensaje" id="mensaje-exito" hidden>%s</div>\n' % bloque(
        "Thank you! Your proposal has been received. It will be reviewed by hand and added to the list if it is new.",
        "¡Gracias! Tu propuesta ha llegado. Se revisará a mano y se añadirá a la lista si es nueva."))
    partes.append('  <div class="mensaje error" id="mensaje-error" hidden>%s</div>\n' % bloque(
        "Something went wrong. Please check the required fields and try again in a minute.",
        "Algo ha fallado. Revisa los campos obligatorios y vuelve a intentarlo dentro de un minuto."))

    partes.append('  <div class="mensaje error" id="mensaje-espera" hidden>%s</div>\n' % bloque(
        "Please wait a moment: to avoid spam, the form accepts one proposal per minute and not in the first seconds after the page loads. Try again shortly.",
        "Espera un momento: para evitar el spam, el formulario admite una propuesta por minuto y no en los primeros segundos tras cargar la página. Inténtalo de nuevo enseguida."))

    partes.append('  <p class="privacidad">%s</p>\n' % bloque(
        "What is stored: your title, description, category and the name or alias you choose to give. We do not ask for your email. Answers go to a private sheet read only by the author; the public list never shows names unless you chose to appear. To have a proposal removed, ask the author.",
        "Qué se guarda: tu título, la descripción, la categoría y el nombre o alias que decidas dar. No pedimos tu correo. Las respuestas van a una hoja privada que solo lee el autor; la lista pública no enseña nombres salvo que hayas elegido figurar. Para retirar una propuesta, pídeselo al autor."))

    configuracion_cliente = None
    if configuracion:
        configuracion_cliente = {"accion": configuracion["accion"], "entradas": configuracion["entradas"],
                                 "opcion_anonimo": OPCION_ANONIMO}
    configuracion_json = json.dumps(configuracion_cliente, ensure_ascii=False).replace("</", "<\\/")
    extra = '<script>window.GPW_FORM = %s;</script>\n<script src="assets/form.js"></script>' % configuracion_json
    partes.append(pie_pagina(extra))
    return "".join(partes)


def bloque_html(ingles, espanol):
    """Como bloque(), pero el texto ya es HTML de confianza (lleva enlaces propios); no se escapa."""
    return '<span class="i18n-en bloque">%s</span><span class="i18n-es bloque">%s</span>' % (ingles, espanol)


def texto_html(ingles, espanol):
    return '<span class="i18n-en">%s</span><span class="i18n-es">%s</span>' % (ingles, espanol)


def cargar_datos_mod():
    with open(RUTA_MOD, encoding="utf-8") as fichero:
        return json.load(fichero)


# Piezas gráficas: réplicas en HTML y SVG, no capturas. Los datos son de ejemplo.
FILAS_TABLERO = [
    # posición, piloto, gap, int, neumático (D seco, I intermedio, W lluvia)
    ("1", "M. Hakkinen", "", "", "D"),
    ("2", "D. Coulthard", "+4.812", "4.812", "D"),
    ("3", "M. Schumacher", "+11.340", "6.528", "D"),
    ("4", "E. Irvine", "+19.077", "7.737", "D"),
    ("5", "J. Villeneuve", "+26.351", "7.274", "I"),
    ("6", "H. Frentzen", "+31.905", "5.554", "I"),
    ("7", "G. Fisichella", "+49.220", "17.315", "D"),
    ("8", "A. Wurz", "+1L", "9.804", "D"),
]
FILAS_PARADAS = [
    ("M. Hakkinen", "L22", "27.6s", "L48", "26.9s", "", ""),
    ("D. Coulthard", "L21", "28.1s", "L47", "27.3s", "", ""),
    ("M. Schumacher", "L18", "26.4s", "L38", "27.0s", "L55", "26.8s"),
    ("E. Irvine", "L23", "29.5s", "", "", "", ""),
]


def tablero_html():
    filas = []
    for posicion, piloto, hueco, intervalo, neumatico in FILAS_TABLERO:
        filas.append('<tr><td class="c-pos">%s</td><td class="c-piloto">%s</td><td class="c-num">%s</td><td class="c-num">%s</td>'
                     '<td class="c-ty ty-%s">%s</td></tr>' % (posicion, piloto, hueco or "&ndash;", intervalo or "&ndash;", neumatico, neumatico))
    paradas = []
    for piloto, v1, t1, v2, t2, v3, t3 in FILAS_PARADAS:
        celdas = ""
        for vuelta, tiempo in ((v1, t1), (v2, t2), (v3, t3)):
            celdas += '<td class="c-num">%s</td>' % (("%s&nbsp;&nbsp;%s" % (vuelta, tiempo)) if vuelta else "&ndash;")
        paradas.append('<tr><td class="c-piloto">%s</td>%s</tr>' % (piloto, celdas))
    return """
    <figure class="tablero" aria-labelledby="pie-tablero">
      <div class="tablero-paneles">
        <table class="panel-juego" aria-label="Race Order">
          <caption>Race Order</caption>
          <thead><tr><th scope="col">Pos</th><th scope="col">Driver</th><th scope="col">Gap</th><th scope="col">Int</th><th scope="col">Ty</th></tr></thead>
          <tbody>%(filas)s</tbody>
        </table>
        <table class="panel-juego" aria-label="Pit Stops">
          <caption>Pit Stops</caption>
          <thead><tr><th scope="col">Driver</th><th scope="col">Pit 1</th><th scope="col">Pit 2</th><th scope="col">Pit 3</th></tr></thead>
          <tbody>%(paradas)s</tbody>
        </table>
      </div>
      <figcaption id="pie-tablero">%(pie)s</figcaption>
    </figure>
""" % {"filas": "".join(filas), "paradas": "".join(paradas),
       "pie": texto("Race Order with the new Gap, Int and tyre (Ty) columns, and the Pit Stops panel. Recreated in HTML with example data; not a screenshot.",
                    "Race Order con las columnas nuevas Gap, Int y neumático (Ty), y el panel Pit Stops. Recreado en HTML con datos de ejemplo; no es una captura.")}


def mapa_svg():
    return """
    <figure class="mapa">
      <svg viewBox="0 0 420 230" role="img" aria-labelledby="mapa-t mapa-d">
        <title id="mapa-t">Safety Car on the circuit map</title>
        <desc id="mapa-d">A schematic circuit with a pit lane along the bottom straight. Six car circles are bunched behind a larger grey circle marked SC.</desc>
        <path class="m-pista" d="M60 170 L60 70 Q60 38 92 38 L214 38 Q246 38 252 62 Q258 84 286 88 L336 94 Q372 98 372 130 Q372 170 336 170 Z"/>
        <path class="m-boxes" d="M96 192 L330 192"/>
        <path class="m-enlace" d="M72 170 L96 192 M318 192 L336 170"/>
        <circle class="m-coche" cx="132" cy="38" r="7"/><circle class="m-coche" cx="152" cy="38" r="7"/>
        <circle class="m-coche" cx="172" cy="38" r="7"/><circle class="m-coche" cx="192" cy="38" r="7"/>
        <circle class="m-coche" cx="212" cy="38" r="7"/><circle class="m-coche" cx="232" cy="41" r="7"/>
        <circle class="m-sc" cx="262" cy="70" r="11"/>
        <text class="m-sc-txt" x="262" y="73.5" text-anchor="middle">SC</text>
        <text class="m-etiqueta" x="96" y="214">pit lane</text>
      </svg>
      <figcaption>%s</figcaption>
    </figure>
""" % texto("While the Safety Car is out the field bunches up behind it. It waits in the pit lane before it comes out. Schematic: not a real circuit.",
            "Con el Safety Car en pista, el pelotón se junta detrás. Espera en el carril de boxes antes de salir. Esquema: no es un circuito real.")


CAMBIOS = [
    ("Safety Car", "Safety Car",
     "It did not exist. A car stopped on the track changed nothing for the rest of the field.",
     "No existía. Un coche parado en pista no cambiaba nada para el resto.",
     "A ghost car leads the field, everyone bunches up behind it, and nobody overtakes. The AI reacts: it pits, saves fuel, changes worn tyres, or stays out.",
     "Un coche fantasma lidera al pelotón, todos se juntan detrás y nadie adelanta. La IA reacciona: entra a boxes, ahorra combustible, cambia neumáticos gastados o se queda fuera."),
    ("The AI's race", "La carrera de la IA",
     "Pit plans were drawn at random: some stints were absurdly short, and every car left the grid with the same fuel.",
     "Los planes de parada eran aleatorios: había tandas absurdamente cortas y todos los coches salían con el mismo combustible.",
     "Plans depend on the tyre, fuel is loaded for the stint ahead, no stint is shorter than a fixed share of the race, and a change in the weather makes the AI think instead of panic.",
     "Los planes dependen del neumático, el combustible se carga para la tanda siguiente, ninguna tanda baja de una parte fija de la carrera y un cambio de tiempo hace pensar a la IA en lugar de entrar en pánico."),
    ("The pit lane", "El carril de boxes",
     "Cars could leave in the wrong order, and they were not visible on the map while they were in there.",
     "Los coches podían salir en el orden equivocado y no se veían en el mapa mientras estaban dentro.",
     "The order is respected, the lane is drawn on all 16 circuit maps and the cars move along it.",
     "Se respeta el orden, el carril está dibujado en los 16 mapas de circuito y los coches avanzan por él."),
    ("Screens", "Pantallas",
     "A race order without gaps, a Pit Stops panel with only the number of stops, and a speed selector from 50% to 150%.",
     "Un orden de carrera sin diferencias, un panel Pit Stops con solo el número de paradas y un selector de velocidad de 50 % a 150 %.",
     "Race Order shows Gap, Int and the tyre of every car. Pit Stops lists the lap and duration of each stop. The speed selector goes from 100% to 600%.",
     "Race Order muestra Gap, Int y el neumático de cada coche. Pit Stops enseña la vuelta y la duración de cada parada. El selector de velocidad va de 100 % a 600 %."),
    ("The paddock", "El paddock",
     "Every contract expired on the same day, and nobody lost a seat during the season.",
     "Todos los contratos vencían el mismo día y nadie perdía el puesto durante la temporada.",
     "Contracts are staggered, free drivers lower their demands as the season runs out, and a driver who is not delivering can lose the seat to a better one.",
     "Los contratos se escalonan, los pilotos libres rebajan sus exigencias al acabar la temporada y quien no rinde puede perder el asiento ante otro mejor."),
    ("1998", "1998",
     "A generic season.",
     "Una temporada genérica.",
     "1998 drivers, teams, sponsors, engines, chiefs and test drivers, 16 circuits with adjusted data, and the names in the game text to match.",
     "Pilotos, equipos, patrocinadores, motores, jefes y probadores de 1998, 16 circuitos con datos ajustados y los nombres del texto del juego en consonancia."),
    ("News and audio", "Noticias y audio",
     "One wording per event.",
     "Una sola redacción por evento.",
     "Many events have several wordings, with their headlines, and the new ones (Safety Car, penalties, the two-hour limit, strategy) have their own. New Race Control audio.",
     "Muchos eventos tienen varias redacciones con sus titulares, y los nuevos (Safety Car, sanciones, el límite de dos horas, estrategia) tienen los suyos. Audio nuevo de Dirección de Carrera."),
]


def generar_mod(datos_mod):
    m = datos_mod
    partes = [cabecera_pagina("Download", "Descarga", "Download", "Descarga", "index.html", "Proposals", "Propuestas",
                              clase_body="pagina-mod", enlace_descarga=False)]
    # Raíl izquierdo: ficha técnica e índice
    partes.append('  <aside class="mod-rail">\n    <dl class="ficha">\n')
    for rotulo_en, rotulo_es, valor in (
            ("Version", "Versión", texto_html(m["version"] + " &middot; " + m["estado"], m["version"] + " &middot; " + m["estado_es"])),
            ("Date", "Fecha", texto_html(m["fecha_en"], m["fecha_es"])),
            ("Size", "Tamaño", html.escape(m["tamano"])),
            ("Files", "Ficheros", str(m["entradas"])),
            ("Needs", "Requiere", texto_html("the original game", "el juego original"))):
        partes.append('      <div><dt>%s</dt><dd>%s</dd></div>\n' % (texto(rotulo_en, rotulo_es), valor))
    partes.append('    </dl>\n    <nav class="indice" aria-label="%s"><ol>\n' % html.escape("Contents / Contenido"))
    for ancla, en, es in (("descarga", "Download", "Descarga"), ("cambios", "What changes", "Qué cambia"), ("instalar", "Install", "Instalar"),
                          ("antes", "Before you play", "Antes de jugar"), ("creditos", "Credits and contact", "Créditos y contacto")):
        partes.append('      <li><a href="#%s">%s</a></li>\n' % (ancla, texto(en, es)))
    partes.append("    </ol></nav>\n  </aside>\n")

    partes.append('  <div class="mod-cuerpo">\n')
    # Cabecera de la página
    partes.append('    <header class="mod-titulo">\n      <h1>GPW Evolution &rsquo;98</h1>\n')
    partes.append('      <p class="entradilla">%s</p>\n' % bloque(
        "A mod for Grand Prix World that adds a Safety Car, makes the AI plan a race with some sense, and sets the game in the 1998 season. It keeps what makes GPW feel like GPW.",
        "Un mod para Grand Prix World que añade un Safety Car, hace que la IA planifique la carrera con algo de sentido y sitúa el juego en la temporada 1998. Conserva lo que hace que GPW se sienta como GPW."))
    partes.append('      <p class="estado-mod"><span class="marca-estado">%s</span> %s</p>\n    </header>\n' % (
        texto("Pre-release", "Pre-lanzamiento"),
        texto("Version 0.1. Most of it has been through real races, but expect rough edges.",
              "Versión 0.1. La mayor parte ha pasado por carreras reales, pero habrá aristas.")))

    # 01 Descarga
    partes.append('    <section id="descarga">\n      <h2><span class="num">01</span> %s</h2>\n' % texto("Download", "Descarga"))
    partes.append("""      <div class="descarga">
        <a class="descarga-nombre" href="%(url)s">%(fichero)s</a>
        <span class="descarga-meta">%(tamano)s</span>
        <a class="boton-descarga" href="%(url)s">%(boton)s</a>
      </div>
      <p class="huella"><span class="rotulo-huella">SHA-256</span> <code id="huella-valor">%(sha)s</code>
        <button type="button" class="copiar" data-copiar="huella-valor" data-ok="%(copiado)s">%(copiar)s</button></p>
""" % {"url": html.escape(m["url_descarga"]), "fichero": html.escape(m["fichero"]), "tamano": html.escape(m["tamano"]),
       "boton": texto("Download", "Descargar"), "sha": html.escape(m["sha256"]),
       "copiar": texto("copy", "copiar"), "copiado": html.escape("copied / copiado")})
    partes.append('      <ul class="recursos">\n')
    partes.append('        <li><a href="%s">%s</a> %s</li>\n' % (html.escape(m["readme"]), "README_EVOLUTION_98.txt", texto("every change, what it was and what it is now", "cada cambio, cómo era y cómo es ahora")))
    partes.append('        <li><a href="%s">%s</a> %s</li>\n' % (html.escape(m["creditos"]), "CREDITS.txt", texto("credits and licences", "créditos y licencias")))
    partes.append('        <li><a href="%s">%s</a> %s</li>\n' % (html.escape(m["perfil_dxwnd"]), "GPW_Evolution_98.dxw", texto("DxWnd profile (also inside the zip)", "perfil de DxWnd (también dentro del zip)")))
    partes.append('        <li><a href="%s">%s</a></li>\n      </ul>\n    </section>\n' % (html.escape(m["url_release"]), texto("Release page on GitHub", "Página de la release en GitHub")))

    # Tablero y mapa
    partes.append(tablero_html())

    # 02 Qué cambia
    partes.append('    <section id="cambios">\n      <h2><span class="num">02</span> %s</h2>\n' % texto("What changes", "Qué cambia"))
    partes.append('      <p>%s</p>\n' % texto_html(
        "The short version, area by area. The README lists all 65 changes in the same form: what the original did, and what this does now.",
        "La versión corta, por áreas. El README lista los 65 cambios con la misma forma: qué hacía el original y qué hace ahora."))
    partes.append(mapa_svg())
    partes.append('      <div class="libro">\n')
    for tema_en, tema_es, antes_en, antes_es, ahora_en, ahora_es in CAMBIOS:
        partes.append('        <article class="cambio">\n          <h3>%s</h3>\n' % texto(tema_en, tema_es))
        partes.append('          <p class="antes"><span class="rotulo">%s</span> %s</p>\n' % (texto("Was", "Antes"), texto(antes_en, antes_es)))
        partes.append('          <p class="ahora"><span class="rotulo">%s</span> %s</p>\n        </article>\n' % (texto("Now", "Ahora"), texto(ahora_en, ahora_es)))
    partes.append("      </div>\n    </section>\n")

    # 03 Instalar
    partes.append('    <section id="instalar">\n      <h2><span class="num">03</span> %s</h2>\n' % texto("Install", "Instalar"))
    partes.append('      <ol class="pasos">\n')
    for en, es in (
            ("Install the original game into a new folder. Do not reuse an install that already has other mods. You do not need the 1.01 or 1.03 patches.",
             "Instala el juego original en una carpeta nueva. No reutilices una instalación que ya tenga otros mods. No hacen falta los parches 1.01 ni 1.03."),
            ("Extract the zip into that folder and accept every overwrite.",
             "Extrae el zip en esa carpeta y acepta todas las sobrescrituras."),
            ("Start gpw.exe, or the launcher you normally use.",
             "Arranca gpw.exe, o el lanzador que uses normalmente."),
            ("Start a new career. Saved games from other versions are not guaranteed to work.",
             "Empieza una carrera nueva. No se garantiza que valgan las partidas guardadas de otras versiones.")):
        partes.append("        <li>%s</li>\n" % texto(en, es))
    partes.append("      </ol>\n")
    partes.append('      <p>%s</p>\n' % texto_html(
        'GPW does not run well on modern Windows by itself. I use <a href="%(dxwnd)s">DxWnd</a> in windowed mode: download it yourself (the latest build there, at the time of writing v2.06.16) and import the profile <a href="%(perfil)s">GPW_Evolution_98.dxw</a>, then right-click the entry, choose Modify and set the path to your gpw.exe. The path must not contain blank spaces. dgVoodoo2 also works as a DirectDraw wrapper.' % {"dxwnd": html.escape(m["url_dxwnd"]), "perfil": html.escape(m["perfil_dxwnd"])},
        'GPW no funciona bien por sí solo en Windows modernos. Yo uso <a href="%(dxwnd)s">DxWnd</a> en ventana: descárgalo tú (la última compilación de esa página, en el momento de escribir esto la v2.06.16) e importa el perfil <a href="%(perfil)s">GPW_Evolution_98.dxw</a>; luego clic derecho en la entrada, Modificar y pon la ruta de tu gpw.exe. La ruta no puede llevar espacios. dgVoodoo2 también sirve como envoltorio de DirectDraw.' % {"dxwnd": html.escape(m["url_dxwnd"]), "perfil": html.escape(m["perfil_dxwnd"])}))
    partes.append('      <p>%s</p>\n    </section>\n' % texto(
        "To go back to the original, delete the folder and install the game again. The pack never touches anything outside the game folder.",
        "Para volver al original, borra la carpeta e instala el juego de nuevo. El paquete no toca nada fuera de la carpeta del juego."))

    # 04 Antes de jugar
    partes.append('    <section id="antes">\n      <h2><span class="num">04</span> %s</h2>\n      <ul class="avisos">\n' % texto("Before you play", "Antes de jugar"))
    for en, es in (
            ("This is a pre-release. The Safety Car, the AI under it and the pit lane have been through several real races. The market changes, the new qualifying runs and the penalty process have been checked on a test bench, but not in many races.",
             "Es un pre-lanzamiento. El Safety Car, la IA bajo él y el carril de boxes han pasado por varias carreras reales. Los cambios del mercado, las nuevas tandas de clasificación y el proceso de sanciones se han comprobado en banco de pruebas, pero en pocas carreras."),
            ("Only the English texts are included. French and German are not up to date, so those languages keep the original game's texts.",
             "Solo van los textos en inglés. El francés y el alemán no están al día, así que esos idiomas conservan los textos del juego original."),
            ("The new audio was generated with a text-to-speech model licensed for non-commercial use only. Do not sell the pack or use it in anything commercial.",
             "El audio nuevo se generó con un modelo de voz de uso solo no comercial. No vendas el paquete ni lo uses en nada comercial."),
            ("The sound code leaks Windows event handles in very long sessions. Saving and restarting the game clears it.",
             "El código de sonido pierde manejadores de eventos de Windows en sesiones muy largas. Guardar y reiniciar el juego lo limpia."),
            ("The internal values (probabilities, times, weights) will change between versions. Do not rely on numbers copied from an older one.",
             "Los valores internos (probabilidades, tiempos, pesos) cambiarán entre versiones. No te fíes de cifras copiadas de una anterior.")):
        partes.append("        <li>%s</li>\n" % texto(en, es))
    partes.append("      </ul>\n    </section>\n")

    # 05 Créditos y contacto
    partes.append('    <section id="creditos">\n      <h2><span class="num">05</span> %s</h2>\n' % texto("Credits and contact", "Créditos y contacto"))
    partes.append('      <p>%s</p>\n' % texto_html(
        'Unofficial fan modification of Grand Prix World, developed by Edward Grabowski Communications Limited for MicroProse. The 1998 graphics come from Simul810&rsquo;s 1998 mod, used with permission. The executable builds on Veedub&rsquo;s 1.03 patch and on my own unreleased base, edited with GPWEdit. Full credits and licences in <a href="%s">CREDITS.txt</a>.' % html.escape(m["creditos"]),
        'Modificación no oficial de Grand Prix World, desarrollado por Edward Grabowski Communications Limited para MicroProse. Los gráficos de 1998 vienen del mod 1998 de Simul810, usados con permiso. El ejecutable se apoya en el parche 1.03 de Veedub y en mi propia base sin publicar, editada con GPWEdit. Créditos y licencias completos en <a href="%s">CREDITS.txt</a>.' % html.escape(m["creditos"])))
    partes.append('      <p>%s</p>\n' % texto("Bugs, ideas and missing credits are welcome.", "Los fallos, las ideas y los créditos que falten son bienvenidos."))
    partes.append('      <dl class="contacto">\n')
    for rotulo, enlace in m["contacto"]:
        partes.append('        <div><dt>%s</dt><dd>%s</dd></div>\n' % (html.escape(rotulo), enlace))
    partes.append("      </dl>\n    </section>\n  </div>\n")
    partes.append(pie_pagina())
    return "".join(partes)


def copiar_descargas():
    """Copia a descargas/ lo que la página enlaza: README, CREDITS y perfil de DxWnd del paquete."""
    destino = os.path.join(CARPETA_SALIDA, "descargas")
    os.makedirs(destino, exist_ok=True)
    for nombre in ("README_EVOLUTION_98.txt", "CREDITS.txt", "GPW_Evolution_98.dxw"):
        origen = os.path.join(CARPETA_PAQUETE, nombre)
        if os.path.exists(origen):
            shutil.copyfile(origen, os.path.join(destino, nombre))


def copiar_assets():
    destino = os.path.join(CARPETA_SALIDA, "assets")
    if os.path.exists(destino):
        shutil.rmtree(destino)
    shutil.copytree(os.path.join(CARPETA_SITIO, "assets"), destino)


def main():
    datos = cargar_lista()
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    apoyos = contar_apoyos()
    with open(os.path.join(CARPETA_SALIDA, "index.html"), "w", encoding="utf-8", newline="\n") as fichero:
        fichero.write(generar_lista(datos, apoyos))
    with open(os.path.join(CARPETA_SALIDA, "propose.html"), "w", encoding="utf-8", newline="\n") as fichero:
        fichero.write(generar_formulario(datos))
    with open(os.path.join(CARPETA_SALIDA, "mod.html"), "w", encoding="utf-8", newline="\n") as fichero:
        fichero.write(generar_mod(cargar_datos_mod()))
    copiar_assets()
    copiar_descargas()
    print("Generadas index.html, propose.html y mod.html con %d propuestas en %s" % (len(datos["propuestas"]), CARPETA_SALIDA))


main()
