import pytest

from src.main import main, mostrar_estadisticas_iniciales


class FakeTienda:
    def __init__(self, nombre):
        self.nombre = nombre

    def obtener_estadisticas(self):
        return {
            "total_muebles": 17,
            "total_comedores": 2,
            "valor_inventario": 12345.67,
            "descuentos_activos": {"mesa": 15},
            "ventas_realizadas": 4,
            "total_muebles_vendidos": 8,
            "valor_total_ventas": 5432.1,
            "tipos_muebles": {"mesa": 3, "silla": 5},
        }


def test_mostrar_estadisticas_iniciales(capsys):
    tienda = FakeTienda("Tienda X")

    mostrar_estadisticas_iniciales(tienda)

    salida = capsys.readouterr().out
    assert "Estadísticas iniciales de la tienda" in salida
    assert "Total de muebles: 17" in salida
    assert "Total de comedores: 2" in salida
    assert "Valor del inventario" in salida
    assert "Ventas realizadas: 4" in salida
    assert "mesa: 3 unidades" in salida
    assert "silla: 5 unidades" in salida


def test_main_ejecuta_flujo_completo(monkeypatch, capsys):
    calls = {}

    class FakeTiendaMuebles:
        def __init__(self, nombre):
            self.nombre = nombre
            calls["tienda"] = self

        def obtener_estadisticas(self):
            return {
                "total_muebles": 10,
                "total_comedores": 1,
                "valor_inventario": 1000.0,
                "descuentos_activos": {},
                "ventas_realizadas": 0,
                "total_muebles_vendidos": 0,
                "valor_total_ventas": 0.0,
                "tipos_muebles": {},
            }

    def fake_cargar_catalogo_en_tienda(tienda):
        calls["catalogo_tienda"] = tienda
        return {
            "muebles_agregados": 17,
            "comedores_agregados": 2,
            "descuentos_aplicados": 3,
        }

    class FakeMenu:
        def __init__(self, tienda):
            calls["menu_tienda"] = tienda

        def ejecutar(self):
            calls["menu_ejecutado"] = True

    monkeypatch.setattr("src.main.TiendaMuebles", FakeTiendaMuebles)
    monkeypatch.setattr("src.main.cargar_catalogo_en_tienda", fake_cargar_catalogo_en_tienda)
    monkeypatch.setattr("src.main.MenuTienda", FakeMenu)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    main()

    salida = capsys.readouterr().out
    assert "Bienvenido a la Tienda de Muebles" in salida
    assert "Catálogo cargado con éxito" in salida
    assert "Muebles agregados: 17" in salida
    assert calls["menu_ejecutado"] is True
    assert calls["catalogo_tienda"] is calls["tienda"]
    assert calls["menu_tienda"] is calls["tienda"]


def test_main_maneja_keyboardinterrupt(monkeypatch, capsys):
    class FakeTiendaMuebles:
        def __init__(self, nombre):
            self.nombre = nombre

        def obtener_estadisticas(self):
            return {}

    def fake_cargar_catalogo_en_tienda(tienda):
        return {
            "muebles_agregados": 0,
            "comedores_agregados": 0,
            "descuentos_aplicados": 0,
        }

    class FakeMenu:
        def __init__(self, tienda):
            pass

        def ejecutar(self):
            raise KeyboardInterrupt

    monkeypatch.setattr("src.main.TiendaMuebles", FakeTiendaMuebles)
    monkeypatch.setattr("src.main.cargar_catalogo_en_tienda", fake_cargar_catalogo_en_tienda)
    monkeypatch.setattr("src.main.MenuTienda", FakeMenu)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    main()

    salida = capsys.readouterr().out
    assert "Programa interrumpido por el usuario" in salida
    assert "Programa finalizado" in salida