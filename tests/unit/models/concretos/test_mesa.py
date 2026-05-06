import pytest
from src.models.concretos.mesa import Mesa


class TestMesa:
    @pytest.fixture
    def mesa_basica(self):
        return Mesa(
            nombre="Mesa Básica",
            material="Madera",
            color="Café",
            precio_base=200.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=4,
        )

    @pytest.fixture
    def mesa_completa(self):
        return Mesa(
            nombre="Mesa Completa",
            material="Vidrio",
            color="Negro",
            precio_base=300.0,
            forma="redonda",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=6,
        )

    def test_instanciacion_correcta(self, mesa_basica):
        assert mesa_basica.nombre == "Mesa Básica"
        assert mesa_basica.material == "Madera"
        assert mesa_basica.color == "Café"
        assert mesa_basica.precio_base == 200.0
        assert mesa_basica.forma == "rectangular"
        assert mesa_basica.largo == 120.0
        assert mesa_basica.ancho == 80.0
        assert mesa_basica.altura == 75.0
        assert mesa_basica.capacidad_personas == 4

    def test_calcular_area(self, mesa_basica):
        assert mesa_basica.calcular_area() == 9600.0

    def test_calcular_factor_tamano(self, mesa_basica):
        factor = mesa_basica.calcular_factor_tamaño()

        # área = 120 * 80 = 9600
        # factor = 1.0 + (9600 / 10000) * 0.05 = 1.048
        assert factor == pytest.approx(1.048)

    def test_calcular_precio_rectangular_sin_recargos(self, mesa_basica):
        precio = mesa_basica.calcular_precio()

        # 200.0 * 1.048 = 209.6
        assert precio == pytest.approx(209.6)

    def test_calcular_precio_redonda_con_recargo_forma(self, mesa_completa):
        precio = mesa_completa.calcular_precio()

        # 300.0 * 1.048 = 314.4
        # +50 por forma no rectangular
        # +50 por capacidad > 4
        assert precio == pytest.approx(414.4)

    def test_calcular_precio_capacidad_mayor_a_4(self):
        mesa = Mesa(
            nombre="Mesa Grande",
            material="Madera",
            color="Roble",
            precio_base=400.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=5,
        )

        # 400 * 1.048 = 419.2
        # +50 por capacidad > 4
        assert mesa.calcular_precio() == pytest.approx(469.2)

    def test_calcular_precio_capacidad_mayor_a_6(self):
        mesa = Mesa(
            nombre="Mesa Extra Grande",
            material="Madera",
            color="Roble",
            precio_base=500.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=7,
        )

        # 500 * 1.048 = 524.0
        # +100 por capacidad > 6
        assert mesa.calcular_precio() == pytest.approx(624.0)

    def test_obtener_descripcion(self, mesa_completa):
        descripcion = mesa_completa.obtener_descripcion()

        assert "Mesa: Mesa Completa" in descripcion
        assert "Material: Vidrio" in descripcion
        assert "Color: Negro" in descripcion
        assert "Forma: redonda" in descripcion
        assert "Dimensiones: 120.0x80.0x75.0cm" in descripcion
        assert "Capacidad: 6 personas" in descripcion

    def test_setter_forma_valido(self, mesa_basica):
        mesa_basica.forma = "ovalada"
        assert mesa_basica.forma == "ovalada"

    def test_setter_forma_invalido(self, mesa_basica):
        with pytest.raises(ValueError, match="Forma debe ser una de"):
            mesa_basica.forma = "hexagonal"

    def test_setter_capacidad_personas_valido(self, mesa_basica):
        mesa_basica.capacidad_personas = 8
        assert mesa_basica.capacidad_personas == 8

    def test_setter_capacidad_personas_invalido(self, mesa_basica):
        with pytest.raises(ValueError, match="La capacidad debe ser mayor a 0"):
            mesa_basica.capacidad_personas = 0

    def test_setter_largo_valido(self, mesa_basica):
        mesa_basica.largo = 150.0
        assert mesa_basica.largo == 150.0

    def test_setter_ancho_valido(self, mesa_basica):
        mesa_basica.ancho = 100.0
        assert mesa_basica.ancho == 100.0

    def test_setter_altura_valido(self, mesa_basica):
        mesa_basica.altura = 80.0
        assert mesa_basica.altura == 80.0