import pytest
from src.models.categorias.almacenamiento import Almacenamiento


class CajoneraPrueba(Almacenamiento):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_almacenamiento(), 2)

    def obtener_descripcion(self) -> str:
        return (
            f"Cajonera de prueba: {self.nombre}, "
            f"{self.obtener_info_almacenamiento()}, "
            f"Precio: {self.calcular_precio()}"
        )


class TestAlmacenamiento:
    @pytest.fixture
    def almacenamiento_basico(self):
        return CajoneraPrueba(
            nombre="Cajonera Base",
            material="Madera",
            color="Café",
            precio_base=100.0,
            num_compartimentos=4,
            capacidad_litros=250.0,
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Almacenamiento(
                nombre="Armario",
                material="Madera",
                color="Blanco",
                precio_base=300.0,
                num_compartimentos=3,
                capacidad_litros=150.0,
            )

    def test_instanciacion_correcta(self, almacenamiento_basico):
        assert almacenamiento_basico.nombre == "Cajonera Base"
        assert almacenamiento_basico.material == "Madera"
        assert almacenamiento_basico.color == "Café"
        assert almacenamiento_basico.precio_base == 100.0
        assert almacenamiento_basico.num_compartimentos == 4
        assert almacenamiento_basico.capacidad_litros == 250.0

    def test_calcular_factor_almacenamiento(self, almacenamiento_basico):
        factor = almacenamiento_basico.calcular_factor_almacenamiento()

        # factor = 1.0 + (4 - 1) * 0.05 + (250 / 100) * 0.02
        # factor = 1.0 + 0.15 + 0.05 = 1.20
        assert factor == 1.2

    def test_obtener_info_almacenamiento(self, almacenamiento_basico):
        info = almacenamiento_basico.obtener_info_almacenamiento()
        assert "Compartimentos: 4" in info
        assert "Capacidad: 250.0L" in info

    def test_calcular_precio(self, almacenamiento_basico):
        precio = almacenamiento_basico.calcular_precio()

        # precio_base = 100.0
        # factor = 1.2
        # 100.0 * 1.2 = 120.0
        assert precio == 120.0

    def test_obtener_descripcion(self, almacenamiento_basico):
        descripcion = almacenamiento_basico.obtener_descripcion()
        assert "Cajonera de prueba" in descripcion
        assert "Cajonera Base" in descripcion
        assert "Compartimentos: 4" in descripcion
        assert "Capacidad: 250.0L" in descripcion

    def test_setter_num_compartimentos_valido(self, almacenamiento_basico):
        almacenamiento_basico.num_compartimentos = 5
        assert almacenamiento_basico.num_compartimentos == 5

    def test_setter_num_compartimentos_invalido(self, almacenamiento_basico):
        with pytest.raises(ValueError, match="El número de compartimentos debe ser mayor a 0"):
            almacenamiento_basico.num_compartimentos = 0

    def test_setter_capacidad_litros_valido(self, almacenamiento_basico):
        almacenamiento_basico.capacidad_litros = 300.0
        assert almacenamiento_basico.capacidad_litros == 300.0

    def test_setter_capacidad_litros_invalido(self, almacenamiento_basico):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            almacenamiento_basico.capacidad_litros = -10