# !/usr/bin/python  
# -*- coding: utf-8 -*-   
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py


"""

import ast
import csv
import os
import sys
import requests


def wms2image(imgwidth, bbox, imgformat):
    wmslist = csv.reader(open("wmslist.csv", "rt"), delimiter=',')

    bboxcoord = ast.literal_eval(bbox)
    imgheight = ((bboxcoord[3] - bboxcoord[1]) * int(imgwidth)) / (bboxcoord[2] - bboxcoord[0])

    for row in wmslist:
        wms = row[0]
        layer = row[1]
        file = row[2]
        url = wms + '?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=' + layer + '&STYLES=&SRS=EPSG:25830&BBOX=' \
              + bbox + '&WIDTH=' + str(imgwidth) + '&HEIGHT=' + str(imgheight) + '&FORMAT=image/' + imgformat

        r = requests.get(url)
        with open(file + "." + imgformat, "wb") as code:
            code.write(r.content)

        print("Downloading..." + file + "." + imgformat)

if __name__ == '__main__':
    imgwidth = sys.argv[1]
    bbox = sys.argv[2]
    imgformat = sys.argv[3]

    wms2image(imgwidth, bbox, imgformat)
