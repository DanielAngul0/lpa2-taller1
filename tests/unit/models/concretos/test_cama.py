import pytest
from src.models.concretos.cama import Cama


class TestCama:
    @pytest.fixture
    def cama_basica(self):
        return Cama(
            nombre="Cama Básica",
            material="Madera",
            color="Blanco",
            precio_base=500.0,
            tamaño="individual",
            incluye_colchon=False,
            tiene_cabecera=False,
        )

    @pytest.fixture
    def cama_completa(self):
        return Cama(
            nombre="Cama Completa",
            material="Madera",
            color="Nogal",
            precio_base=700.0,
            tamaño="king",
            incluye_colchon=True,
            tiene_cabecera=True,
        )

    def test_instanciacion_correcta(self, cama_basica):
        assert cama_basica.nombre == "Cama Básica"
        assert cama_basica.material == "Madera"
        assert cama_basica.color == "Blanco"
        assert cama_basica.precio_base == 500.0
        assert cama_basica.tamaño == "individual"
        assert cama_basica.incluye_colchon is False
        assert cama_basica.tiene_cabecera is False

    def test_calcular_precio_individual_sin_extras(self, cama_basica):
        precio = cama_basica.calcular_precio()
        assert precio == 500.0

    def test_calcular_precio_matrimonial_con_extras(self):
        cama = Cama(
            nombre="Cama Matrimonial",
            material="Madera",
            color="Café",
            precio_base=500.0,
            tamaño="matrimonial",
            incluye_colchon=True,
            tiene_cabecera=True,
        )

        # 500 + 200 + 300 + 100 = 1100
        assert cama.calcular_precio() == 1100.0

    def test_calcular_precio_queen_con_extras(self):
        cama = Cama(
            nombre="Cama Queen",
            material="Metal",
            color="Negro",
            precio_base=600.0,
            tamaño="queen",
            incluye_colchon=True,
            tiene_cabecera=False,
        )

        # 600 + 400 + 300 = 1300
        assert cama.calcular_precio() == 1300.0

    def test_calcular_precio_king_con_extras(self, cama_completa):
        precio = cama_completa.calcular_precio()

        # 700 + 600 + 300 + 100 = 1700
        assert precio == 1700.0

    def test_obtener_descripcion(self, cama_completa):
        descripcion = cama_completa.obtener_descripcion()

        assert "Cama: Cama Completa" in descripcion
        assert "Material: Madera" in descripcion
        assert "Color: Nogal" in descripcion
        assert "Tamaño: king" in descripcion
        assert "Incluye colchón: Sí" in descripcion
        assert "Cabecera: Sí" in descripcion
        assert "Precio final: $1700.0" in descripcion

    def test_setter_tamano_valido(self, cama_basica):
        cama_basica.tamaño = "queen"
        assert cama_basica.tamaño == "queen"

    def test_setter_tamano_invalido(self, cama_basica):
        with pytest.raises(ValueError, match="Tamaño debe ser uno de"):
            cama_basica.tamaño = "gigante"