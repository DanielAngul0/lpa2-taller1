import pytest
from src.models.concretos.sillon import Sillon


class TestSillon:
    @pytest.fixture
    def sillon_basico(self):
        return Sillon(
            nombre="Sillón Básico",
            material="Tela",
            color="Gris",
            precio_base=1000,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=True,
            es_reclinable=False,
            tiene_reposapiés=False,
        )

    @pytest.fixture
    def sillon_completo(self):
        return Sillon(
            nombre="Sillón Completo",
            material="Cuero",
            color="Negro",
            precio_base=1500,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            tiene_brazos=True,
            es_reclinable=True,
            tiene_reposapiés=True,
        )

    def test_instanciacion_correcta(self, sillon_basico):
        assert sillon_basico.nombre == "Sillón Básico"
        assert sillon_basico.material == "Tela"
        assert sillon_basico.color == "Gris"
        assert sillon_basico.precio_base == 1000
        assert sillon_basico.capacidad_personas == 2
        assert sillon_basico.tiene_respaldo is True
        assert sillon_basico.material_tapizado is None
        assert sillon_basico.tiene_brazos is True
        assert sillon_basico.es_reclinable is False
        assert sillon_basico.tiene_reposapiés is False

    def test_calcular_precio_sin_recargos(self):
        sillon = Sillon(
            nombre="Sillón Simple",
            material="Tela",
            color="Azul",
            precio_base=900,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=False,
            es_reclinable=False,
            tiene_reposapiés=False,
        )

        assert sillon.calcular_precio() == 900

    def test_calcular_precio_con_todos_los_recargos(self, sillon_completo):
        precio = sillon_completo.calcular_precio()

        # 1500 + 200 + 100 + 250 + 80 = 2130
        assert precio == 2130

    def test_calcular_precio_con_recargos_parciales(self):
        sillon = Sillon(
            nombre="Sillón Parcial",
            material="Tela",
            color="Verde",
            precio_base=1000,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=False,
            es_reclinable=True,
            tiene_reposapiés=True,
        )

        # 1000 + 250 + 80 = 1330
        assert sillon.calcular_precio() == 1330

    def test_obtener_descripcion(self, sillon_completo):
        descripcion = sillon_completo.obtener_descripcion()

        assert "Sillón 'Sillón Completo'" in descripcion
        assert "Material=Cuero" in descripcion
        assert "Color=Negro" in descripcion
        assert "Capacidad=3 personas" in descripcion
        assert "Tapizado=Cuero" in descripcion
        assert "Brazos=Sí" in descripcion
        assert "Reclinable=Sí" in descripcion
        assert "Reposapiés=Sí" in descripcion
        assert "Precio base=$1500" in descripcion

    def test_obtener_descripcion_sin_tapizado(self):
        sillon = Sillon(
            nombre="Sillón Sin Tapizado",
            material="Tela",
            color="Beige",
            precio_base=700,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=True,
            es_reclinable=False,
            tiene_reposapiés=False,
        )

        descripcion = sillon.obtener_descripcion()
        assert "Tapizado=N/A" in descripcion

    def test_precio_base_none_se_convierte_en_cero(self):
        sillon = Sillon(
            nombre="Sillón Sin Base",
            material="Madera",
            color="Gris",
            precio_base=None,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado="Tela",
            tiene_brazos=False,
            es_reclinable=False,
            tiene_reposapiés=False,
        )

        assert sillon.precio_base == 0
        assert sillon.calcular_precio() == 200