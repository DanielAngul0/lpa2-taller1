import pytest
from src.models.concretos.armario import Armario


class TestArmario:
    @pytest.fixture
    def armario_basico(self):
        return Armario(
            nombre="Armario Básico",
            material="Madera",
            color="Blanco",
            precio_base=500,
            num_puertas=2,
            num_cajones=3,
            tiene_espejos=False,
        )

    @pytest.fixture
    def armario_completo(self):
        return Armario(
            nombre="Armario Completo",
            material="MDF",
            color="Café",
            precio_base=800,
            num_puertas=4,
            num_cajones=2,
            tiene_espejos=True,
        )

    def test_instanciacion_correcta(self, armario_basico):
        assert armario_basico.nombre == "Armario Básico"
        assert armario_basico.material == "Madera"
        assert armario_basico.color == "Blanco"
        assert armario_basico.precio_base == 500
        assert armario_basico.num_puertas == 2
        assert armario_basico.num_cajones == 3
        assert armario_basico.tiene_espejos is False

    def test_calcular_precio_sin_espejos(self, armario_basico):
        precio = armario_basico.calcular_precio()

        # 500 + (2 * 50) + (3 * 30) = 690
        assert precio == 690

    def test_calcular_precio_con_espejos(self, armario_completo):
        precio = armario_completo.calcular_precio()

        # 800 + (4 * 50) + (2 * 30) + 100 = 1160
        assert precio == 1160

    def test_obtener_descripcion(self, armario_completo):
        descripcion = armario_completo.obtener_descripcion()

        assert "Armario 'Armario Completo'" in descripcion
        assert "Material=MDF" in descripcion
        assert "Color=Café" in descripcion
        assert "Puertas=4" in descripcion
        assert "Cajones=2" in descripcion
        assert "Espejos=Sí" in descripcion
        assert "Precio base=$800" in descripcion

    def test_precio_base_none_se_convierte_en_cero(self):
        armario = Armario(
            nombre="Armario Sin Base",
            material="Madera",
            color="Gris",
            precio_base=None,
            num_puertas=1,
            num_cajones=0,
            tiene_espejos=False,
        )

        assert armario.precio_base == 0
        assert armario.calcular_precio() == 50

    def test_valores_cero(self):
        armario = Armario(
            nombre="Armario Simple",
            material="Metal",
            color="Negro",
            precio_base=0,
            num_puertas=0,
            num_cajones=0,
            tiene_espejos=False,
        )

        assert armario.calcular_precio() == 0