# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:58:45 2021

@author: 2rome
"""

#Función read_file implementada por Hugo Romero
#LEE UN FICHERO DE TEXTO PLANO Y LO DEVUELVE COMO STRING
def read_file(file):
    with open(file, 'r') as reader:
        content = reader.read().splitlines()
        lines = [x.lstrip() for x in content if x != ""]
        return lines