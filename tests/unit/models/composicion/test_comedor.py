import pytest
from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedor:
    @pytest.fixture
    def comedor_basico(self):
        mesa = Mesa(
            nombre="Mesa Comedor",
            material="Roble",
            color="Terracota",
            precio_base=200.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=6,
        )

        sillas = [
            Silla(
                nombre="Silla Comedor",
                material="Roble",
                color="Terracota",
                precio_base=50.0,
                tiene_respaldo=True,
                material_tapizado=None,
                altura_regulable=False,
                tiene_ruedas=False,
            )
            for _ in range(6)
        ]

        return Comedor("Comedor Familiar", mesa, sillas)

    @pytest.fixture
    def silla_extra(self):
        return Silla(
            nombre="Silla Extra",
            material="Roble",
            color="Terracota",
            precio_base=50.0,
            tiene_respaldo=True,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

    def test_composicion_correcta(self, comedor_basico):
        assert comedor_basico.mesa is not None
        assert len(comedor_basico.sillas) == 6
        assert isinstance(comedor_basico.mesa, Mesa)
        assert all(isinstance(silla, Silla) for silla in comedor_basico.sillas)

    def test_calcular_precio_total_con_descuento(self, comedor_basico):
        precio_total = comedor_basico.calcular_precio_total()

        # Mesa:
        # precio_base = 200.0
        # factor_tamaño = 1.048 -> 200.0 * 1.048 = 209.6
        # ajuste por capacidad (> 4) = +50
        precio_mesa = 259.6

        # Sillas:
        # precio_base = 50.0
        # factor_comodidad (respaldo=True) = 1.1 -> 50.0 * 1.1 = 55.0
        precio_silla = 55.0
        total_sillas = 6 * precio_silla  # 330.0

        subtotal = precio_mesa + total_sillas  # 589.6
        precio_esperado = round(subtotal * 0.95, 2)  # 560.12

        assert precio_total == precio_esperado

    def test_calcular_precio_total_sin_descuento(self):
        mesa = Mesa(
            nombre="Mesa Pequeña",
            material="Madera",
            color="Blanco",
            precio_base=100.0,
            forma="rectangular",
            largo=80.0,
            ancho=60.0,
            altura=75.0,
            capacidad_personas=3,
        )

        sillas = [
            Silla(
                nombre="Silla 1",
                material="Madera",
                color="Blanco",
                precio_base=50.0,
                tiene_respaldo=True,
                material_tapizado=None,
                altura_regulable=False,
                tiene_ruedas=False,
            )
            for _ in range(3)
        ]

        comedor = Comedor("Comedor Sin Descuento", mesa, sillas)
        precio_total = comedor.calcular_precio_total()

        # Mesa: 100 * 1.024 = 102.4
        # Sillas: 3 * 55 = 165
        # Total: 267.4
        assert precio_total == 267.4

    def test_agregar_silla(self, comedor_basico, silla_extra):
        resultado = comedor_basico.agregar_silla(silla_extra)

        # Ya está lleno (capacidad 6)
        assert "capacidad máxima" in resultado.lower()
        assert len(comedor_basico.sillas) == 6

    def test_quitar_silla(self, comedor_basico):
        resultado = comedor_basico.quitar_silla()

        assert "removida del comedor" in resultado.lower()
        assert len(comedor_basico.sillas) == 5

    def test_quitar_silla_sin_sillas(self):
        mesa = Mesa(
            nombre="Mesa Vacía",
            material="Madera",
            color="Negro",
            precio_base=100.0,
        )

        comedor = Comedor("Comedor Vacío", mesa, [])
        resultado = comedor.quitar_silla()

        assert resultado == "No hay sillas para quitar"

    def test_obtener_resumen(self, comedor_basico):
        resumen = comedor_basico.obtener_resumen()

        assert resumen["nombre"] == "Comedor Familiar"
        assert resumen["total_muebles"] == 7
        assert resumen["capacidad_personas"] == 6
        assert "precio_total" in resumen
        assert isinstance(resumen["materiales_utilizados"], list)

    def test_obtener_descripcion_completa(self, comedor_basico):
        descripcion = comedor_basico.obtener_descripcion_completa()

        assert "COMEDOR COMEDOR FAMILIAR" in descripcion.upper()
        assert "MESA:" in descripcion
        assert "SILLAS" in descripcion
        assert "PRECIO TOTAL" in descripcion

    def test_len(self, comedor_basico):
        assert len(comedor_basico) == 7