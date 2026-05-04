import pytest
from unittest.mock import Mock

from src.services.tienda import TiendaMuebles
from src.models.concretos.silla import Silla
from src.models.concretos.mesa import Mesa
from src.models.composicion.comedor import Comedor


class TestTienda:
    @pytest.fixture
    def tienda_vacia(self):
        return TiendaMuebles("Tienda de Prueba")

    @pytest.fixture
    def silla_madera(self):
        return Silla(
            nombre="Silla Madera",
            material="Madera",
            color="Café",
            precio_base=100.0,
            tiene_respaldo=True,
            material_tapizado="tela",
            altura_regulable=False,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def silla_metal(self):
        return Silla(
            nombre="Silla Metal",
            material="Metal",
            color="Negro",
            precio_base=90.0,
            tiene_respaldo=False,
            material_tapizado=None,
            altura_regulable=False,
            tiene_ruedas=False,
        )

    @pytest.fixture
    def mesa_roble(self):
        return Mesa(
            nombre="Mesa Roble",
            material="Madera",
            color="Terracota",
            precio_base=200.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=4,
        )

    @pytest.fixture
    def comedor_familiar(self, mesa_roble, silla_madera, silla_metal):
        return Comedor("Comedor Familiar", mesa_roble, [silla_madera, silla_metal])

    @pytest.fixture
    def tienda_con_catalogo(self, tienda_vacia, silla_madera, silla_metal, mesa_roble, comedor_familiar):
        tienda_vacia.agregar_mueble(silla_madera)
        tienda_vacia.agregar_mueble(silla_metal)
        tienda_vacia.agregar_mueble(mesa_roble)
        tienda_vacia.agregar_comedor(comedor_familiar)
        return tienda_vacia

    def test_agregar_mueble(self, tienda_vacia, silla_madera):
        mensaje = tienda_vacia.agregar_mueble(silla_madera)

        assert len(tienda_vacia._inventario) == 1
        assert tienda_vacia._inventario[0] == silla_madera
        assert "agregado exitosamente" in mensaje.lower()

    def test_agregar_mueble_none(self, tienda_vacia):
        resultado = tienda_vacia.agregar_mueble(None)
        assert resultado == "Error: El mueble no puede ser None"

    def test_agregar_mueble_con_precio_invalido(self, tienda_vacia):
        mueble_malo = Mock()
        mueble_malo.nombre = "Mueble Malo"
        mueble_malo.calcular_precio.return_value = 0

        resultado = tienda_vacia.agregar_mueble(mueble_malo)

        assert "precio válido mayor a 0" in resultado
        assert len(tienda_vacia._inventario) == 0

    def test_agregar_comedor(self, tienda_vacia, comedor_familiar):
        mensaje = tienda_vacia.agregar_comedor(comedor_familiar)

        assert len(tienda_vacia._comedores) == 1
        assert tienda_vacia._comedores[0] == comedor_familiar
        assert "agregado exitosamente" in mensaje.lower()

    def test_agregar_comedor_none(self, tienda_vacia):
        resultado = tienda_vacia.agregar_comedor(None)
        assert resultado == "Error: El comedor no puede ser None"

    def test_buscar_muebles_por_nombre_encontrado(self, tienda_con_catalogo):
        resultados = tienda_con_catalogo.buscar_muebles_por_nombre("silla")

        assert len(resultados) == 2
        assert all("silla" in mueble.nombre.lower() for mueble in resultados)

    def test_buscar_muebles_por_nombre_vacio(self, tienda_con_catalogo):
        assert tienda_con_catalogo.buscar_muebles_por_nombre("") == []
        assert tienda_con_catalogo.buscar_muebles_por_nombre("   ") == []

    def test_filtrar_por_precio(self, tienda_con_catalogo, silla_madera, mesa_roble):
        precio_min = silla_madera.calcular_precio() + 1
        precio_max = mesa_roble.calcular_precio() + 1

        resultados = tienda_con_catalogo.filtrar_por_precio(precio_min, precio_max)

        assert resultados == [mesa_roble]

    def test_filtrar_por_precio_con_error_en_un_mueble(self, tienda_vacia, silla_madera):
        mueble_malo = Mock()
        mueble_malo.nombre = "Mueble Malo"
        mueble_malo.calcular_precio.side_effect = Exception("boom")

        tienda_vacia._inventario.append(silla_madera)
        tienda_vacia._inventario.append(mueble_malo)

        resultados = tienda_vacia.filtrar_por_precio(0, 1000)

        assert silla_madera in resultados
        assert mueble_malo not in resultados

    def test_filtrar_por_material(self, tienda_con_catalogo, silla_madera, silla_metal, mesa_roble):
        resultados = tienda_con_catalogo.filtrar_por_material("madera")

        assert silla_madera in resultados
        assert mesa_roble in resultados
        assert silla_metal not in resultados

    def test_filtrar_por_material_vacio(self, tienda_con_catalogo):
        assert tienda_con_catalogo.filtrar_por_material("") == []
        assert tienda_con_catalogo.filtrar_por_material("   ") == []

    def test_aplicar_descuento_normaliza_categoria(self, tienda_vacia):
        mensaje = tienda_vacia.aplicar_descuento("sillas", 10)

        assert tienda_vacia._descuentos_activos == {"Silla": 0.1}
        assert "descuento del 10%" in mensaje.lower()
        assert "Silla" in mensaje

    def test_aplicar_descuento_invalido(self, tienda_vacia):
        assert tienda_vacia.aplicar_descuento("sillas", 0) == "Error: El porcentaje debe estar entre 1 y 100"
        assert tienda_vacia.aplicar_descuento("sillas", 150) == "Error: El porcentaje debe estar entre 1 y 100"

    def test_realizar_venta_existente_sin_descuento(self, tienda_vacia, silla_madera):
        tienda_vacia.agregar_mueble(silla_madera)

        resultado = tienda_vacia.realizar_venta(silla_madera, "Cliente Test")
        precio_esperado = round(silla_madera.calcular_precio(), 2)

        assert resultado["mueble"] == "Silla Madera"
        assert resultado["cliente"] == "Cliente Test"
        assert resultado["precio_original"] == precio_esperado
        assert resultado["precio_final"] == precio_esperado
        assert len(tienda_vacia._inventario) == 0
        assert len(tienda_vacia._ventas_realizadas) == 1
        assert tienda_vacia._total_muebles_vendidos == 1
        assert tienda_vacia._valor_total_ventas == precio_esperado

    def test_realizar_venta_existente_con_descuento(self, tienda_vacia, silla_madera):
        tienda_vacia.aplicar_descuento("sillas", 10)
        tienda_vacia.agregar_mueble(silla_madera)

        resultado = tienda_vacia.realizar_venta(silla_madera, "Cliente Descuento")
        precio_original = round(silla_madera.calcular_precio(), 2)
        precio_final_esperado = round(precio_original * 0.9, 2)

        assert resultado["mueble"] == "Silla Madera"
        assert resultado["descuento"] == 10.0
        assert resultado["precio_original"] == precio_original
        assert resultado["precio_final"] == precio_final_esperado

    def test_realizar_venta_inexistente(self, tienda_vacia, silla_madera):
        resultado = tienda_vacia.realizar_venta(silla_madera, "Cliente Test")
        assert resultado == {"error": "El mueble no está disponible en inventario"}

    def test_obtener_estadisticas_y_estadisticas(self, tienda_vacia, silla_madera, mesa_roble, comedor_familiar):
        tienda_vacia.agregar_mueble(silla_madera)
        tienda_vacia.agregar_mueble(mesa_roble)
        tienda_vacia.agregar_comedor(comedor_familiar)
        tienda_vacia.aplicar_descuento("sillas", 10)

        venta = tienda_vacia.realizar_venta(silla_madera, "Cliente 1")
        stats_1 = tienda_vacia.obtener_estadisticas()
        stats_2 = tienda_vacia.estadisticas()

        assert stats_1 == stats_2
        assert stats_1["total_muebles"] == 1
        assert stats_1["total_comedores"] == 1
        assert stats_1["ventas_realizadas"] == 1
        assert stats_1["total_muebles_vendidos"] == 1
        assert stats_1["descuentos_activos"] == {"Silla": 0.1}
        assert stats_1["tipos_muebles"] == {"Mesa": 1}
        assert stats_1["valor_total_ventas"] == venta["precio_final"]
        assert stats_1["valor_inventario"] == round(mesa_roble.calcular_precio(), 2)

    def test_generar_reporte_inventario(self, tienda_vacia, silla_madera, mesa_roble, comedor_familiar):
        tienda_vacia.agregar_mueble(silla_madera)
        tienda_vacia.agregar_mueble(mesa_roble)
        tienda_vacia.agregar_comedor(comedor_familiar)
        tienda_vacia.aplicar_descuento("sillas", 10)

        reporte = tienda_vacia.generar_reporte_inventario()

        assert "REPORTE DE INVENTARIO" in reporte
        assert "Total de muebles: 2" in reporte
        assert "Total de comedores: 1" in reporte
        assert "DISTRIBUCIÓN POR TIPOS:" in reporte
        assert "- Silla: 1 unidades" in reporte
        assert "- Mesa: 1 unidades" in reporte
        assert "DESCUENTOS ACTIVOS:" in reporte
        assert "- Silla: 10.0%" in reporte