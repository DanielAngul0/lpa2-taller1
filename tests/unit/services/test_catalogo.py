import pytest

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
from src.services.catalogo import (
    cargar_catalogo_completo,
    cargar_catalogo_en_tienda,
    crear_catalogo_inicial,
    crear_comedores_ejemplo,
    crear_descuentos_ejemplo,
)


class FakeTienda:
    def __init__(self):
        self.muebles = []
        self.comedores = []
        self.descuentos = {}

    def agregar_mueble(self, mueble):
        self.muebles.append(mueble)
        return "Mueble agregado exitosamente"

    def agregar_comedor(self, comedor):
        self.comedores.append(comedor)
        return "Comedor agregado exitosamente"

    def aplicar_descuento(self, categoria, porcentaje):
        self.descuentos[categoria] = porcentaje
        return "Descuento aplicado exitosamente"


class TestCatalogo:
    def test_crear_catalogo_inicial_devuelve_17_muebles(self):
        catalogo = crear_catalogo_inicial()

        assert len(catalogo) == 17
        assert isinstance(catalogo[0], Silla)
        assert isinstance(catalogo[3], Mesa)
        assert isinstance(catalogo[6], Sillon)
        assert isinstance(catalogo[9], Armario)
        assert isinstance(catalogo[10], Cajonera)
        assert isinstance(catalogo[12], Cama)
        assert isinstance(catalogo[14], Escritorio)
        assert isinstance(catalogo[-1], SofaCama)

    def test_crear_catalogo_inicial_contenido_basico(self):
        catalogo = crear_catalogo_inicial()
        nombres = [mueble.nombre for mueble in catalogo]

        assert "Silla Clásica" in nombres
        assert "Mesa de Comedor Familiar" in nombres
        assert "Sillón Reclinable de Lujo" in nombres
        assert "Armario Ropero 4 Puertas" in nombres
        assert "Cama King Size de Lujo" in nombres
        assert "SofaCama Convertible Premium" in nombres

    def test_crear_comedores_ejemplo_devuelve_2_comedores(self):
        comedores = crear_comedores_ejemplo()

        assert len(comedores) == 2
        assert all(isinstance(comedor, Comedor) for comedor in comedores)
        assert comedores[0].nombre == "Comedor Familiar Completo"
        assert comedores[1].nombre == "Comedor Moderno Premium"
        assert len(comedores[0].sillas) == 6
        assert len(comedores[1].sillas) == 4
        assert isinstance(comedores[0].mesa, Mesa)
        assert isinstance(comedores[1].mesa, Mesa)

    def test_crear_descuentos_ejemplo(self):
        descuentos = crear_descuentos_ejemplo()

        assert descuentos == {
            "silla": 10,
            "mesa": 15,
            "sofa": 20,
        }

    def test_cargar_catalogo_en_tienda(self):
        tienda = FakeTienda()

        resumen = cargar_catalogo_en_tienda(tienda)

        assert resumen == {
            "muebles_agregados": 17,
            "comedores_agregados": 2,
            "descuentos_aplicados": 3,
        }
        assert len(tienda.muebles) == 17
        assert len(tienda.comedores) == 2
        assert tienda.descuentos == {"silla": 10, "mesa": 15, "sofa": 20}

    def test_cargar_catalogo_completo(self):
        catalogo = cargar_catalogo_completo()

        assert set(catalogo.keys()) == {"muebles", "comedores", "descuentos"}
        assert len(catalogo["muebles"]) == 17
        assert len(catalogo["comedores"]) == 2
        assert catalogo["descuentos"] == {"silla": 10, "mesa": 15, "sofa": 20}