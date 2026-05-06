import pytest
from src.models.concretos.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedor:
    @pytest.fixture
    def mesa_basica(self):
        return Mesa(
            nombre="Mesa Familiar",
            material="Madera",
            color="Roble",
            precio_base=200.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=6,
        )

    @pytest.fixture
    def silla_1(self):
        return Silla(
            nombre="Silla 1",
            material="Madera",
            color="Café",
            precio_base=50.0,
            tiene_respaldo=True,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def silla_2(self):
        return Silla(
            nombre="Silla 2",
            material="Madera",
            color="Café",
            precio_base=50.0,
            tiene_respaldo=True,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def comedor_basico(self, mesa_basica, silla_1, silla_2):
        return Comedor(mesa_basica, [silla_1, silla_2])

    @pytest.fixture
    def comedor_vacio(self, mesa_basica):
        return Comedor(mesa_basica, [])

    def test_instanciacion_correcta(self, comedor_basico, mesa_basica):
        assert comedor_basico.mesa is mesa_basica
        assert len(comedor_basico.sillas) == 2
        assert all(isinstance(silla, Silla) for silla in comedor_basico.sillas)

    def test_calcular_precio_total_con_sillas(self, comedor_basico):
        precio_total = comedor_basico.calcular_precio_total()

        # Mesa:
        # 200.0 * 1.048 = 209.6
        # +50 por capacidad > 4 = 259.6
        precio_mesa = 259.6

        # Sillas:
        # cada silla: 50.0 * 1.1 = 55.0
        precio_sillas = 2 * 55.0  # 110.0

        precio_esperado = round(precio_mesa + precio_sillas, 2)  # 369.6

        assert precio_total == pytest.approx(precio_esperado)

    def test_calcular_precio_total_sin_sillas(self, comedor_vacio):
        precio_total = comedor_vacio.calcular_precio_total()

        # Solo la mesa
        precio_esperado = 259.6
        assert precio_total == pytest.approx(precio_esperado)

    def test_agregar_silla(self, comedor_vacio, silla_1):
        comedor_vacio.agregar_silla(silla_1)

        assert len(comedor_vacio.sillas) == 1
        assert comedor_vacio.sillas[0] is silla_1

    def test_quitar_silla_existente(self, comedor_basico, silla_1):
        comedor_basico.quitar_silla(silla_1)

        assert len(comedor_basico.sillas) == 1
        assert silla_1 not in comedor_basico.sillas

    def test_quitar_silla_inexistente_no_cambia_nada(self, comedor_basico):
        silla_inexistente = Silla(
            nombre="Silla Fantasma",
            material="Metal",
            color="Negro",
            precio_base=60.0,
            tiene_respaldo=False,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

        comedor_basico.quitar_silla(silla_inexistente)

        assert len(comedor_basico.sillas) == 2

    def test_cantidad_sillas(self, comedor_basico):
        assert comedor_basico.cantidad_sillas() == 2

    def test_descripcion(self, comedor_basico):
        descripcion = comedor_basico.descripcion()

        assert "Comedor con mesa:" in descripcion
        assert "Mesa: Mesa Familiar" in descripcion
        assert "y 2 sillas:" in descripcion
        assert "1. Silla:" in descripcion
        assert "2. Silla:" in descripcion