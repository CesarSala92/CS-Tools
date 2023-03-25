# -*- coding: utf-8 -*-

__title__ = "Crear \nFitros CIZ"
__autor__ = "César Sala Gago"
__doc__ = """
"""

#---------------IMPORTACIONES----------------
from random import randint
import Autodesk
import clr
clr.AddReference("RevitAPI")

from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
import sys
import System
from System.Collections.Generic import *
from RevitServices.Transactions import TransactionManager



#------------------VARIABLES------------------
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
tran = Autodesk.Revit.DB.Transaction(doc,"do")

# FUNCIONES
# ............................................................................

def elementos_por_nombre_bic(arg = None):
    enumNombres = System.Enum.GetNames(BuiltInCategory)
    enumValores = System.Enum.GetValues(BuiltInCategory)
    # Comprobamos si se ha instroducido un arguments
    if bool(arg):
        # Si el argumento está en la lista de nombre buscamos el indice de dicho elemento
        # Para utilizar el index tenemos que pasar los enumeradores a lista, metemos como arguemtno el nombre y no devuelve su indice
    
        if arg in enumNombres:
            indice = list(enumNombres).index(arg)
            """Vamos a extraer la bic de enumValores (la lsita ordenada con todos los bic) buscando por su indice"""
            # El bic de salida será el enumValores con ese indice
            bic = enumValores[indice]
            
            # la coleccion será tods los elementos que tengan esa BIC
            coleccion = (FilteredElementCollector(doc).OfCategory(bic).ToElements())
            
            salida = {"Instancias" : [], "Tipos" : []}
            
            # Ordenamos los elementos según si es instancia o tipo
            
            for ele in list(coleccion):
                if ele.GetTypeId() == ElementId.InvalidElementId:
                    salida["Tipos"].append(ele)
                else:
                    salida["Instancias"].append(ele)
                  
        else:
            # Si se ha introducido un valor que es incorrecto primero comprobamos si la diferencia está en la mayusculas usada
            coincidencias = []
            for nombre in enumNombres:
                if arg.lower() in nombre.lower():
                    coincidencias.append(nombre)

            mensaje1 = ("Se han encontrado algunas coincidencias, revisar.")
            
            mensaje2 = ("No se han encontrado coincidencias, resvisar nombre")
            
            
            if bool (coincidencias):
                salida = [mensaje1, sorted(coincidencias)]
                
            else: 
                salida = mensaje2        
    else:
        salida = sorted(enumNombres)
    
    return salida

def unidades_internas_a_metros(num):
    if isinstance(num, int) or isinstance(num, float):
        if int(doc.Application.VersionNumber) >= 2022:
            unidad = UnitTypeId.Meters
            return UnitUtils.ConvertFromInternalUnits(float(num), unidad)
        else:
            unidad = DisplayUnitType.DUT_METERS
            return UnitUtils.ConvertFromInternalUnits(float(num), unidad)
        
    else:
        return None

def unidades_metros_a_internas(num):
    if isinstance(num, int) or isinstance(num, float):
        if int(doc.Application.VersionNumber) >= 2022:
            unidad = UnitTypeId.Meters
            return UnitUtils.ConvertToInternalUnits(float(num), unidad)
        else:
            unidad = DisplayUnitType.DUT_METERS
            return UnitUtils.ConvertToInternalUnits(float(num), unidad)
        
    else:
        return None

def obtener_cota_inferior_zapatas(lista_zapatas):
    parametro = BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM_SURVEY
    lista_ciz = []
    for zapata in lista_zapatas:
        if zapata.get_Parameter(parametro).AsDouble() not in lista_ciz:
            lista_ciz.append(zapata.get_Parameter(parametro).AsDouble())
    return lista_ciz

def crear_filtro_zapatas(prefjio, cota):
    filtrosProyecto = FilteredElementCollector(doc).OfClass(ParameterFilterElement)
    cat = List[ElementId]()
    cat.Add(ElementId(BuiltInCategory.OST_StructuralFoundation))
    parametro = BuiltInParameter.STRUCTURAL_ELEVATION_AT_BOTTOM_SURVEY
    nombre = prefjio + str(round(unidades_internas_a_metros(cota),4))
    nombresFiltros = [f.Name for f in filtrosProyecto]
    if nombre not in nombresFiltros:
        ciz = cota
        ciz_metros = unidades_metros_a_internas(float(ciz))
        regla = (ParameterFilterRuleFactory.CreateEqualsRule(ElementId(parametro), cota, False))
        tran.Start()
        salida = (ParameterFilterElement.Create(doc, nombre, cat, ElementParameterFilter(regla)))
        tran.Commit()
    else:
        salida = None
    return salida


def patron_relleno_defecto():
    patrones = [pat for pat in FilteredElementCollector(doc).OfClass(FillPatternElement) if pat.GetFillPattern().IsSolidFill == True]
    salida = patrones[0]
    return salida

def agregar_filtros_vista(listaFiltros):
    vista = doc.ActiveView
    patron = patron_relleno_defecto()
    tran.Start()
    for f in listaFiltros:
    	if isinstance(f, ParameterFilterElement): 
        	vista.AddFilter(f.Id)
        	mod = vista.GetFilterOverrides(f.Id)
        	mod.SetSurfaceForegroundPatternColor(Color(randint(0,255),randint(0,255),randint(0,255)))
        	mod.SetSurfaceForegroundPatternId(patron.Id)
        	vista.SetFilterOverrides(f.Id, mod)
    tran.Commit()
    return None
        
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
# ENTRADA
# ............................................................................

mensaje = "Se van a generar los filtros de cota inferior de zapata en la vista actual"
listaFiltros = []

if mensaje_inicio_tarea(mensaje):
    instanciasCimentacion = elementos_por_nombre_bic("OST_StructuralFoundation")["Instancias"]
    lista_ciz = obtener_cota_inferior_zapatas(instanciasCimentacion)
    for ciz in lista_ciz:
        filtro = crear_filtro_zapatas("CIZ_", ciz)
        listaFiltros.append(filtro)
        
    agregar_filtros_vista(listaFiltros)
    


# CODIGO
# ............................................................................

       
# SALIDA
# ............................................................................

OUT = listaFiltros