# -*- coding: utf-8 -*-

__title__ = "Aislar \nSubproyectos"
__autor__ = "César Sala Gago"
__doc__ = """Aísla temporalmente los subproyectos seleccionado.
"""


#---------------IMPORTACIONES----------------

import clr

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import (FilteredWorksetCollector, WorksetKind, ElementWorksetFilter,FilteredElementCollector, ElementId, View)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager



import System
from System.Collections.Generic import List

from pyrevit import forms

#------------------VARIABLES------------------
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document


#-----------------FUNCIONES-------------------

def seleccion_por_nombre_subproyecto(lista_nombres):
    """USO: Introducir el nombre de un subproyecto y obtener su Autodesk.Revit.DB.Workset"""
    
    if doc.IsWorkshared:
        coleccion = (FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets())
        nombres = [sub.Name for sub in coleccion]
        salida = []
        for nombre in lista_nombres:        
            if nombre in nombres:
                salida.append(dict(zip(nombres, coleccion))[nombre])
                  
            else:
                salida = ("Error: Se recomienda revisar el nombre del subproyecto")
                    

    else:
        salida = "Error: Documento no compartido"
    return salida
        

def instancias_por_subproyecto(lista_subs):
    """USO: Colectar todas las instancias en un subproyecto"""
    salida = []
    for sub in lista_subs:
        if isinstance(sub, Autodesk.Revit.DB.Workset):
            filtro = ElementWorksetFilter(sub.Id, False)
            salida.append((FilteredElementCollector(doc).WherePasses(filtro).WhereElementIsNotElementType().ToElements()))
        else: 
            salida = "Error: Workset no válido"
    salida = [item for sublist in salida for item in sublist]      
    return salida

def visibilidad_aislar_temporalmente(lista, vista = doc.ActiveView):
    
    tran = Autodesk.Revit.DB.Transaction(doc,"do")
    """USO: Aisla temporalmente los elementos de la lista"""
    if hasattr(lista, '__iter__'):
        idLista = List[ElementId]() 
        for elemento in lista:
            if elemento.Id is not None:
                idLista.Add(elemento.Id)
                
        try:
            tran.Start()
            vista.IsolateElementsTemporary(idLista)
            tran.Commit() 
            salida = vista
            
        except:
            salida = "Error: No se han podido aislar los elementos"
           
    else:
        salida = "Error: Se esperaba una lista de elementos"
        
    return salida

def visibilidad_seleccionar_elementos(lista):
    """USO: Seleccionar los elementos de la lista"""
    uidoc = __revit__.ActiveUIDocument
    idLista = List[ElementId]()
    
    for elemento in lista:
        if elemento.Id is not None:
            idLista.Add(elemento.Id)
            
    try:
        uidoc.Selection.SetElementIds(idLista)
        salida = "Completado: Elementos seleccionados"
    except:
        salida = "Error: No se han podido seleccionar los elementos"
        
    return salida       

#--------------------UI---------------------

ops = (FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets())
dict_ops = {view.Name: view for view in ops}
res = forms.SelectFromList.show(sorted(dict_ops),
                                multiselect= True,
                                #name_attr='Name',
                                button_name='Seleccionar Subproyecto')

if not res:
    forms.alert('No se ha seleccionado ningun subproyecto', exitscript=True)

nombre_sub = [item for item in res]


#--------------------CODIGO---------------------

subproyecto = seleccion_por_nombre_subproyecto(nombre_sub)

instancias = instancias_por_subproyecto(subproyecto)     
visibilidad_aislar_temporalmente(instancias)
visibilidad_seleccionar_elementos(instancias)