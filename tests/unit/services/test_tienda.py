import pytest
from unittest.mock import Mock
from src.services.tienda import TiendaMuebles
from src.models.concretos.silla import Silla


class TestTienda:
    @pytest.fixture
    def tienda_vacia(self):
        return TiendaMuebles()

    @pytest.fixture
    def silla_mock(self):
        mock_silla = Mock(spec=Silla)
        mock_silla.nombre = "Silla Mock"
        mock_silla.calcular_precio.return_value = 75.0
        return mock_silla

    def test_agregar_mueble(self, tienda_vacia, silla_mock):
        mensaje = tienda_vacia.agregar_mueble(silla_mock)

        assert len(tienda_vacia._inventario) == 1
        assert tienda_vacia._inventario[0] == silla_mock
        assert "agregado exitosamente" in mensaje.lower()

    def test_agregar_mueble_none(self, tienda_vacia):
        resultado = tienda_vacia.agregar_mueble(None)
        assert resultado == "Error: El mueble no puede ser None"

    def test_realizar_venta_existente(self, tienda_vacia, silla_mock):
        tienda_vacia.agregar_mueble(silla_mock)

        resultado = tienda_vacia.realizar_venta(silla_mock, "Cliente Test")

        assert isinstance(resultado, dict)
        assert resultado["mueble"] == "Silla Mock"
        assert resultado["cliente"] == "Cliente Test"
        assert resultado["precio_original"] == 75.0
        assert resultado["precio_final"] == 75.0
        assert len(tienda_vacia._inventario) == 0
        assert len(tienda_vacia._ventas_realizadas) == 1

    def test_realizar_venta_inexistente(self, tienda_vacia, silla_mock):
        resultado = tienda_vacia.realizar_venta(silla_mock, "Cliente Test")
        assert resultado == {"error": "El mueble no está disponible en inventario"}