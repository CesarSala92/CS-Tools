# -*- coding: utf-8 -*-

__title__ = "Desbloquear vínculos"
__autor__ = "César Sala Gago"
__doc__ = """Desbloquea todos los vínculos del proyecto."""
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
tran = Autodesk.Revit.DB.Transaction(doc,"do")




def vinculos_desbloqueador():
    contador = 0
    vinculos = list(FilteredElementCollector(doc).OfClass(RevitLinkInstance))
    
    if bool(vinculos):
        
        for vinculo in vinculos:
            tran.Start()
            Element.Pinned.SetValue(vinculo, False)
            tran.Commit()

        forms.alert("Se han desbloqueado los vínculos", exitscript=False) 
    else:
        forms.alert("No hay vinculos en el modelo", exitscript=True) 


vinculos_desbloqueador()