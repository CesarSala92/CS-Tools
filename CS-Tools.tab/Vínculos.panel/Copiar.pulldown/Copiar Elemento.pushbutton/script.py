# -*- coding: utf-8 -*-

__title__ = "Copiar elemento de subproyecto"
__autor__ = "César Sala Gago"
__doc__ = """
"""


## BIBLIOTECAS
# ............................................................................

import clr
clr.AddReference("RevitAPI")
import Autodesk

from Autodesk.Revit.DB import ElementId, BuiltInParameter, ElementTransformUtils, Transform, CopyPasteOptions

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

def ui_seleccion_objeto_vinculo(inicio):
    if inicio:
        try:
            seleccion = uidoc.Selection.PickObject(ObjectType.LinkedElement)

            vinculo = doc.GetElement(seleccion.ElementId)

            docVinculo = vinculo.GetLinkDocument()

            instancia = docVinculo.GetElement(seleccion.LinkedElementId)

            salida = {"Vinculo" : vinculo, "Instancia": instancia}

        except:
            salida = "Proceso Cancelado"
    return salida

def instancia_obtener_anfitrion(ins, documento = doc):
    
    bip = BuiltInParameter.HOST_ID_PARAM

    parametro = ins.get_Parameter(bip)

    if parametro == None or parametro == ElementId.InvalidElementId:
        salida = None
    else:
        id = parametro.AsElementId()
        salida = documento.GetElement(id)

    return salida


    
# ENTRADA
# ............................................................................

instrucciones = "Selecciona una instancia de un vínculo, dicha instancia se copiará en el mismo sitio si no necesita anfitrion"


# CODIGO
# ............................................................................

inicio = mensaje_inicio_tarea(instrucciones)

if inicio:
    seleccion = ui_seleccion_objeto_vinculo(inicio)

    instancia = seleccion["Instancia"]
    documento = seleccion["Vinculo"].GetLinkDocument()

    anfitrion = instancia_obtener_anfitrion(instancia, documento)

    if anfitrion:
        salida = "No se puede copiar, precisa de un anfitrion"

    else:
        iLista = List[ElementId]()
        iLista.Add(instancia.Id)

        tran.Start()
        ElementTransformUtils.CopyElements(documento, iLista, doc, Transform.Identity, CopyPasteOptions())

        tran.Commit()

        salida = "Copia completada"

else:
    salida = "Proceso no iniciado"


    

        
# SALIDA
# ............................................................................

OUT = salida