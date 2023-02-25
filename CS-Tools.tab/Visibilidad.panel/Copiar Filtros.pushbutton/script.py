# -*- coding: utf-8 -*-

__title__ = "Copiar \nfiltros"
__autor__ = "César Sala Gago"
__doc__ = """Copia filtros de una vista a una o varias vistas seleccionadas.

1- Selecciona la vista con los filtros que se quieren copiar.
2- Selecciona los filtros.
3- Selecciona las vistas de destino.
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

todas_vistas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

vistas_con_filtros =[view for view in todas_vistas if view.GetFilters()]

if not vistas_con_filtros:
    forms.alert('No hay vistas con filtros en el documento', exitscript=True)
    
dict_vistas_con_filtros = {view.Name: view for view in vistas_con_filtros}

selec_vista_origen = forms.SelectFromList.show(sorted(dict_vistas_con_filtros),
                                title="Origen",
                                multiselect=False,
                                button_name='Seleccionar vista')

if not selec_vista_origen:
    forms.alert('No se ha seleccionado ninguna vista', exitscript=True)
    
vista_origen = dict_vistas_con_filtros[selec_vista_origen]

id_filtro = vista_origen.GetFilters()
filtros = [doc.GetElement(f_id) for f_id in id_filtro]
dict_filtros = {f.Name: f for f in filtros}

selec_filtros = forms.SelectFromList.show(sorted(dict_filtros),
                                title="Filtros",
                                multiselect=True,
                                button_name='Seleccionar filtros')

if not selec_filtros:
    forms.alert('No se ha seleccionado ningun filtro', exitscript=True)
    
filtros_copiar = [dict_filtros[f_name] for f_name in selec_filtros]

dict_todas_vistas = {v.Name: v for v in todas_vistas}

selec_dest_vistas = forms.SelectFromList.show(sorted(dict_todas_vistas),
                                title="Vistas",
                                multiselect=True,
                                button_name='Seleccionar vistas')

with Transaction(doc, __title__) as t:
    t.Start()

    if not selec_dest_vistas:
        forms.alert('No se ha seleccionado ninguna vista', exitscript=True)
        
    vista_destino = [dict_todas_vistas[v_name] for v_name in selec_dest_vistas]

    for filtro_vista in filtros_copiar:
        filter_sobreescribir = vista_origen.GetFilterOverrides(filtro_vista.Id)
        
        for vista in vista_destino:
            vista.SetFilterOverrides(filtro_vista.Id, filter_sobreescribir)
        
    t.Commit()