# wms2image

Script de Python para obtener imágenes de un listado de servicios de visualización de mapas (WMS)

Más información en la entrada de SIGdeletras http://sigdeletras.com/

El script esta testeado en Python 3.5.1+. 

## Requisitos
- requests

Ejecutar

    pip install -r requirements.txt


## Uso

    python wms2image.py 800 "332401,4188300,341225,4193019" jpeg

- Debe existir el archivo wmslist.csv en el mismo directorio que el archivo py
- Las coordenadas serán UTM
- EPGS es 25830
- Formatos para la solicitud de getmap solo de tipo imágen.
    + png
    + tiff
    + jpeg
    + png

# Editar archivo wmslist.csv
