# -*- coding: utf-8 -*-

__title__ = "Seleccionar cotas"
__autor__ = "César Sala Gago"
__doc__ = """
"""


#---------------IMPORTACIONES----------------

import clr
clr.AddReference("RevitAPI")

from Autodesk.Revit.DB import ElementId, CategoryType, FilteredElementCollector, BuiltInCategory, Dimension

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
    

    rectangulo = [ele for ele in seleccion if ele.Category and ele.Category.CategoryType == CategoryType.Annotation]
    filtro = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions).ToElements()
    salida = []
    for i in rectangulo:
        if isinstance(i, Dimension):
            salida.append(i)

    visibilidad_seleccionar_elementos(salida)

else:
    salida = "Proceso cancelado"

       
# SALIDA
# ............................................................................

OUT = salida