# wms2image.py

Script de Python para obtener un conjunto de imágenes (GetMap) de un listado de servicios WMS a partir de un rectángulo geográfico definido mediante par de coordenadas UTM.

La obtención rápida de información geográfica de una determinada área puede tener utilidad a la hora de aportar documentación cartográfica que no requiera estar georreferenciada para documentos, informes o trabajos sobre la evolución geográfica de un determinado lugar.

![http://i.giphy.com/l2SqaIg0lAiLIrMYM.gif](http://i.giphy.com/l2SqaIg0lAiLIrMYM.gif)

Más información en la entrada de SIGdeletras http://sigdeletras.com/

## Versión de Python

El *script* está testeado en Python 3.5.1+.

## Requisitos

Es necesario tener instalada la librería [requests](http://docs.python-requests.org/en/master/).
M    pip install -r requirements.txt

## Instalación

El script está disponible en GitHub. Desde el repositorio puede descargarse el [archivo zip](https://github.com/sigdeletras/wms2image/archive/master.zip) con el script o bien hacer un *git clone*

    git clone https://github.com/sigdeletras/wms2image.git

## Uso

Una vez obtenido el script, se puede usar el intérprete de Python por defecto o el terminal para ejecutar el archivo *wms2image.py* definiendo a continuación los parámetros obligatorios.

Ejemplo:

    python wms2image.py wmslist/wmslist.csv 25830 "332401,4188300,341225,4193019" 800 tiff

    import wms2image
    wms2image.wms2image('wmslist.csv, '25830','332401,4188300,341225,4193019','800','png')


### Parámetros

**Todos los parámetros son obligatorio**

- **csvfile**: Archivo en formato CSV con el listado de servicios WMS
- **code**: Sistema de Referencia de Coordenadas (código EPSG). Las coordenadas serán UTM
    + ETR89 UTM 28 al 31 (25828, 25829, 25830 y 25831)
    + ED50 UTM 28 al 31 (23028, 23029, 23030 y 23031)
- **bbox**: Par de coordenadas del área geográfica. El orden de las coordenadas es minx,miny,maxx,maxy. Las coordenadas serán UTM
- **imgwidth**: Ancho de la imagen. Ej. 800.
- **imgformat**: Formato de la imagen. Formatos para la solicitud de getmap solo de tipo imagen (png, tiff, jpeg, gif). Nota: No todos los WMS soportan todos los formatos.

## Crear nuevo listado de WMS

Para crear un listado de capas de WMS a usar podemos usar cualquier editor de texto. La estructura del archivo es sencilla. Para capa servicio se añadirá una file en el archivo que contenga la url del WMS y a continuación separado por como el nombre de la capa y por último el nombre con el que se guardará el fichero de imagen.

Ej.
'''
http://www.ign.es/wms/pnoa-historico,PNOA2004,2004_pnoa
http://www.ign.es/wms/pnoa-historico,PNOA2005,2005_pnoa
http://www.ign.es/wms/pnoa-historico,PNOA2006,2006_pnoa
http://www.ign.es/wms/pnoa-historico,PNOA2007,2007_pnoa
'''
En la carpeta [wmslist](https://github.com/sigdeletras/wms2image/tree/master/wmslist) pueden encontrarse algunos ejemplos.

Para obtener el listado de capas de un WMS puede consultarse los metadatos del servicio a través de la petición **GetCapabilities**.

Ej. [http://www.ign.es/wms/pnoa-historico?request=GetCapabilities&service=WMS](http://www.ign.es/wms/pnoa-historico?request=GetCapabilities&service=WMS)

## Obtener coordenadas

Por ahora el script sólo puede usarse con sistema de referencia de coordenadas UTM. Esto se debe a que las coordenadas métricas son utilizadas, junto al ancho definido, para calcular la altura de la imagen final

Las coordenadas se deben indicar en el siguiente orden:

- 1º minx,miny (esquina inferior izquierda)
- 2º maxx,maxy (esquina superior derecha)

Podemos obtener de forma rápida la caja de coordendas usando QGIS.

##2do

- Porder usar coordendas no geográficas

##¿Cómo colaborar?

- Usando el script
- Compartiendo en Redes Sociales
- Creando listados de WMS por provincias o municipios
- Indicando mejoras (issues, PR..)