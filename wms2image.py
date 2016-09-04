# !/usr/bin/python  
# -*- coding: utf-8 -*- 

__author__ = [
    'Patricio Soriano Castro <pasoriano@gmail.com>'
]
__license__ = 'GPLv3'

"""Example Google style docstrings.

Descripción
===========
El script genera un fichero GML de parcela catastral según las especificaciones de Castastro.
Basado en https://github.com/sigdeletras/dxf2gmlcatastro (Patricio Soriano :: SIGdeletras.com)

Especificaciones
================
    * http://www.catastro.minhap.gob.es/esp/formatos_intercambio.asp
    * Cada parcela debe estar en una capa en cuyo nombre se establecerá su referencia.
    * No se permiten incorporar en el mismo fichero dxf parcelas con referencias catastrales y referencias locales mezcladas, todas deben ser del mismo tipo, o bien locales o bien catastrales.
    * Se asume referencia catastral si la longitud de la referencia es de 14 caracteres.
    * Las geometrías deben ser sólidas y estar cerradas (el primer y último punto del polígono deben ser el mismo)
Requisitos
==========
Es necesario tener instalado Python y el módulo GDAL (python-gdal).

Ejemplos de uso
===============
    * python dxfgmlcatastro.py <parcela1.dxf>
         generará el fichero parcela1.gml
    * python dxfgmlcatastro.py <parcela1.dxf> 25831
         generará el fichero parcela1.gml usando el código EPSG 25831
    * python dxfgmlcatastro.py <mi_directorio>
         generará un fichero .gml por cada fichero .dxf que se encuentre en mi_directorio

"""

import ast
import csv
import os
import sys
import requests

try:
    import requests
except ImportError:
    print('Error: requests no instalado')
    sys.exit(1)

# Sistemas de referencia de coordenadas
EPSG_ZONES = [
    '25828',  # ETRS89 / UTM zone 28N
    '25829',  # ETRS89 / UTM zone 29N
    '25830',  # ETRS89 / UTM zone 30N
    '25831',  # ETRS89 / UTM zone 31N
    '23028',  # ED50 / UTM zone 28N
    '23029',  # ED50 / UTM zone 29N
    '23030',  # ED50 / UTM zone 30N
    '23031',  # ED50 / UTM zone 31N
]


# Formatos de imágen
IMAGE_FORMAT = [
    'png',  
    'jpeg',  
    'tiff',  
    'gif',  
]


def wms2image(csvfile, code, bbox, imgwidth, imgformat):
    """
    Obtiene un conjunto de imágenes (Getmap) de un listado de servicios
    WMS de un rectángulo geográfico definido mediante par de coordendas
    en un EPSG UTM.
    csvfile: Archivo en formato CSV con el listado de servicios WMS
    code: Sistema de Referencia de Coordenadas del DXF (código EPSG)
    bbox: Par de coordendas del área geográfica
    imgwidth: Ancho de la imagen
    imgformat: Formato de la imagen
    """
    if code not in EPSG_ZONES:
        return (
            False,
            u'Error: El código EPSG "%s" es incorrecto' % code
        )
        sys.exit(1)        
    
    if imgformat not in IMAGE_FORMAT:
        return (
            False,
            u'Error: El formato "%s" es incorrecto' % imgformat
        )
        sys.exit(1)    

    wmslist = csv.reader(open(csvfile, "rt"), delimiter=',')

    bboxcoord = ast.literal_eval(bbox)
    imgheight = ((bboxcoord[3] - bboxcoord[1]) * int(imgwidth)) / (bboxcoord[2] - bboxcoord[0])

    for row in wmslist:
        wms = row[0]
        layer = row[1]
        file = row[2]
        url = wms + '?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=' + layer + '&STYLES=&SRS=EPSG:' + str(code) + '&BBOX=' \
              + bbox + '&WIDTH=' + str(imgwidth) + '&HEIGHT=' + str(imgheight) + '&FORMAT=image/' + imgformat

        r = requests.get(url)
        with open(file + "." + imgformat, "wb") as code:
            code.write(r.content)

        print("Downloading..." + file + "." + imgformat)


def usage():
    print(u'\nParámetros:')

    print(u'\t1. csvfile: nombre del archivo csv con el listado de servicios WMS')
    print(u'\t2. code: Código EPGS del Sistema de referencia de coordenadas. Solo UTM.')
    print(u'\t3. bbox: Pares de coordenadas de las esquinas de área. Solo UTM')
    print(u'\t4. imgwidth: Ancho de la imagen')
    print(u'\t5. imgformat: Formato de la imagen')

    print(u'\nEjemplos de uso:')

    print(u'\tObtiene un conjunto de imágenes en formato png del listado pnoa.csv:\n')
    
    print(u'\t$ python wms2image.py pnoa.csv 800 25830 "332401,4188300,341225,4193019" png')


def main():
    if len(sys.argv) < 6:
        print(u'Error: parámetros insuficientes')
        usage()
        sys.exit(1)
    
    csvfile = sys.argv[1]
    code = sys.argv[2]
    bbox = sys.argv[3]
    imgwidth = sys.argv[4]
    imgformat = sys.argv[5]

    if sys.argv[2] not in EPSG_ZONES:
        return (
            False,
            print(u'Error: El código EPSG "%s" es incorrecto' % sys.argv[2])
        )
        sys.exit(1)        
    
    if sys.argv[5] not in IMAGE_FORMAT:
        return (
            False,
            print(u'Error: El formato "%s" es incorrecto' % sys.argv[5])
        )
        sys.exit(1)

    wms2image(csvfile, code, bbox, imgwidth, imgformat)

if __name__ == '__main__':
    main()
