import pytest
from src.models.concretos.cajonera import Cajonera


class TestCajonera:
    @pytest.fixture
    def cajonera_basica(self):
        return Cajonera(
            nombre="Cajonera Básica",
            material="Madera",
            color="Blanco",
            precio_base=300,
            num_cajones=3,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def cajonera_con_ruedas(self):
        return Cajonera(
            nombre="Cajonera con Ruedas",
            material="Metal",
            color="Gris",
            precio_base=400,
            num_cajones=5,
            tiene_ruedas=True,
        )

    def test_instanciacion_correcta(self, cajonera_basica):
        assert cajonera_basica.nombre == "Cajonera Básica"
        assert cajonera_basica.material == "Madera"
        assert cajonera_basica.color == "Blanco"
        assert cajonera_basica.precio_base == 300
        assert cajonera_basica.num_cajones == 3
        assert cajonera_basica.tiene_ruedas is False

    def test_calcular_precio_sin_ruedas(self, cajonera_basica):
        precio = cajonera_basica.calcular_precio()

        # 300 + (3 * 20) = 360
        assert precio == 360

    def test_calcular_precio_con_ruedas(self, cajonera_con_ruedas):
        precio = cajonera_con_ruedas.calcular_precio()

        # 400 + (5 * 20) + 30 = 530
        assert precio == 530

    def test_obtener_descripcion(self, cajonera_con_ruedas):
        descripcion = cajonera_con_ruedas.obtener_descripcion()

        assert "Cajonera 'Cajonera con Ruedas'" in descripcion
        assert "Material=Metal" in descripcion
        assert "Color=Gris" in descripcion
        assert "Cajones=5" in descripcion
        assert "Ruedas=Sí" in descripcion
        assert "Precio base=$400" in descripcion

    def test_precio_base_none_se_convierte_en_cero(self):
        cajonera = Cajonera(
            nombre="Cajonera Sin Base",
            material="Madera",
            color="Negro",
            precio_base=None,
            num_cajones=2,
            tiene_ruedas=False,
        )

        assert cajonera.precio_base == 0
        assert cajonera.calcular_precio() == 40

    def test_valores_cero(self):
        cajonera = Cajonera(
            nombre="Cajonera Simple",
            material="Metal",
            color="Negro",
            precio_base=0,
            num_cajones=0,
            tiene_ruedas=False,
        )

        assert cajonera.calcular_precio() == 0