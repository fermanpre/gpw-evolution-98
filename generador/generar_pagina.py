# Genera la página pública de propuestas del minimod de GPW (lista + formulario), bilingüe (ENG por defecto y ESP), a partir de lista.json.
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


def cabecera_pagina(titulo_ingles, titulo_espanol, miga_ingles, miga_espanol, enlace_accion, texto_accion_ingles, texto_accion_espanol):
    return """<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="Community proposals for GPW Evolution '98, a Grand Prix World 1998 mod.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="sitio">
  <div>
    <div class="marca"><a href="index.html">GPW Evolution '98</a></div>
    <div class="migas">%(miga)s</div>
  </div>
  <div class="acciones">
    <a class="boton-accion" href="%(enlace_accion)s">%(texto_accion)s</a>
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
    copiar_assets()
    print("Generadas index.html y propose.html con %d propuestas en %s" % (len(datos["propuestas"]), CARPETA_SALIDA))


main()
