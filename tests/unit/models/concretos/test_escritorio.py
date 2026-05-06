import pytest
from src.models.concretos.escritorio import Escritorio


class TestEscritorio:
    @pytest.fixture
    def escritorio_basico(self):
        return Escritorio(
            nombre="Escritorio Básico",
            material="Madera",
            color="Café",
            precio_base=400,
            forma="rectangular",
            tiene_cajones=False,
            num_cajones=0,
            largo=1.2,
            tiene_iluminacion=False,
        )

    @pytest.fixture
    def escritorio_completo(self):
        return Escritorio(
            nombre="Escritorio Gamer",
            material="Metal",
            color="Negro",
            precio_base=500,
            forma="L",
            tiene_cajones=True,
            num_cajones=4,
            largo=1.8,
            tiene_iluminacion=True,
        )

    def test_instanciacion_correcta(self, escritorio_basico):
        assert escritorio_basico.nombre == "Escritorio Básico"
        assert escritorio_basico.material == "Madera"
        assert escritorio_basico.color == "Café"
        assert escritorio_basico.precio_base == 400
        assert escritorio_basico.forma == "rectangular"
        assert escritorio_basico.tiene_cajones is False
        assert escritorio_basico.num_cajones == 0
        assert escritorio_basico.largo == 1.2
        assert escritorio_basico.tiene_iluminacion is False

    def test_calcular_precio_sin_extras(self, escritorio_basico):
        precio = escritorio_basico.calcular_precio()
        assert precio == 400

    def test_calcular_precio_con_todos_los_extras(self, escritorio_completo):
        precio = escritorio_completo.calcular_precio()

        # precio_base = 500
        # cajones: 4 * 25 = 100
        # largo > 1.5 = +50
        # iluminación = +40
        # forma distinta de rectangular = +30
        # total = 720
        assert precio == 720

    def test_calcular_precio_solo_forma_distinta(self):
        escritorio = Escritorio(
            nombre="Escritorio en L",
            material="Madera",
            color="Negro",
            precio_base=300,
            forma="L",
            tiene_cajones=False,
            num_cajones=0,
            largo=1.2,
            tiene_iluminacion=False,
        )

        assert escritorio.calcular_precio() == 330

    def test_calcular_precio_solo_cajones(self):
        escritorio = Escritorio(
            nombre="Escritorio con Cajones",
            material="Madera",
            color="Blanco",
            precio_base=200,
            forma="rectangular",
            tiene_cajones=True,
            num_cajones=3,
            largo=1.2,
            tiene_iluminacion=False,
        )

        # 200 + (3 * 25) = 275
        assert escritorio.calcular_precio() == 275

    def test_obtener_descripcion(self, escritorio_completo):
        descripcion = escritorio_completo.obtener_descripcion()

        assert "Escritorio 'Escritorio Gamer'" in descripcion
        assert "Material=Metal" in descripcion
        assert "Color=Negro" in descripcion
        assert "Forma=L" in descripcion
        assert "Cajones=4" in descripcion
        assert "Largo=1.8m" in descripcion
        assert "Iluminación=Sí" in descripcion
        assert "Precio base=$500" in descripcion

    def test_obtener_descripcion_sin_cajones(self, escritorio_basico):
        descripcion = escritorio_basico.obtener_descripcion()

        assert "Escritorio 'Escritorio Básico'" in descripcion
        assert "Cajones=0" in descripcion
        assert "Iluminación=No" in descripcion