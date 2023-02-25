# -*- coding: utf-8 -*-

__title__ = "Información"
__autor__ = "César Sala Gago"
__doc__ = """Infomación"""


#---------------IMPORTACIONES----------------

import clr
import webbrowser
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import (FilteredWorksetCollector, WorksetKind, ElementWorksetFilter,FilteredElementCollector, ElementId, View)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager



import System
from System.Collections.Generic import List

from pyrevit import script


#------------------VARIABLES------------------
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

output = script.get_output()
#-----------------FUNCIONES-------------------

print("Autor: César Sala Gago")

print("Fecha de la última versión: 25/02/2023")

output.print_html('Visita mi <a href="https://www.linkedin.com/in/c%C3%A9sar-sala-gago-84837936/">LinkedIn</a>')
output.print_html('Visita mi <a href="https://github.com/CesarSala92">GitHub</a>')