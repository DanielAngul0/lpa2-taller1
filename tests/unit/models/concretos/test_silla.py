import pytest
from src.models.concretos.silla import Silla

class TestSilla:
    @pytest.fixture
    def silla_basica(self):
        return Silla(
            nombre = "Silla Básica",
            material = "Madera",
            color = "Café",
            precio_base= 50.0,
            tiene_respaldo = True,
            material_tapizado = None,
            altura_regulable = False,
            tiene_ruedas = False,
        )
        
    def test_instanciacion_correcta(self, silla_basica):
        # Verificar herencia de atributos
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.color == "Café"
        assert silla_basica.precio_base == 50.0
        assert silla_basica.capacidad_personas == 1
        assert silla_basica.tiene_respaldo is True
        assert silla_basica.material_tapizado is None
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False
    
    def test_calcular_precio(self, silla_basica):
        # Probar polimorfismo
        precio = silla_basica.calcular_precio()
        
        # precio_base = 50.0
        # respaldo = True -> factor comodidad = 1.1
        # 50.0 * 1.1 = 55.0
        precio_esperado = 55.0
        
        assert precio == precio_esperado
    
    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()
        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion