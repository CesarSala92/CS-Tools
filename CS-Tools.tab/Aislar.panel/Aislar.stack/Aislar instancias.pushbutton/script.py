# -*- coding: utf-8 -*-

__title__ = "Aislar \ninstancias similares"
__autor__ = "César Sala Gago"
__doc__ = """Aísla temporalmente las instancias similares a la seleccionada"""

# BIBLIOTECAS
# ............................................................................

import Autodesk
import clr
clr.AddReference("RevitAPI")

from Autodesk.Revit.DB import FilteredElementCollector, ElementId, Category, ElementType, FamilySymbol, FamilyInstanceFilter

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import TaskDialog, TaskDialogIcon, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc =  __revit__.ActiveUIDocument.Document
app = __revit__.Application
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = __revit__.ActiveUIDocument
tran = Autodesk.Revit.DB.Transaction(doc,"do")



import sys
import System
from System.Collections.Generic import List

# FUNCIONES
# ............................................................................

def instancias_por_tipo(tipos):
    """USO: Seleccionar un tipo de familia por normbre
    """
    if isinstance(tipos, ElementType):
        salida = [ins for ins in FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements() if ins.GetTypeId() == tipos.Id]
    elif isinstance(tipos, FamilySymbol):
        filtro = FamilyInstanceFilter(doc, tipos.Id)
        salida = (FilteredElementCollector(doc).WherePasses(filtro).ToElements())
    else: 
        salida = "Introducir un Element Type o FamilySymbol"
        
    return salida


def visibilidad_aislar_temporalmente(lista, vista = doc.ActiveView):
    """USO: Aisla temporalmente los elementos de la lista

    Args:
        lista (list): elementos a ailsar
        vista (vista, optional): Si no se selecciona ninguna se escoge la actual. Defaults to doc.ActiveView.

    Returns:
        _type_: _description_
    """
    if hasattr(lista, '__iter__'):
        # Comprobamos que el argumento sea una lista de elementos.
        idLista = List[ElementId]() # Creamos una lista que contenga los ids delos elementos, es una lista fuertemente tipada
        for elemento in lista:
            if elemento.Id is not None:
                idLista.Add(elemento.Id)
                
        try:
        
            tran.Start()
            vista.IsolateElementsTemporary(idLista)
            salida = vista
            tran.Commit()
            
        except:
            salida = "Error"
            
    else:
        salida = "Se esperaba una lista de elementos"
        
    return salida

def instancias_por_categoria(cat):
    """USO: Colectar todas las instancias de una categorica

    Args:
        cat (Categoria)
        
    Salida: Lista de categorias
    """
    if isinstance(cat, Category):
        salida = FilteredElementCollector(doc).OfCategoryId(cat.Id).WhereElementIsNotElementType().ToElements()
        
    else: 
        salida = "Introducir una categoria"
        
    return salida

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
    
# ENTRADA
# ............................................................................

instrucciones = "Seleccionar una instancia para aislar todas las instancias similares del modelo en la vista actual."

# CODIGO
# ............................................................................

inicio = mensaje_inicio_tarea(instrucciones)

if inicio:
    seleccion = ui_seleccion_objeto_elemento(inicio)
    if isinstance(seleccion, str):
        salida = seleccion
        
    else:
        if seleccion.GetTypeId() != ElementId.InvalidElementId:
            id = seleccion.GetTypeId()
            tipo = doc.GetElement(id)
            
            instancias = instancias_por_tipo(tipo)
            
        else:
            categoria = seleccion.Category
            instancias = instancias_por_categoria(categoria)
            
        mensaje = "Se han localizado {} elementos partiendo de la instancia seleccionada. Al cerrar se aislaran todas las intancias".format(len(instancias))
        mensaje_salida(mensaje)
        visibilidad_aislar_temporalmente(instancias)
        salida = mensaje
        
else:
    salida = "Proceso no iniciado"
        
# SALIDA
# ............................................................................

OUT = salida