import pytest
from src.models.categorias.asientos import Asiento


class AsientoPrueba(Asiento):
    def calcular_precio(self) -> float:
        return round(self.precio_base * self.calcular_factor_comodidad(), 2)

    def obtener_descripcion(self) -> str:
        return (
            f"Asiento de prueba: {self.nombre}, "
            f"{self.obtener_info_asiento()}, "
            f"Precio: {self.calcular_precio()}"
        )


class TestAsiento:
    @pytest.fixture
    def asiento_basico(self):
        return AsientoPrueba(
            nombre="Asiento Base",
            material="Madera",
            color="Café",
            precio_base=100.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="cuero",
        )

    @pytest.fixture
    def asiento_simple(self):
        return AsientoPrueba(
            nombre="Asiento Simple",
            material="Metal",
            color="Negro",
            precio_base=80.0,
            capacidad_personas=1,
            tiene_respaldo=False,
            material_tapizado=None,
        )

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Asiento(
                nombre="Asiento",
                material="Madera",
                color="Café",
                precio_base=100.0,
                capacidad_personas=2,
                tiene_respaldo=True,
                material_tapizado="tela",
            )

    def test_instanciacion_correcta(self, asiento_basico):
        assert asiento_basico.nombre == "Asiento Base"
        assert asiento_basico.material == "Madera"
        assert asiento_basico.color == "Café"
        assert asiento_basico.precio_base == 100.0
        assert asiento_basico.capacidad_personas == 3
        assert asiento_basico.tiene_respaldo is True
        assert asiento_basico.material_tapizado == "cuero"

    def test_calcular_factor_comodidad_con_todo(self, asiento_basico):
        factor = asiento_basico.calcular_factor_comodidad()

        assert factor == pytest.approx(1.4)

    def test_calcular_factor_comodidad_simple(self, asiento_simple):
        factor = asiento_simple.calcular_factor_comodidad()

        assert factor == pytest.approx(1.0)

    def test_obtener_info_asiento_con_tapizado(self, asiento_basico):
        info = asiento_basico.obtener_info_asiento()
        assert "Capacidad: 3 personas" in info
        assert "Respaldo: Sí" in info
        assert "Tapizado: cuero" in info

    def test_obtener_info_asiento_sin_tapizado(self, asiento_simple):
        info = asiento_simple.obtener_info_asiento()
        assert "Capacidad: 1 personas" in info
        assert "Respaldo: No" in info
        assert "Tapizado" not in info

    def test_calcular_precio(self, asiento_basico):
        precio = asiento_basico.calcular_precio()
        assert precio == 140.0

    def test_obtener_descripcion(self, asiento_basico):
        descripcion = asiento_basico.obtener_descripcion()
        assert "Asiento de prueba" in descripcion
        assert "Asiento Base" in descripcion
        assert "Capacidad: 3 personas" in descripcion

    def test_setter_capacidad_personas_valido(self, asiento_basico):
        asiento_basico.capacidad_personas = 4
        assert asiento_basico.capacidad_personas == 4

    def test_setter_capacidad_personas_invalido(self, asiento_basico):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            asiento_basico.capacidad_personas = 0

    def test_setter_tiene_respaldo(self, asiento_basico):
        asiento_basico.tiene_respaldo = False
        assert asiento_basico.tiene_respaldo is False

    def test_setter_material_tapizado(self, asiento_basico):
        asiento_basico.material_tapizado = "tela"
        assert asiento_basico.material_tapizado == "tela"