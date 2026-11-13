# Genera datos/publico.csv (las respuestas SANEADAS del formulario) a partir de la exportación CSV de la pestaña «Form Responses 1» de la hoja privada, con las mismas reglas que la
# pestaña «publico» de la hoja de Google (formulas_pestana_publico.txt):
#   - columnas: fecha (número de serie de Google), titulo, descripcion, categoria, figura_como, apoya;
#   - figura_como: «anónimo» si la persona eligió «Anonymous / Anónimo» (aunque haya escrito un nombre), «sin nombre» si no hay nombre, y si no el nombre o alias escrito;
#   - se excluyen las filas cargadas a mano («Imported / Importada») y la cabecera duplicada.
# La exportación completa NUNCA se publica: solo el resultado de este script.
# Uso: python generar_publico_csv.py <exportacion.csv> [salida, por defecto datos/publico.csv]
import csv
import datetime
import os
import re
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ENTRADA = sys.argv[1]
SALIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "datos", "publico.csv")
ORIGEN_SERIE_GOOGLE = datetime.datetime(1899, 12, 30)


def numero_de_serie(marca):
    """«10/28/2026 13:32:26» (mes/día/año hora:minuto:segundo) -> número de serie de Google (días desde 30/12/1899, con la fracción de la hora)."""
    momento = datetime.datetime.strptime(marca.strip(), "%m/%d/%Y %H:%M:%S")
    diferencia = momento - ORIGEN_SERIE_GOOGLE
    return "%.5f" % (diferencia.days + diferencia.seconds / 86400.0)


def como_figura(eleccion, nombre):
    if re.search(r"anonym|anónim", eleccion.lower()):
        return "anónimo"
    return nombre.strip() if nombre.strip() else "sin nombre"


def principal():
    filas = list(csv.reader(open(ENTRADA, encoding="utf-8-sig", newline="")))
    resultado = [["fecha", "titulo", "descripcion", "categoria", "figura_como", "apoya"]]
    for fila in filas[1:]:
        fila = fila + [""] * (7 - len(fila))
        marca, titulo, descripcion, categoria, eleccion, nombre, apoyo = fila[:7]
        if not titulo.strip() or re.search(r"imported|how do you want", eleccion.lower()):
            continue
        resultado.append([numero_de_serie(marca), titulo, descripcion, categoria, como_figura(eleccion, nombre), apoyo])
    with open(SALIDA, "w", encoding="utf-8", newline="") as fichero:
        csv.writer(fichero, lineterminator="\n").writerows(resultado)
    print("Escritas %d respuestas en %s" % (len(resultado) - 1, SALIDA))


if __name__ == "__main__":
    principal()
