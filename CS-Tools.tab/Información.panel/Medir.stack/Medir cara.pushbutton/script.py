# -*- coding: utf-8 -*-

__title__ = "Medir \ncara"
__autor__ = "César Sala Gago"
__doc__ = """Medir la cara seleccionada del elemento"""


#---------------IMPORTACIONES----------------
import clr
clr.AddReference("RevitAPI")


from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import TaskDialog, TaskDialogIcon, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

uidoc = __revit__.ActiveUIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

import sys
import System
from System.Collections.Generic import List

# FUNCIONES
# ............................................................................

def mensaje_inicio_tarea(mensaje):
    """USO: Introducir los argumentos para generar un TaskDialog

    
    """
    
    titulo = "Automatizaciones"
    if sys.implementation.name == "cpython":
        ventana= TaskDialog.Show(titulo, mensaje,(TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel))
        
        resultado = ventana
        
    else:
        ventana = TaskDialog(titulo)
        ventana.MainInstruction = "Instrucciones"
        ventana.TitleAutoPrefix = False
        ventana.FooterText = "Esperando al usuario..."
        ventana.MainContent = mensaje
        ventana.MainIcon = TaskDialogIcon.TaskDialogIconInformation
        ventana.CommonButtons = (TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel)

        resultado = ventana.Show()
        
    salida = True if resultado == TaskDialogResult.Ok else False
    return salida

def mensaje_salida(mensaje):
    """USO: Introducir los argumentos para generar un TaskDialog

    
    """

    titulo = "Automatizaciones"
    if sys.implementation.name == "cpython":
        ventana= TaskDialog.Show(titulo, mensaje,(TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel))
        
        resultado = ventana
        
    else:
        ventana = TaskDialog(titulo)
        ventana.MainInstruction = "Resultado"
        ventana.TitleAutoPrefix = False
        ventana.FooterText = "Cerrar para completar"
        ventana.MainContent = mensaje
        ventana.MainIcon = TaskDialogIcon.TaskDialogIconInformation
        ventana.CommonButtons = (TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel)

        resultado = ventana.Show()
        
def ui_seleccion_objeto_elemento(inicio):
    """USO: Seleccionar un objeto del modelo por el usuario
    
    Inicio (bool): da inicio al proceso
    
    Salida (str): en caso de no introducir un True"""    
    
    if inicio:
        try:
            seleccion = uidoc.Selection.PickObject(ObjectType.Element)
            
            id = seleccion.ElementId
            salida = doc.GetElement(id)
            
        except:
            salida = "Proceso cancelado"
            
    else:
        salida = "Introducir un True para ejecutar"
        
    return salida      

def unidades_area_a_modelo(arg):
	
    """USO: Convierte unidades internas a modelo en revit 2022
    
    UNIDADES DE ÁREA"""
    
    if int(doc.Application.VersionNumber) >= 2022:
        unidadModelo = Document.GetUnits(doc).GetFormatOptions(SpecTypeId.Area).GetUnitTypeId()
        return UnitUtils.ConvertFromInternalUnits(arg, unidadModelo)    
    else: 
        unidadModelo = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Area).DisplayUnits
        return UnitUtils.ConvertFromInternalUnits(arg, unidadModelo)    
    
    
def ui_seleccion_objeto_cara(inicio):
    if inicio:
        try:
            mensaje = "Esperando selección de cara"
            seleccion = uidoc.Selection.PickObject(ObjectType.Face, mensaje)
            salida = (doc.GetElement(seleccion).GetGeometryObjectFromReference(seleccion))
            
        except:
            salida = "Proceso cancelado"
            
    else:
        salida = "Introducir un true para inciar"
        
    return salida
# ENTRADA
# ............................................................................

instrucciones = ("Seleccionar una cara para consultar su área")

# CODIGO
# ............................................................................

inicio = mensaje_inicio_tarea(instrucciones)

if inicio:
    cara = ui_seleccion_objeto_cara(inicio)
    
    if cara:
        if isinstance(cara, str):
            mensaje = cara
        
        else:
            area = cara.Area
            salida = round(unidades_area_a_modelo(area), 3)
            mensaje = "La cara seleccionada tiene {} m2".format(salida)
                      
    else:
        mensaje = "Esta cara no ha aportado el valor esperado"
        
    mensaje_salida(mensaje)
    salida = mensaje
    
else:
    salida = "Proceso no iniciado"
# ............................................................................

OUT = salida