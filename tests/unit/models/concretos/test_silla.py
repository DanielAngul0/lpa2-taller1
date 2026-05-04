import pytest
from src.models.concretos.silla import Silla


class TestSilla:
    @pytest.fixture
    def silla_basica(self):
        return Silla(
            nombre="Silla Básica",
            material="Madera",
            color="Café",
            precio_base=50.0,
            tiene_respaldo=True,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def silla_oficina(self):
        return Silla(
            nombre="Silla Oficina",
            material="Metal",
            color="Negro",
            precio_base=100.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        )

    def test_instanciacion_correcta(self, silla_basica):
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.color == "Café"
        assert silla_basica.precio_base == 50.0
        assert silla_basica.capacidad_personas == 1
        assert silla_basica.tiene_respaldo is True
        assert silla_basica.material_tapizado is None
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False

    def test_calcular_precio(self, silla_basica):
        precio = silla_basica.calcular_precio()

        # precio_base = 50.0
        # respaldo = True -> factor comodidad = 1.1
        # 50.0 * 1.1 = 55.0
        precio_esperado = 55.0

        assert precio == precio_esperado

    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion
        assert "Altura regulable: No" in descripcion
        assert "Ruedas: No" in descripcion

    def test_regular_altura_sin_ajuste(self, silla_basica):
        resultado = silla_basica.regular_altura(70)
        assert resultado == "Esta silla no tiene altura regulable"

    def test_regular_altura_valida(self, silla_oficina):
        resultado = silla_oficina.regular_altura(70)
        assert resultado == "Altura ajustada a 70 cm"

    def test_regular_altura_invalida_baja(self, silla_oficina):
        resultado = silla_oficina.regular_altura(30)
        assert resultado == "La altura debe estar entre 40 y 100 cm"

    def test_regular_altura_invalida_alta(self, silla_oficina):
        resultado = silla_oficina.regular_altura(120)
        assert resultado == "La altura debe estar entre 40 y 100 cm"

    def test_es_silla_oficina_true(self, silla_oficina):
        assert silla_oficina.es_silla_oficina() is True

    def test_es_silla_oficina_false(self, silla_basica):
        assert silla_basica.es_silla_oficina() is False

    def test_setters(self, silla_basica):
        silla_basica.altura_regulable = True
        silla_basica.tiene_ruedas = True

        assert silla_basica.altura_regulable is True
        assert silla_basica.tiene_ruedas is True