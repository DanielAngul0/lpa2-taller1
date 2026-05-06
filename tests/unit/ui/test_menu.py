import pytest
from contextlib import nullcontext
from unittest.mock import Mock
from rich.table import Table

from src.ui.menu import MenuTienda


class DummyConsole:
    def __init__(self):
        self.print_calls = []
        self.clear_called = False
        self.status_messages = []

    def print(self, *args, **kwargs):
        self.print_calls.append((args, kwargs))

    def clear(self):
        self.clear_called = True

    def status(self, message):
        self.status_messages.append(message)
        return nullcontext()


class FakeMueble:
    def __init__(self, nombre="Mueble X", material="Madera", color="Café", precio=100):
        self.nombre = nombre
        self.material = material
        self.color = color
        self._precio = precio

    def calcular_precio(self):
        return self._precio

    def obtener_descripcion(self):
        return f"Descripción de {self.nombre}"


class FakeComedor:
    def __init__(self, descripcion="Descripción comedor"):
        self._descripcion = descripcion

    def obtener_descripcion_completa(self):
        return self._descripcion


class FakeTienda:
    def __init__(self):
        self.nombre = "Tienda Fake"
        self._inventario = []
        self._comedores = []
        self.buscar_muebles_por_nombre = Mock(return_value=[])
        self.filtrar_por_precio = Mock(return_value=[])
        self.filtrar_por_material = Mock(return_value=[])
        self.realizar_venta = Mock(return_value={})
        self.obtener_estadisticas = Mock(return_value={})
        self.generar_reporte_inventario = Mock(return_value="REPORTE")
        self.aplicar_descuento = Mock(return_value="Descuento aplicado exitosamente")


@pytest.fixture
def tienda():
    return FakeTienda()


@pytest.fixture
def menu(tienda):
    m = MenuTienda(tienda)
    m.console = DummyConsole()
    return m


class TestMenuTienda:
    def test_mostrar_catalogo_completo_sin_muebles(self, menu):
        menu.tienda._inventario = []

        menu.mostrar_catalogo_completo()

        assert len(menu.console.print_calls) == 1
        assert "No hay muebles en el inventario." in str(menu.console.print_calls[0][0][0])

    def test_mostrar_catalogo_completo_con_muebles(self, menu):
        menu.tienda._inventario = [FakeMueble(nombre="Silla 1", precio=150)]

        menu.mostrar_catalogo_completo()

        assert len(menu.console.print_calls) == 1
        printed = menu.console.print_calls[0][0][0]
        assert isinstance(printed, Table)
        assert printed.title == "📋 Catálogo de Muebles"

    def test_buscar_muebles_interactivo_con_resultados(self, menu, monkeypatch):
        menu.tienda.buscar_muebles_por_nombre = Mock(
            return_value=[FakeMueble(nombre="Mesa 1", precio=250)]
        )
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "Mesa")
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)
        menu._mostrar_lista_muebles = Mock()

        menu.buscar_muebles_interactivo()

        menu.tienda.buscar_muebles_por_nombre.assert_called_once_with("Mesa")
        menu._mostrar_lista_muebles.assert_called_once()
        assert len(menu._mostrar_lista_muebles.call_args.args[0]) == 1

    def test_buscar_muebles_interactivo_termino_vacio(self, menu, monkeypatch):
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "   ")

        menu.buscar_muebles_interactivo()

        assert any(
            "Término de búsqueda vacío." in str(args[0])
            for args, _ in menu.console.print_calls
        )

    def test_filtrar_por_precio_interactivo_rango_invalido(self, menu, monkeypatch):
        values = iter([100, 50])
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: next(values))
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)

        menu.filtrar_por_precio_interactivo()

        assert any(
            "El precio mínimo no puede ser mayor al máximo." in str(args[0])
            for args, _ in menu.console.print_calls
        )

    def test_filtrar_por_precio_interactivo_con_resultados(self, menu, monkeypatch):
        values = iter([0, 0])
        menu.tienda.filtrar_por_precio = Mock(
            return_value=[FakeMueble(nombre="Sofá 1", precio=1200)]
        )
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: next(values))
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)
        menu._mostrar_lista_muebles = Mock()

        menu.filtrar_por_precio_interactivo()

        menu.tienda.filtrar_por_precio.assert_called_once()
        menu._mostrar_lista_muebles.assert_called_once()

    def test_filtrar_por_material_interactivo_con_resultados(self, menu, monkeypatch):
        menu.tienda.filtrar_por_material = Mock(
            return_value=[FakeMueble(nombre="Mesa de madera", material="Madera")]
        )
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "Madera")
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)
        menu._mostrar_lista_muebles = Mock()

        menu.filtrar_por_material_interactivo()

        menu.tienda.filtrar_por_material.assert_called_once_with("Madera")
        menu._mostrar_lista_muebles.assert_called_once()

    def test_mostrar_comedores_sin_comedores(self, menu):
        menu.tienda._comedores = []

        menu.mostrar_comedores()

        assert any(
            "No hay comedores disponibles." in str(args[0])
            for args, _ in menu.console.print_calls
        )

    def test_mostrar_comedores_con_comedores(self, menu):
        menu.tienda._comedores = [FakeComedor("Comedor A"), FakeComedor("Comedor B")]

        menu.mostrar_comedores()

        assert len(menu.console.print_calls) == 2

    def test_realizar_venta_interactiva_sin_inventario(self, menu):
        menu.tienda._inventario = []

        menu.realizar_venta_interactiva()

        assert any(
            "No hay muebles disponibles para venta." in str(args[0])
            for args, _ in menu.console.print_calls
        )

    def test_realizar_venta_interactiva_cancelada(self, menu, monkeypatch):
        menu.tienda._inventario = [FakeMueble(nombre="Silla 1", precio=100)]
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: 1)
        monkeypatch.setattr("src.ui.menu.Confirm.ask", lambda *args, **kwargs: False)
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "Cliente X")
        menu.tienda.realizar_venta = Mock(return_value={})

        menu.realizar_venta_interactiva()

        assert any(
            "Venta cancelada." in str(args[0])
            for args, _ in menu.console.print_calls
        )

    def test_realizar_venta_interactiva_exitosa(self, menu, monkeypatch):
        mueble = FakeMueble(nombre="Mesa 1", precio=250)
        menu.tienda._inventario = [mueble]
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: 1)
        monkeypatch.setattr("src.ui.menu.Confirm.ask", lambda *args, **kwargs: True)
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "Cliente X")
        menu.tienda.realizar_venta = Mock(
            return_value={
                "cliente": "Cliente X",
                "mueble": "Mesa 1",
                "precio_original": 250.0,
                "descuento": 10.0,
                "precio_final": 225.0,
            }
        )
        menu._mostrar_comprobante_venta = Mock()

        menu.realizar_venta_interactiva()

        menu.tienda.realizar_venta.assert_called_once_with(mueble, "Cliente X")
        menu._mostrar_comprobante_venta.assert_called_once()

    def test_mostrar_estadisticas(self, menu, monkeypatch):
        menu.tienda.obtener_estadisticas = Mock(
            return_value={
                "total_muebles": 5,
                "total_comedores": 2,
                "valor_inventario": 1234.5,
                "ventas_realizadas": 3,
                "descuentos_activos": {"mesa": 15},
                "total_muebles_vendidos": 8,
                "valor_total_ventas": 900.0,
                "tipos_muebles": {"mesa": 2, "silla": 3},
            }
        )
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)

        menu.mostrar_estadisticas()

        assert len(menu.console.print_calls) >= 1

    def test_generar_reporte_interactivo_guarda_archivo(self, menu, monkeypatch, tmp_path):
        menu.tienda.generar_reporte_inventario = Mock(return_value="REPORTE DE PRUEBA")
        monkeypatch.setattr("src.ui.menu.time.sleep", lambda *_: None)
        monkeypatch.setattr("src.ui.menu.Confirm.ask", lambda *args, **kwargs: True)
        monkeypatch.setattr("src.ui.menu.Prompt.ask", lambda *args, **kwargs: "reporte.txt")
        monkeypatch.chdir(tmp_path)

        menu.generar_reporte_interactivo()

        archivo = tmp_path / "reporte.txt"
        assert archivo.exists()
        assert archivo.read_text(encoding="utf-8") == "REPORTE DE PRUEBA"

    def test_aplicar_descuentos_interactivo(self, menu, monkeypatch):
        values = iter([2, 25])
        menu.tienda.aplicar_descuento = Mock(return_value="Descuento aplicado exitosamente")
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: next(values))

        menu.aplicar_descuentos_interactivo()

        menu.tienda.aplicar_descuento.assert_called_once_with("mesa", 25)

    def test_mostrar_menu_principal_devuelve_opcion(self, menu, monkeypatch):
        monkeypatch.setattr("src.ui.menu.IntPrompt.ask", lambda *args, **kwargs: 3)

        opcion = menu.mostrar_menu_principal()

        assert opcion == 3

    def test_ejecutar_sale_con_opcion_cero(self, menu, monkeypatch):
        menu.mostrar_banner = Mock()
        menu.mostrar_menu_principal = Mock(return_value=0)
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

        menu.ejecutar()

        assert menu.running is False
        menu.mostrar_banner.assert_called_once()
        menu.mostrar_menu_principal.assert_called_once()

    def test_ejecutar_maneja_keyboardinterrupt(self, menu, monkeypatch):
        menu.mostrar_banner = Mock()
        menu.mostrar_menu_principal = Mock(side_effect=KeyboardInterrupt)
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

        menu.ejecutar()

        assert menu.running is False