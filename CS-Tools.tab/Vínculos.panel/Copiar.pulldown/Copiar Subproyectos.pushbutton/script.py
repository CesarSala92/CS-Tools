# -*- coding: utf-8 -*-

__title__ = "Copiar Subproyectos"
__autor__ = "César Sala Gago"
__doc__ = """Copia todos los elementos de un subproyecto de un vínculo al archivo actual.

Hay elementos que no se pueden copiar, intentar hacerlo dará error al copiar el subproyecto y paralizará la operación.
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
tran = Autodesk.Revit.DB.Transaction(doc,"do")



#----------------FUNCIONES---------------------

def vinculo_copiar_subproyectos(vinculo, subproyectos, doc = __revit__.ActiveUIDocument.Document):
    documento = vinculo.GetLinkDocument()
    # coleccion = (FilteredWorksetCollector(documento).OfKind(WorksetKind.UserWorkset).ToWorksets())
    salida = []
    for sub in subproyectos:
        filtro = ElementWorksetFilter(sub.Id, False)
        salida.append((FilteredElementCollector(documento).WherePasses(filtro).WhereElementIsNotElementType().ToElements()))
        
    coleccionids = [item for sublist in salida for item in sublist] 


    ids = List[ElementId]() 
    for elemento in coleccionids:
        if elemento.Id is not None:
            ids.Add(elemento.Id)


    tran.Start()
    try:
        nuevos = (doc.GetElement(id) for id in ElementTransformUtils.CopyElements(documento, ids, doc, Transform.Identity, CopyPasteOptions()))
        salida = nuevos
    except:
        forms.alert('El subproyecto contiene elementos que no se pueden copiar', exitscript=False)
    tran.Commit()
    return salida  

#--------------------UI---------------------

# Seleccionar vinculo

vinculos = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
nombresVinculos = [vin.GetLinkDocument().Title for vin in vinculos]



vinculoOpciones = forms.SelectFromList.show(sorted(nombresVinculos),
                                title = "Vinculos",
                                multiselect= False,
                                #name_attr='Id',
                                button_name='Seleccionar Vinculos')

if not vinculoOpciones:
    forms.alert('No se ha seleccionado ningun vinculo', exitscript=True)

vinculoSeleccionado = dict(zip(nombresVinculos,vinculos))[vinculoOpciones]


subproyectoVinculos = FilteredWorksetCollector(vinculoSeleccionado.GetLinkDocument()).OfKind(WorksetKind.UserWorkset).ToWorksets()
nombresSubproyectosVinculos = {sub.Name: sub for sub in subproyectoVinculos}
subproyectosSeleccionados = forms.SelectFromList.show(sorted(nombresSubproyectosVinculos),
                                title = "Subproyectos",
                                multiselect= True,
                                #name_attr='Id',
                                button_name='Seleccionar Subproyectos')
if not subproyectosSeleccionados:
    forms.alert('No se ha seleccionado ningun subproyecto', exitscript=True)

listaSubproyectosSeleccionados = []

for subs in subproyectosSeleccionados:
    listaSubproyectosSeleccionados.append(nombresSubproyectosVinculos[subs])



#--------------------CODIGO---------------------


vinculo_copiar_subproyectos(vinculoSeleccionado, listaSubproyectosSeleccionados)