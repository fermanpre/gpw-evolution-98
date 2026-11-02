# Genera el CSV de la lista PÚBLICA de propuestas (sin autores): número, título, descripción corta y estado, a partir de lista.json (la misma fuente que la página web).
# Se publica en el repositorio público (datos/lista_publica.csv) y la pestaña «lista» de la hoja del formulario lo lee con =IMPORTDATA(...), para que quien rellene el
# formulario vea qué propuestas ya existen antes de enviar o apoyar una. Ningún autor ni alias aparece aquí (lista.json no los lleva).
# Uso: python generar_csv_lista.py [ruta_de_salida]
import csv
import json
import os
import re
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(CARPETA, "..", ".."))
RUTA_LISTA = os.path.join(CARPETA, "lista.json")
SALIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "datos", "propuestas", "lista_publica.csv")
CABECERA = ["No. / N.º", "Title / Título", "What it asks / Qué pide", "Status / Estado"]
LONGITUD_MAXIMA = 220


def resumen_corto(texto):
    """Primer párrafo, en una línea, recortado en un límite de palabra."""
    primer_parrafo = texto.strip().split("\n")[0].strip()
    primer_parrafo = re.sub(r"\s+", " ", primer_parrafo)
    if len(primer_parrafo) <= LONGITUD_MAXIMA:
        return primer_parrafo
    recorte = primer_parrafo[:LONGITUD_MAXIMA].rsplit(" ", 1)[0].rstrip(",;:")
    return recorte + "…"


datos = json.loads(open(RUTA_LISTA, encoding="utf-8").read())
estados = datos["estados"]
filas = []
for propuesta in sorted(datos["propuestas"], key=lambda p: p["numero"]):
    titulo = "%s / %s" % (propuesta["titulo"]["en"], propuesta["titulo"]["es"])
    estado = estados[propuesta["estado"]]
    filas.append([propuesta["numero"], titulo, resumen_corto(propuesta["pide"]["en"]), "%s / %s" % (estado["en"], estado["es"])])

with open(SALIDA, "w", encoding="utf-8-sig", newline="") as fichero:
    escritor = csv.writer(fichero)
    escritor.writerow(CABECERA)
    escritor.writerows(filas)
print("Escritas %d filas en %s" % (len(filas), SALIDA))
