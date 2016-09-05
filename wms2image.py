# !/usr/bin/python  
# -*- coding: utf-8 -*- 

__author__ = [
    'Patricio Soriano Castro <pasoriano@gmail.com>'
]
__license__ = 'GPLv3'

"""Script Python para descarga de imágenes de un listado de servicios WMS usado GetMap.

Descripción
===========
Script de Python para obtener un conjunto de imágenes (GetMap) de un listado de servicios WMS a partir de un rectángulo geográfico definido mediante par de coordenadas UTM.

Requisitos
==========
Es necesario tener instalado Python y el módulo Requests.
Puede ejecutarse e archivo requirements.txt mediate pip install -r requirements.txt

Ejemplos de uso
===============
    * python wms2image.py wmslist/pnoa.csv 25830 "332401,4188300,341225,4193019" 800 tiff
         descarga las imágenes del listado ponoa.csv en formato tiff del área indicada
    
"""

import os
import sys
import requests
import ast
import csv

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
    epgscode = str(code)
    for row in wmslist:
        wms = row[0]
        layer = row[1]
        file = row[2]
        url = wms + '?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=' + layer + '&STYLES=&SRS=EPSG:' + epgscode + '&BBOX=' \
              + bbox + '&WIDTH=' + str(imgwidth) + '&HEIGHT=' + str(imgheight) + '&FORMAT=image/' + imgformat

        r = requests.get(url)
        with open(file + "." + imgformat, "wb") as code:
            code.write(r.content)

        print("Downloading..." + file + "." + imgformat)
        print(url)


def usage():
    print(u'\nEjemplo:')

    print(u'\tpython wms2image.py wmslist/pnoa.csv 25830 "332401,4188300,341225,4193019" 800 tiff')
   
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
