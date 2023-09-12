# -*- coding: utf-8 -*-

__title__ = "Crear \nSubproyectos"
__autor__ = "César Sala Gago"
__doc__ = """Crea subproyectos a partir de un archivo .txt con los nombres separados por comas.
"""


#---------------IMPORTACIONES----------------
import clr

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import *
from RevitServices.Transactions import *

import System
from System.Collections.Generic import *

from pyrevit import forms

#------------------VARIABLES------------------
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document


#-----------------FUNCIONES-------------------
coleccion = (FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets())
listaColeccion = (sub.Name for sub in coleccion)
listaSubproyectos = list()
if doc.IsWorkshared:
    archivoBase = forms.pick_file(file_ext='txt')

    if archivoBase:
        miArchivo = open(archivoBase, "r")
        archivoLeer = miArchivo.read()
        archivoLista = archivoLeer.split(",")

        for elemento in archivoLista:
            listaSubproyectos.append(str(elemento.replace("\n","")))
        
        with Transaction(doc, __title__) as t:
            t.Start()
            for subproyecto in listaSubproyectos:
                if subproyecto not in listaColeccion:
                    nuevoSubproyecto = Workset.Create(doc, subproyecto)
            t.Commit()

    else:
        res = forms.alert("No se ha seleccionado ningún archivo",
                  ok=True)
else:
    res = forms.alert("El archivo no está compartido",
                  ok=True)