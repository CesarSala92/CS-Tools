# -*- coding: utf-8 -*-

__title__ = "Visibilidad \nSubproyectos"
__autor__ = "César Sala Gago"
__doc__ = """Aisla temporalmente los subproyectos seleccionados.

Autor: César Sala Gago
Versión: 01
Fecha: 21/02/2023"""


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


#--------------------UI---------------------

ops = (FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets())
dict_ops = {view.Name: view for view in ops}
res = forms.SelectFromList.show(sorted(dict_ops),
                                title = "Subproyectos",
                                multiselect= True,
                                #name_attr='Id',
                                button_name='Seleccionar Subproyectos')

if not res:
    forms.alert('No se ha seleccionado ningun subproyecto', exitscript=True)

#--------------------CODIGO---------------------

coleccion = (FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets())
id_worksets = []
for i in res:
    for v in ops:
        if i in v.Name:
            id_worksets.append(v.Id)

for elemento in ops:
    tran.Start()
    if elemento.Id in id_worksets:
        doc.ActiveView.SetWorksetVisibility(elemento.Id, WorksetVisibility.Visible)
        tran.Commit() 
    else:
        doc.ActiveView.SetWorksetVisibility(elemento.Id, WorksetVisibility.Hidden)
        tran.Commit() 