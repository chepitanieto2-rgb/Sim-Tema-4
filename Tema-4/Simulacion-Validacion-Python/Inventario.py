import math
import random

from RegistroInventario import RegistroInventario


class Inventario:

    def __init__(self):
        self.registros = []
        self.datosValidacion = []

    # =========================================================
    # SIMULACIÓN
    # =========================================================

    def simular(
            self,
            inventarioInicial,
            periodos,
            demandaMinima,
            demandaMaxima,
            puntoReorden,
            cantidadPedido
    ):

        # =====================================================
        # VALIDACIONES
        # =====================================================

        if (
                inventarioInicial < 0
                or periodos <= 0
                or demandaMinima < 0
                or demandaMaxima < 0
                or puntoReorden < 0
                or cantidadPedido <= 0
        ):
            raise ValueError(
                "Los valores ingresados no son válidos."
            )

        if demandaMinima > demandaMaxima:
            raise ValueError(
                "La demanda mínima no puede ser mayor "
                "que la demanda máxima."
            )

        # =====================================================
        # LIMPIAR DATOS ANTERIORES
        # =====================================================

        self.registros.clear()
        self.datosValidacion.clear()

        # =====================================================
        # VARIABLES DE LA SIMULACIÓN
        # =====================================================

        inventarioActual = inventarioInicial

        pedidosRealizados = 0
        faltanteTotal = 0

        sumaInventarios = 0.0

        inventarioMinimo = float("inf")

        # =====================================================
        # SIMULAR CADA PERÍODO
        # =====================================================

        for periodo in range(1, periodos + 1):

            inventarioInicioPeriodo = inventarioActual

            # -------------------------------------------------
            # GENERAR DEMANDA ALEATORIA
            # -------------------------------------------------

            demanda = self.generarEntero(
                demandaMinima,
                demandaMaxima
            )

            # -------------------------------------------------
            # CALCULAR UNIDADES ATENDIDAS
            # -------------------------------------------------

            unidadesAtendidas = min(
                inventarioInicioPeriodo,
                demanda
            )

            # -------------------------------------------------
            # CALCULAR FALTANTE
            # -------------------------------------------------

            faltante = max(
                0,
                demanda - inventarioInicioPeriodo
            )

            # -------------------------------------------------
            # INVENTARIO DESPUÉS DE LA DEMANDA
            # -------------------------------------------------

            inventarioDespuesDemanda = (
                inventarioInicioPeriodo
                - unidadesAtendidas
            )

            pedido = 0

            # -------------------------------------------------
            # PUNTO DE REORDEN
            # -------------------------------------------------
            #
            # Si el inventario llega o baja del punto
            # de reorden, se genera un pedido.
            # -------------------------------------------------

            if inventarioDespuesDemanda <= puntoReorden:

                pedido = cantidadPedido
                pedidosRealizados += 1

            # -------------------------------------------------
            # INVENTARIO FINAL
            # -------------------------------------------------
            #
            # Igual que en Java, suponemos que el pedido
            # se recibe al final del período.
            # -------------------------------------------------

            inventarioFinal = (
                inventarioDespuesDemanda
                + pedido
            )

            # -------------------------------------------------
            # ACUMULAR ESTADÍSTICAS
            # -------------------------------------------------

            faltanteTotal += faltante

            sumaInventarios += inventarioFinal

            inventarioMinimo = min(
                inventarioMinimo,
                inventarioFinal
            )

            # -------------------------------------------------
            # CREAR REGISTRO
            # -------------------------------------------------

            registro = RegistroInventario(
                periodo,
                inventarioInicioPeriodo,
                demanda,
                pedido,
                inventarioFinal,
                faltante
            )

            self.registros.append(registro)

            # Los inventarios finales son los datos
            # utilizados posteriormente para la prueba t.

            self.datosValidacion.append(
                float(inventarioFinal)
            )

            # El inventario final pasa a ser el inventario
            # inicial del siguiente período.

            inventarioActual = inventarioFinal

        # =====================================================
        # RESULTADOS GENERALES
        # =====================================================

        promedio = (
            sumaInventarios
            / periodos
        )

        estadoInventario = self.evaluarInventario(
            inventarioActual,
            puntoReorden,
            cantidadPedido
        )

        # =====================================================
        # DEVOLVER RESULTADOS A LA INTERFAZ
        # =====================================================

        return {
            "registros": self.registros,
            "inventarioPromedio": promedio,
            "inventarioMinimo": int(inventarioMinimo),
            "pedidosRealizados": pedidosRealizados,
            "faltanteTotal": faltanteTotal,
            "inventarioActual": inventarioActual,
            "estadoInventario": estadoInventario
        }

    # =========================================================
    # ESTADO DEL INVENTARIO
    # =========================================================

    def evaluarInventario(
            self,
            inventarioActual,
            puntoReorden,
            cantidadPedido
    ):

        # =====================================================
        # INVENTARIO CRÍTICO
        # =====================================================

        if inventarioActual <= 0:

            return (
                "🔴 INVENTARIO CRÍTICO\n"
                f"Inventario actual: {inventarioActual} unidades.\n"
                "Se requiere reabastecimiento."
            )

        # =====================================================
        # REORDEN RECOMENDADO
        # =====================================================

        elif inventarioActual <= puntoReorden:

            return (
                "🟠 REORDEN RECOMENDADO\n"
                f"Inventario actual: {inventarioActual} unidades.\n"
                f"Punto de reorden: {puntoReorden} unidades.\n"
                f"Pedido sugerido: {cantidadPedido} unidades.\n"
                "Es recomendable solicitar nueva mercancía."
            )

        # =====================================================
        # INVENTARIO SUFICIENTE
        # =====================================================

        else:

            return (
                "🟢 INVENTARIO SUFICIENTE\n"
                f"Inventario actual: {inventarioActual} unidades.\n"
                f"Punto de reorden: {puntoReorden} unidades.\n"
                "Por el momento no es necesario "
                "realizar otro pedido."
            )

    # =========================================================
    # VALIDACIÓN DE LA SIMULACIÓN
    # =========================================================

    def validarSimulacion(
            self,
            referencia,
            significancia
    ):

        # Igual que en Java:
        # necesitamos al menos 2 períodos.

        if len(self.datosValidacion) < 2:

            raise ValueError(
                "Primero debe ejecutar una simulación "
                "con al menos 2 períodos."
            )

        if significancia <= 0 or significancia >= 1:

            raise ValueError(
                "El nivel de significancia debe "
                "estar entre 0 y 1."
            )

        return self.ejecutarPruebaT(
            referencia,
            significancia
        )

    # =========================================================
    # PRUEBA T DE UNA MUESTRA
    # =========================================================

    def ejecutarPruebaT(
            self,
            referencia,
            significancia
    ):

        n = len(self.datosValidacion)

        # -----------------------------------------------------
        # PROMEDIO
        # -----------------------------------------------------

        suma = 0.0

        for dato in self.datosValidacion:
            suma += dato

        promedio = suma / n

        # -----------------------------------------------------
        # DESVIACIÓN ESTÁNDAR MUESTRAL
        # -----------------------------------------------------

        sumaCuadrados = 0.0

        for dato in self.datosValidacion:

            sumaCuadrados += math.pow(
                dato - promedio,
                2
            )

        desviacion = math.sqrt(
            sumaCuadrados / (n - 1)
        )

        # -----------------------------------------------------
        # SIN VARIABILIDAD
        # -----------------------------------------------------

        if desviacion == 0:

            return {
                "estadistico": "No calculable",
                "pValor": "No calculable",
                "valorEstadistico": None,
                "valorP": None,
                "promedio": promedio,
                "conclusion": (
                    "No es posible realizar la prueba t porque "
                    "los resultados no presentan variabilidad."
                )
            }

        # -----------------------------------------------------
        # ESTADÍSTICO t
        # -----------------------------------------------------

        t = (
            (promedio - referencia)
            /
            (desviacion / math.sqrt(n))
        )

        # -----------------------------------------------------
        # P-VALOR BILATERAL
        # -----------------------------------------------------
        #
        # IMPORTANTE:
        # El programa Java utiliza una aproximación normal
        # para calcular el p-valor. Conservamos exactamente
        # ese comportamiento.
        # -----------------------------------------------------

        pValor = (
            2.0
            *
            (
                1.0
                -
                self.normalCDF(
                    abs(t)
                )
            )
        )

        # =====================================================
        # CONCLUSIÓN
        # =====================================================

        if pValor < significancia:

            conclusion = (
                "El p-valor es menor que el nivel de "
                f"significancia ({significancia}). "
                "Existe evidencia estadística de que "
                "el inventario promedio simulado es diferente "
                "del valor de referencia de "
                f"{referencia:.2f} unidades."
            )

        else:

            conclusion = (
                "El p-valor es mayor o igual que el nivel de "
                f"significancia ({significancia}). "
                "No se encontró evidencia estadística "
                "suficiente para afirmar que el inventario "
                "promedio simulado sea diferente del valor "
                "de referencia de "
                f"{referencia:.2f} unidades."
            )

        return {
            "estadistico": f"{t:.4f}",
            "pValor": f"{pValor:.4f}",
            "valorEstadistico": t,
            "valorP": pValor,
            "promedio": promedio,
            "conclusion": conclusion
        }

    # =========================================================
    # DISTRIBUCIÓN NORMAL
    # =========================================================

    def normalCDF(self, x):

        return (
            0.5
            *
            (
                1.0
                +
                self.erf(
                    x / math.sqrt(2.0)
                )
            )
        )

    # =========================================================
    # FUNCIÓN DE ERROR
    # =========================================================

    def erf(self, x):

        # Aproximación numérica de erf.
        # Se conservan las mismas constantes de Java.

        signo = -1 if x < 0 else 1

        x = abs(x)

        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        t = (
            1.0
            /
            (1.0 + p * x)
        )

        y = (
            1.0
            -
            (
                (
                    (
                        (
                            (
                                a5 * t + a4
                            ) * t + a3
                        ) * t + a2
                    ) * t + a1
                )
                * t
                * math.exp(-x * x)
            )
        )

        return signo * y

    # =========================================================
    # NÚMERO ALEATORIO ENTERO
    # =========================================================

    def generarEntero(
            self,
            minimo,
            maximo
    ):

        # randint incluye ambos extremos.
        #
        # Por ejemplo:
        # generarEntero(5, 10)
        # puede producir 5, 6, 7, 8, 9 o 10.
        #
        # Esto equivale al nextInt utilizado en Java.

        return random.randint(
            minimo,
            maximo
        )