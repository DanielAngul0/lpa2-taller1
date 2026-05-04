import pytest
from src.models.concretos.sofacama import SofaCama

class TestSofaCama:
    @pytest.fixture
    def sofa_cama_basico(self):
        return SofaCama(
            nombre = "Sofá Cama Moderno",
            material = "Tela",
            color = "Blanco",
            precio_base = 500.0,
            capacidad_personas = 3,
            material_tapizado = "tela",
            tamaño_cama = "queen",
            incluye_colchon = True,
            mecanismo_conversion = "plegable",
        )
    
    def test_herencia_multiple(self, sofa_cama_basico):
        assert sofa_cama_basico.nombre == "Sofá Cama Moderno"
        assert sofa_cama_basico.material == "Tela"
        assert sofa_cama_basico.color == "Blanco"
        assert sofa_cama_basico.precio_base == 500.0

        # Atributos heredados / compuestos
        assert sofa_cama_basico.capacidad_personas == 3
        assert sofa_cama_basico.tamaño_cama == "queen"
        assert sofa_cama_basico.incluye_colchon is True

        # Método específico de la clase
        assert hasattr(sofa_cama_basico, "convertir_a_cama")
        assert sofa_cama_basico.modo_actual == "sofa"

    def test_resolucion_metodos(self, sofa_cama_basico):
        precio = sofa_cama_basico.calcular_precio()

        # Cálculo esperado:
        # Sofa:
        # precio_base = 500.0
        # factor_comodidad = 1.0 + 0.1 (respaldo) + 0.1 (tela) + 0.1 (capacidad 3) = 1.3
        # 500.0 * 1.3 = 650.0
        # + 150 por brazos = 800.0
        #
        # SofaCama:
        # + 500 por tamaño queen = 1300.0
        # + 250 por colchón = 1550.0
        precio_esperado = 1550.0

        assert precio == precio_esperado
        
    def test_convertir_a_cama(self, sofa_cama_basico):
        resultado = sofa_cama_basico.convertir_a_cama()
        assert "convertido a cama" in resultado.lower()
        assert sofa_cama_basico.modo_actual == "cama"