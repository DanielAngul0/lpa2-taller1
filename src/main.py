#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Tienda de Muebles.
Inicializa la tienda, carga el catálogo de ejemplo y abre la interfaz.
"""

from src.services.tienda import TiendaMuebles
from src.services.catalogo import cargar_catalogo_en_tienda
from src.ui.menu import MenuTienda


def mostrar_estadisticas_iniciales(tienda: TiendaMuebles) -> None:
    """
    Muestra estadísticas iniciales de la tienda.
    """
    print("\n📊 Estadísticas iniciales de la tienda:")

    stats = tienda.obtener_estadisticas()
    print(f"  📦 Total de muebles: {stats.get('total_muebles', 0)}")
    print(f"  🍽️ Total de comedores: {stats.get('total_comedores', 0)}")
    print(f"  💰 Valor del inventario: ${stats.get('valor_inventario', 0):,.2f}")
    print(f"  🏷️ Descuentos activos: {stats.get('descuentos_activos', {})}")
    print(f"  🛒 Ventas realizadas: {stats.get('ventas_realizadas', 0)}")
    print(
        f"  📈 Total muebles vendidos (acumulado): {stats.get('total_muebles_vendidos', 0)}"
    )
    print(
        f"  💵 Valor total de ventas (acumulado): ${stats.get('valor_total_ventas', 0):,.2f}"
    )
    print("\n  📋 Distribución por tipos:")
    for tipo, cantidad in (stats.get("tipos_muebles", {}) or {}).items():
        print(f"    • {tipo}: {cantidad} unidades")


def main() -> None:
    """
    Función principal que inicializa y ejecuta la aplicación.
    """
    try:
        print("🏠 Bienvenido a la Tienda de Muebles - Taller OOP 🏠")
        print("=" * 50)

        tienda = TiendaMuebles("Mueblería Moderna OOP")
        print(f"🏪 Inicializando {tienda.nombre}...")

        resumen = cargar_catalogo_en_tienda(tienda)
        print("\n📦 Catálogo cargado con éxito:")
        print(f"  • Muebles agregados: {resumen['muebles_agregados']}")
        print(f"  • Comedores agregados: {resumen['comedores_agregados']}")
        print(f"  • Descuentos aplicados: {resumen['descuentos_aplicados']}")

        mostrar_estadisticas_iniciales(tienda)

        print("\n🎯 Iniciando interfaz de usuario...")
        menu = MenuTienda(tienda)

        input("\nPresiona Enter para iniciar el menú interactivo...")
        menu.ejecutar()

    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback

        traceback.print_exc()
    finally:
        print("\n" + "=" * 50)
        print("✨ Programa finalizado. ¡Gracias por usar la Tienda de Muebles! ✨")


if __name__ == "__main__":
    main()