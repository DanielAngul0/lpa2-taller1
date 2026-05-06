import pytest
from src.models.categorias.superficies import Superficie


class SuperficiePrueba(Superficie):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_tamaño(), 2)

    def obtener_descripcion(self) -> str:
        return (
            f"Superficie de prueba: {self.nombre}, "
            f"{self.obtener_info_superficie()}, "
            f"Precio: {self.calcular_precio()}"
        )


class TestSuperficie:
    @pytest.fixture
    def superficie_basica(self):
        return SuperficiePrueba(
            nombre="Superficie Base",
            material="Madera",
            color="Café",
            precio_base=200.0,
            largo=100.0,
            ancho=50.0,
            altura=75.0,
        )

    @pytest.fixture
    def superficie_pequena(self):
        return SuperficiePrueba(
            nombre="Superficie Pequeña",
            material="Metal",
            color="Negro",
            precio_base=100.0,
            largo=20.0,
            ancho=10.0,
            altura=50.0,
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Superficie(
                nombre="Mesa",
                material="Madera",
                color="Café",
                precio_base=100.0,
                largo=100.0,
                ancho=50.0,
                altura=75.0,
            )

    def test_instanciacion_correcta(self, superficie_basica):
        assert superficie_basica.nombre == "Superficie Base"
        assert superficie_basica.material == "Madera"
        assert superficie_basica.color == "Café"
        assert superficie_basica.precio_base == 200.0
        assert superficie_basica.largo == 100.0
        assert superficie_basica.ancho == 50.0
        assert superficie_basica.altura == 75.0

    def test_calcular_area(self, superficie_basica):
        area = superficie_basica.calcular_area()
        assert area == 5000.0

    def test_calcular_factor_tamano(self, superficie_basica):
        factor = superficie_basica.calcular_factor_tamaño()

        # área = 100 * 50 = 5000
        # factor = 1.0 + (5000 / 10000) * 0.05 = 1.025
        assert factor == pytest.approx(1.025)

    def test_obtener_info_superficie(self, superficie_basica):
        info = superficie_basica.obtener_info_superficie()
        assert "100.0x50.0x75.0cm" in info
        assert "Área: 5000.0cm²" in info

    def test_calcular_precio(self, superficie_basica):
        precio = superficie_basica.calcular_precio()
        # 200.0 * 1.025 = 205.0
        assert precio == pytest.approx(205.0)

    def test_obtener_descripcion(self, superficie_basica):
        descripcion = superficie_basica.obtener_descripcion()
        assert "Superficie de prueba" in descripcion
        assert "Superficie Base" in descripcion
        assert "Área: 5000.0cm²" in descripcion

    def test_setter_largo_valido(self, superficie_basica):
        superficie_basica.largo = 120.0
        assert superficie_basica.largo == 120.0

    def test_setter_largo_invalido(self, superficie_basica):
        with pytest.raises(ValueError, match="El largo debe ser mayor a 0"):
            superficie_basica.largo = 0

    def test_setter_ancho_valido(self, superficie_basica):
        superficie_basica.ancho = 60.0
        assert superficie_basica.ancho == 60.0

    def test_setter_ancho_invalido(self, superficie_basica):
        with pytest.raises(ValueError, match="El ancho debe ser mayor a 0"):
            superficie_basica.ancho = -1

    def test_setter_altura_valido(self, superficie_basica):
        superficie_basica.altura = 80.0
        assert superficie_basica.altura == 80.0

    def test_setter_altura_invalido(self, superficie_basica):
        with pytest.raises(ValueError, match="La altura debe ser mayor a 0"):
            superficie_basica.altura = 0