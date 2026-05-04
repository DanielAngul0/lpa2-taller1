import pytest
from src.models.composicion.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla

class TestComedor:
    @pytest.fixture
    def comedor_basico(self):
        mesa = Mesa(
            nombre = "Mesa Comedor",
            material = "Roble",
            color = "Terracota",
            precio_base= 200.0,
            forma = "rectangular",
            largo = 120.0,
            ancho = 80.0,
            altura = 75.0,
            capacidad_personas = 4
        )
        sillas = [
            Silla(
                nombre = "Silla Comedor",
                material = "Roble",
                color = "Terracota",
                precio_base = 50.0,
                tiene_respaldo = True,
                material_tapizado = None,
                altura_regulable = False,
                tiene_ruedas = False,
                ) 
                for _ in range(6)
            ]
        
        return Comedor("Comedor Familiar", mesa, sillas)
    
    def test_composicion_correcta(self, comedor_basico):
        assert comedor_basico.mesa is not None
        assert len(comedor_basico.sillas) == 6
        assert isinstance(comedor_basico.mesa, Mesa)
        assert all(isinstance(silla, Silla) for silla in comedor_basico.sillas)
    
    def test_calcular_precio_total(self, comedor_basico):
        precio_total = comedor_basico.calcular_precio_total()

        # Mesa:
        # precio_base = 200.0
        # factor_tamaño ≈ 1.048 → 200 * 1.048 = 209.6
        precio_mesa = 209.6

        # Sillas:
        # precio_base = 50.0
        # factor_comodidad (respaldo=True) = 1.1 → 50 * 1.1 = 55.0
        precio_silla = 55.0
        total_sillas = 6 * precio_silla  # 330.0

        # Subtotal:
        # 209.6 + 330.0 = 539.6
        subtotal = precio_mesa + total_sillas

        # Descuento 5% por 6 sillas:
        # 539.6 * 0.95 = 512.62
        precio_esperado = round(subtotal * 0.95, 2)

        assert precio_total == precio_esperado
        
        