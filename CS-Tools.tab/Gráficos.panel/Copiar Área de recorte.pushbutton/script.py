# -*- coding: utf-8 -*-

__title__ = "Copiar \nArea de recorte"
__autor__ = "César Sala Gago"
__doc__ = """Copia el área de recorte de una vista a una o varias vistas seleccionadas.

1- Selecciona la vista con el área de recorte que se quieren copiar.
2- Selecciona las vistas de destino.
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

def vista_transferir_region_recorte(origen, destino):
    if isinstance(origen, View):
        if isinstance(destino, list):
            if origen in destino:
                salida = "La vista de origen está seleccionada como vista de destino"

            else:
                activa = origen.CropBoxActive
                visible = origen.CropBoxVisible
                region = origen.GetCropRegionShapeManager().GetCropShape()

                contorno = list(region)[0]

                
                for vista in destino:
                    vista.CropBoxActive = activa
                    vista.CropBoxVisible = visible
                    vista.GetCropRegionShapeManager().SetCropShape(contorno) 

                
                salida = "Se han transferido las propiedades a {} vistas".format(len(destino))

        else:
            salida = "Revisar, se esperaba una lista de vistas"
    else:
        salida = "Se esperaba una vista"
    return salida

#-----------------CÓDIGO-------------------

todas_vistas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

    
dict_vistas_origen = {view.Name: view for view in todas_vistas}


selec_vista_origen = forms.SelectFromList.show(sorted(dict_vistas_origen),
                                title="Origen",
                                multiselect=False,
                                button_name='Seleccionar vista')

if not selec_vista_origen:
    forms.alert('No se ha seleccionado ninguna vista', exitscript=True)


vista_origen = dict_vistas_origen[selec_vista_origen]

dict_vistas_destino = {v.Name: v for v in todas_vistas}

selec_dest_vistas = forms.SelectFromList.show(sorted(dict_vistas_destino),
                                title="Vistas",
                                multiselect=True,
                                button_name='Seleccionar vistas')

if not selec_dest_vistas:
    forms.alert('No se ha seleccionado ninguna vista', exitscript=True)

vista_destino = [dict_vistas_origen[v_name] for v_name in selec_dest_vistas]

with Transaction(doc, __title__) as t:
    t.Start()
    vista_transferir_region_recorte(vista_origen,vista_destino)    
    t.Commit()