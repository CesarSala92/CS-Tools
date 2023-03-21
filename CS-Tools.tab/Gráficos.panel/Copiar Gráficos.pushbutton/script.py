# -*- coding: utf-8 -*-

__title__ = "Copiar \ngráficos"
__autor__ = "César Sala Gago"
__doc__ = """Copia las carácteristicas gráficas de un elemento
"""

# BIBLIOTECAS
# ............................................................................

import clr
clr.AddReference("RevitAPI")

import Autodesk

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import TaskDialog, TaskDialogIcon, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
tran = Autodesk.Revit.DB.Transaction(doc,"do")

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

def mensaje_confirmar_tarea(mensaje):
    titulo = "Automatizaciones"
    if sys.implementation.name == "cpython":
        ventana= TaskDialog.Show(titulo, mensaje,(TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No))
        
        resultado = ventana
        
    else:
        ventana = TaskDialog(titulo)
        ventana.MainInstruction = "Confirmar"
        ventana.TitleAutoPrefix = False
        ventana.FooterText = "Esperando al usuario..."
        ventana.MainContent = mensaje
        ventana.MainIcon = TaskDialogIcon.TaskDialogIconInformation
        ventana.CommonButtons = (TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No)

        resultado = ventana.Show()
        
    salida = True if resultado == TaskDialogResult.Yes else False
    return salida

def ui_seleccion_objetos_subelementos(inicio):
    if inicio:
        try:
            seleccion = uidoc.Selection.PickObjects(ObjectType.Subelement)

            salida = [doc.GetElement(ref.ElementId) for ref in seleccion]

        except:
            salida = "Proceso cancelado"

    else:
        salida = "Introducir un True para iniciar"

    return salida


    
# ENTRADA
# ............................................................................

instrucciones1 = "Seleccionar una instancia para transferir sus modificaciones al siguiente grupo de seleccion"
instrucciones2 = "Para continuar: pulsar Si para inciail la seleccion de instancias a modificar"

# CODIGO
# ............................................................................

inicio = mensaje_inicio_tarea(instrucciones1)

if inicio:
    seleccion1 = ui_seleccion_objeto_elemento(inicio)
    if seleccion1:
        if isinstance(seleccion1, str):
            salida = seleccion1
        else:
            vista = doc.ActiveView
            mod = vista.GetElementOverrides(seleccion1.Id)
            confirmacion = mensaje_confirmar_tarea(instrucciones2)

            if confirmacion:
                seleccion2 = ui_seleccion_objetos_subelementos(confirmacion)
                if seleccion2:
                    if isinstance(seleccion2,str):
                        salida = seleccion2
                    else:
                        tran.Start()
                        for ins in seleccion2:
                            vista.SetElementOverrides(ins.Id, mod)
                        tran.Commit()
                        salida = seleccion2

                else:
                    salida = "Proceso cancelado"

            else:
                    salida = "Proceso cancelado"

    else:
        salida = "Selección erronea"

else: salida = "Proceso no iniciado"