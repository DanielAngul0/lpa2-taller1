"""
Servicio auxiliar para construir el catálogo de ejemplo de la tienda.

Este módulo centraliza la creación de muebles, comedores y descuentos
para evitar repetir lógica en main.py.
"""

from __future__ import annotations

from src.models.composicion.comedor import Comedor
from src.models.concretos.armario import Armario
from src.models.concretos.cajonera import Cajonera
from src.models.concretos.cama import Cama
from src.models.concretos.escritorio import Escritorio
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla
from src.models.concretos.sillon import Sillon
from src.models.concretos.sofa import Sofa
from src.models.concretos.sofacama import SofaCama
from src.services.tienda import TiendaMuebles


def crear_catalogo_inicial() -> list[object]:
    """
    Crea una lista con los muebles iniciales del sistema.

    Returns:
        list[object]: Lista de muebles listos para agregarse a la tienda.
    """
    sillas = [
        Silla(
            nombre="Silla Clásica",
            material="Madera",
            color="Café",
            precio_base=150.0,
            tiene_respaldo=True,
            material_tapizado="tela",
        ),
        Silla(
            nombre="Silla de Oficina Ejecutiva",
            material="Metal",
            color="Negro",
            precio_base=350.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        ),
        Silla(
            nombre="Silla Moderna Minimalista",
            material="Plástico",
            color="Blanco",
            precio_base=80.0,
            tiene_respaldo=True,
        ),
    ]

    mesas = [
        Mesa(
            nombre="Mesa de Comedor Familiar",
            material="Madera",
            color="Roble",
            precio_base=500.0,
            forma="rectangular",
            capacidad_personas=6,
        ),
        Mesa(
            nombre="Mesa de Centro Redonda",
            material="Vidrio",
            color="Transparente",
            precio_base=300.0,
            forma="redonda",
            capacidad_personas=4,
        ),
        Mesa(
            nombre="Mesa de Trabajo Industrial",
            material="Metal",
            color="Gris",
            precio_base=450.0,
            forma="rectangular",
            capacidad_personas=4,
        ),
    ]

    asientos_grandes = [
        Sillon(
            nombre="Sillón Reclinable de Lujo",
            material="Cuero",
            color="Marrón",
            precio_base=800.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            es_reclinable=True,
            tiene_reposapiés=True,
        ),
        Sofa(
            nombre="Sofá Modular de 3 Plazas",
            material="Tela",
            color="Gris",
            precio_base=1200.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="tela",
            es_modular=True,
            incluye_cojines=True,
        ),
        Sofa(
            nombre="Sofá Chesterfield Clásico",
            material="Cuero",
            color="Verde",
            precio_base=2000.0,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado="cuero",
            es_modular=False,
            incluye_cojines=False,
        ),
    ]

    almacenamiento = [
        Armario(
            nombre="Armario Ropero 4 Puertas",
            material="Madera",
            color="Blanco",
            precio_base=600.0,
            num_puertas=4,
            num_cajones=2,
            tiene_espejos=True,
        ),
        Cajonera(
            nombre="Cajonera Vintage 5 Cajones",
            material="Madera",
            color="Vintage",
            precio_base=300.0,
            num_cajones=5,
            tiene_ruedas=False,
        ),
        Cajonera(
            nombre="Cajonera Oficina con Ruedas",
            material="Metal",
            color="Gris",
            precio_base=180.0,
            num_cajones=3,
            tiene_ruedas=True,
        ),
    ]

    dormitorio_oficina = [
        Cama(
            nombre="Cama King Size de Lujo",
            material="Madera",
            color="Nogal",
            precio_base=1000.0,
            tamaño="king",
            incluye_colchon=True,
            tiene_cabecera=True,
        ),
        Cama(
            nombre="Cama Individual Juvenil",
            material="Metal",
            color="Azul",
            precio_base=400.0,
            tamaño="individual",
            incluye_colchon=False,
            tiene_cabecera=True,
        ),
        Escritorio(
            nombre="Escritorio Ejecutivo L-Shape",
            material="Madera",
            color="Caoba",
            precio_base=750.0,
            forma="L",
            tiene_cajones=True,
            num_cajones=4,
        ),
        Escritorio(
            nombre="Escritorio Gaming RGB",
            material="Metal",
            color="Negro",
            precio_base=500.0,
            forma="rectangular",
            tiene_cajones=False,
            tiene_iluminacion=True,
        ),
    ]

    sofa_cama = SofaCama(
        nombre="SofaCama Convertible Premium",
        material="Tela",
        color="Beige",
        precio_base=1500.0,
        capacidad_personas=3,
        material_tapizado="tela",
        tamaño_cama="matrimonial",
        incluye_colchon=True,
        mecanismo_conversion="hidraulico",
    )

    return (
        sillas
        + mesas
        + asientos_grandes
        + almacenamiento
        + dormitorio_oficina
        + [sofa_cama]
    )


def crear_comedores_ejemplo() -> list[Comedor]:
    """
    Crea comedores de ejemplo para demostrar la composición.

    Returns:
        list[Comedor]: Lista de comedores de ejemplo.
    """
    mesa_familiar = Mesa(
        nombre="Mesa Familiar Extensible",
        material="Madera",
        color="Roble",
        precio_base=800.0,
        forma="rectangular",
        capacidad_personas=8,
    )

    sillas_familiares = [
        Silla(
            nombre=f"Silla Familiar {i}",
            material="Madera",
            color="Roble",
            precio_base=120.0,
            tiene_respaldo=True,
            material_tapizado="tela",
        )
        for i in range(1, 7)
    ]

    comedor_familiar = Comedor(
        nombre="Comedor Familiar Completo",
        mesa=mesa_familiar,
        sillas=sillas_familiares,
    )

    mesa_moderna = Mesa(
        nombre="Mesa Moderna Cristal",
        material="Vidrio",
        color="Negro",
        precio_base=600.0,
        forma="redonda",
        capacidad_personas=4,
    )

    sillas_modernas = [
        Silla(
            nombre=f"Silla Moderna {i}",
            material="Metal",
            color="Negro",
            precio_base=150.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
        )
        for i in range(1, 5)
    ]

    comedor_moderno = Comedor(
        nombre="Comedor Moderno Premium",
        mesa=mesa_moderna,
        sillas=sillas_modernas,
    )

    return [comedor_familiar, comedor_moderno]


def crear_descuentos_ejemplo() -> dict[str, float]:
    """
    Crea descuentos de ejemplo por categoría.

    Returns:
        dict[str, float]: Diccionario con categorías y porcentaje de descuento.
    """
    return {
        "silla": 10,
        "mesa": 15,
        "sofa": 20,
    }


def cargar_catalogo_en_tienda(tienda: TiendaMuebles) -> dict[str, int]:
    """
    Carga el catálogo de ejemplo dentro de una tienda.

    Args:
        tienda: Instancia de TiendaMuebles donde se cargará el catálogo.

    Returns:
        dict[str, int]: Resumen con la cantidad de muebles, comedores y descuentos aplicados.
    """
    muebles = crear_catalogo_inicial()
    comedores = crear_comedores_ejemplo()
    descuentos = crear_descuentos_ejemplo()

    muebles_agregados = 0
    comedores_agregados = 0
    descuentos_aplicados = 0

    for mueble in muebles:
        resultado = tienda.agregar_mueble(mueble)
        if "exitosamente" in resultado.lower():
            muebles_agregados += 1

    for comedor in comedores:
        resultado = tienda.agregar_comedor(comedor)
        if "exitosamente" in resultado.lower():
            comedores_agregados += 1

    for categoria, porcentaje in descuentos.items():
        resultado = tienda.aplicar_descuento(categoria, porcentaje)
        if "aplicado" in resultado.lower():
            descuentos_aplicados += 1

    return {
        "muebles_agregados": muebles_agregados,
        "comedores_agregados": comedores_agregados,
        "descuentos_aplicados": descuentos_aplicados,
    }


def cargar_catalogo_completo() -> dict[str, object]:
    """
    Devuelve todo el catálogo de ejemplo en una sola estructura.

    Returns:
        dict[str, object]: Contiene muebles, comedores y descuentos.
    """
    return {
        "muebles": crear_catalogo_inicial(),
        "comedores": crear_comedores_ejemplo(),
        "descuentos": crear_descuentos_ejemplo(),
    }