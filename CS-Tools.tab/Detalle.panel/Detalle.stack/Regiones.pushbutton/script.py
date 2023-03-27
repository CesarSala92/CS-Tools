# -*- coding: utf-8 -*-

__title__ = "Seleccionar regiones"
__autor__ = "César Sala Gago"
__doc__ = """
"""


#---------------IMPORTACIONES----------------

import clr
clr.AddReference("RevitAPI")

from Autodesk.Revit.DB import ElementId, CategoryType, FilteredElementCollector, BuiltInCategory, FilledRegion

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import TaskDialog, TaskDialogIcon, TaskDialogCommonButtons, TaskDialogResult

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
"""doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument"""

import sys
import System
from System.Collections.Generic import List


#------------------VARIABLES------------------
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__.Application
doc = __revit__.ActiveUIDocument.Document


# BIBLIOTECAS
# ............................................................................

# FUNCIONES
# ............................................................................

def mensaje_inicio_tarea(mensaje):
    """USO: Generar un mensaje de inicio de tarea, si se acepta devuelve un True
       ARGS: Mensaje en forma de cadena de texto
       SALIDA: True o False
    """
    
    titulo = "CS-TOOLS"
    if sys.implementation.name == "cpython":
        ventana= TaskDialog.Show(titulo, mensaje,(TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel))
        
        resultado = ventana
        
    else:
        ventana = TaskDialog(titulo)
        ventana.MainInstruction = "Información"
        ventana.TitleAutoPrefix = False
        ventana.FooterText = "Esperando acción del usuario"
        ventana.MainContent = mensaje
        ventana.MainIcon = TaskDialogIcon.TaskDialogIconInformation
        ventana.CommonButtons = (TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel)

        resultado = ventana.Show()
        
    salida = True if resultado == TaskDialogResult.Ok else False
    return salida

def visibilidad_seleccionar_elementos(lista):
    """USO: Seleccionar los elementos de la lista"""
    
    # Se accede al bojeto que representa el proyecto actualmente activo
    uidoc = __revit__.ActiveUIDocument
    
    idLista = List[ElementId]()
    for elemento in lista:
        if elemento.Id is not None:
            idLista.Add(elemento.Id)
            
    try:
        uidoc.Selection.SetElementIds(idLista)
        salida = "Completado: Elementos seleccionados"
    except:
        salida = "Fallo"
    return salida   

def ui_seleccion_rectangulo(inicio):
    if inicio:
        try:
            seleccion = uidoc.Selection.PickElementsByRectangle()
            salida = list(seleccion)

        except:
            salida = "Proceso cancelado"
            
    else:
        salida = "Introducir True para iniciar"

    return salida
    
# ENTRADA
# ............................................................................

instrucciones = "Generar un rectangulo de seleccion para seleccionar las intancias de anotación deseadas"


# CODIGO
# ............................................................................

inicio = mensaje_inicio_tarea(instrucciones)

if inicio:
    seleccion = ui_seleccion_rectangulo(inicio)
    

    rectangulo = [ele for ele in seleccion if ele.Category and ele.Category.CategoryType == CategoryType.Model]
    filtro = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents).ToElements()
    salida = []
    for i in rectangulo:
        if isinstance(i, FilledRegion):
            salida.append(i)

    visibilidad_seleccionar_elementos(salida)

else:
    salida = "Proceso cancelado"
       
# SALIDA
# ............................................................................

OUT = salida