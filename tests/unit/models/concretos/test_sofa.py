import pytest
from src.models.concretos.sofa import Sofa


class TestSofa:
    @pytest.fixture
    def sofa_basico(self):
        return Sofa(
            nombre="Sofá Básico",
            material="Tela",
            color="Gris",
            precio_base=1000.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=True,
            es_modular=False,
            incluye_cojines=False,
        )

    @pytest.fixture
    def sofa_completo(self):
        return Sofa(
            nombre="Sofá Completo",
            material="Cuero",
            color="Negro",
            precio_base=1500.0,
            capacidad_personas=4,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            tiene_brazos=True,
            es_modular=True,
            incluye_cojines=True,
        )

    def test_instanciacion_correcta(self, sofa_basico):
        assert sofa_basico.nombre == "Sofá Básico"
        assert sofa_basico.material == "Tela"
        assert sofa_basico.color == "Gris"
        assert sofa_basico.precio_base == 1000.0
        assert sofa_basico.capacidad_personas == 3
        assert sofa_basico.tiene_respaldo is True
        assert sofa_basico.material_tapizado is None
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False

    def test_propiedades_de_solo_lectura(self, sofa_basico):
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False

    def test_calcular_precio_sin_recargos_adicionales(self, sofa_basico, monkeypatch):
        monkeypatch.setattr(Sofa, "calcular_factor_comodidad", lambda self: 1.0)

        precio = sofa_basico.calcular_precio()

        # 1000 * 1.0 + 150 por brazos = 1150
        assert precio == 1150

    def test_calcular_precio_con_todos_los_recargos(self, sofa_completo, monkeypatch):
        monkeypatch.setattr(Sofa, "calcular_factor_comodidad", lambda self: 1.0)

        precio = sofa_completo.calcular_precio()

        # 1500 * 1.0 + 150 brazos + 200 modular + 50 cojines = 1900
        assert precio == 1900

    def test_calcular_precio_con_factor_comodidad(self, sofa_basico, monkeypatch):
        monkeypatch.setattr(Sofa, "calcular_factor_comodidad", lambda self: 1.2)

        precio = sofa_basico.calcular_precio()

        # 1000 * 1.2 + 150 = 1350
        assert precio == 1350

    def test_obtener_descripcion(self, sofa_completo, monkeypatch):
        monkeypatch.setattr(Sofa, "calcular_factor_comodidad", lambda self: 1.0)

        descripcion = sofa_completo.obtener_descripcion()

        assert "Sofá: Sofá Completo" in descripcion
        assert "Material: Cuero" in descripcion
        assert "Color: Negro" in descripcion
        assert "Brazos: Sí" in descripcion
        assert "Modular: Sí" in descripcion
        assert "Incluye cojines: Sí" in descripcion
        assert "Precio final: $1900" in descripcion

    def test_obtener_descripcion_sin_extras(self, monkeypatch):
        sofa = Sofa(
            nombre="Sofá Simple",
            material="Tela",
            color="Beige",
            precio_base=900.0,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado=None,
            tiene_brazos=False,
            es_modular=False,
            incluye_cojines=False,
        )

        monkeypatch.setattr(Sofa, "calcular_factor_comodidad", lambda self: 1.0)

        descripcion = sofa.obtener_descripcion()

        assert "Sofá: Sofá Simple" in descripcion
        assert "Brazos: No" in descripcion
        assert "Modular: No" in descripcion
        assert "Incluye cojines: No" in descripcion
        assert "Precio final: $900" in descripcion