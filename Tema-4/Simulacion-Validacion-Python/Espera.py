import math
import random

from Cliente import Cliente


class Espera:

    def __init__(self):
        self.clientes = []
        self.tiemposEspera = []

    # =========================================================
    # SIMULACIÓN
    # =========================================================

    def simular(
            self,
            cantidadClientes,
            cantidadServidores,
            llegadaMinima,
            llegadaMaxima,
            servicioMinimo,
            servicioMaximo
    ):

        # =====================================================
        # VALIDACIONES
        # =====================================================

        if cantidadClientes <= 0:
            raise ValueError(
                "El número de clientes debe ser mayor que 0."
            )

        if cantidadServidores <= 0:
            raise ValueError(
                "El número de servidores debe ser mayor que 0."
            )

        if llegadaMinima < 0 or llegadaMaxima <= llegadaMinima:
            raise ValueError(
                "Revise los tiempos de llegada."
            )

        if servicioMinimo < 0 or servicioMaximo <= servicioMinimo:
            raise ValueError(
                "Revise los tiempos de servicio."
            )

        # =====================================================
        # LIMPIAR DATOS ANTERIORES
        # =====================================================

        self.clientes.clear()
        self.tiemposEspera.clear()

        # Cada posición representa un servidor.
        #
        # servidoresDisponibles[0] = servidor 1
        # servidoresDisponibles[1] = servidor 2
        # servidoresDisponibles[2] = servidor 3

        servidoresDisponibles = [
            0.0 for _ in range(cantidadServidores)
        ]

        tiempoLlegada = 0.0
        sumaEspera = 0.0
        esperaMaxima = 0.0
        clientesEsperaron = 0
        sumaServicio = 0.0
        tiempoFinalSimulacion = 0.0

        # =====================================================
        # GENERACIÓN DE CLIENTES
        # =====================================================

        for i in range(1, cantidadClientes + 1):

            # -------------------------------------------------
            # TIEMPO ENTRE LLEGADAS
            # -------------------------------------------------

            intervaloLlegada = self.generarAleatorio(
                llegadaMinima,
                llegadaMaxima
            )

            tiempoLlegada += intervaloLlegada

            # -------------------------------------------------
            # TIEMPO DE SERVICIO
            # -------------------------------------------------

            tiempoServicio = self.generarAleatorio(
                servicioMinimo,
                servicioMaximo
            )

            # -------------------------------------------------
            # BUSCAR EL SERVIDOR DISPONIBLE PRIMERO
            # -------------------------------------------------

            indiceServidor = 0
            menorDisponibilidad = servidoresDisponibles[0]

            for j in range(1, cantidadServidores):

                if servidoresDisponibles[j] < menorDisponibilidad:

                    menorDisponibilidad = servidoresDisponibles[j]
                    indiceServidor = j

            # índice 0 -> servidor 1
            # índice 1 -> servidor 2
            # etc.

            numeroServidor = indiceServidor + 1

            # -------------------------------------------------
            # INICIO DEL SERVICIO
            # -------------------------------------------------

            inicioServicio = max(
                tiempoLlegada,
                menorDisponibilidad
            )

            # -------------------------------------------------
            # TIEMPO DE ESPERA
            # -------------------------------------------------

            espera = inicioServicio - tiempoLlegada

            # -------------------------------------------------
            # FIN DEL SERVICIO
            # -------------------------------------------------

            finServicio = inicioServicio + tiempoServicio

            # -------------------------------------------------
            # ACTUALIZAR SERVIDOR
            # -------------------------------------------------

            servidoresDisponibles[indiceServidor] = finServicio

            # -------------------------------------------------
            # ESTADÍSTICAS
            # -------------------------------------------------

            sumaEspera += espera
            sumaServicio += tiempoServicio

            tiempoFinalSimulacion = max(
                tiempoFinalSimulacion,
                finServicio
            )

            if espera > esperaMaxima:
                esperaMaxima = espera

            if espera > 0:
                clientesEsperaron += 1

            self.tiemposEspera.append(espera)

            # -------------------------------------------------
            # CREAR CLIENTE
            # -------------------------------------------------

            cliente = Cliente(
                i,
                numeroServidor,
                tiempoLlegada,
                tiempoServicio,
                espera,
                inicioServicio,
                finServicio
            )

            self.clientes.append(cliente)

        # =====================================================
        # RESULTADOS
        # =====================================================

        esperaPromedio = sumaEspera / cantidadClientes

        # Utilización promedio de los servidores:
        #
        # tiempo total de servicio /
        # (número de servidores * tiempo total)

        utilizacion = 0.0

        if tiempoFinalSimulacion > 0:

            utilizacion = (
                sumaServicio /
                (
                    cantidadServidores *
                    tiempoFinalSimulacion
                )
            ) * 100

        # La lógica devuelve los resultados.
        # La ventana será la encargada de mostrarlos.

        return {
            "clientes": self.clientes,
            "esperaPromedio": esperaPromedio,
            "esperaMaxima": esperaMaxima,
            "clientesEsperaron": clientesEsperaron,
            "utilizacion": utilizacion
        }

    # =========================================================
    # NÚMERO ALEATORIO
    # =========================================================

    def generarAleatorio(self, minimo, maximo):

        return minimo + (
            maximo - minimo
        ) * random.random()
        
    # =========================================================
    # VALIDACIÓN ESTADÍSTICA
    # =========================================================

    def validarSimulacion(
            self,
            referencia,
            significancia,
            tipoPrueba
    ):

        if not self.tiemposEspera:
            raise ValueError(
                "Primero debe ejecutar una simulación."
            )

        if significancia <= 0 or significancia >= 1:
            raise ValueError(
                "El nivel de significancia debe estar entre 0 y 1."
            )

        if not tipoPrueba:
            raise ValueError(
                "Seleccione un tipo de prueba."
            )

        # =====================================================
        # PRUEBA PARAMÉTRICA
        # =====================================================

        if tipoPrueba.startswith("Prueba paramétrica"):

            return self.ejecutarPruebaT(
                referencia,
                significancia
            )

        # =====================================================
        # PRUEBA NO PARAMÉTRICA
        # =====================================================

        if tipoPrueba.startswith("Prueba no paramétrica"):

            return self.ejecutarWilcoxon(
                referencia,
                significancia
            )

        raise ValueError(
            "El tipo de prueba seleccionado no es válido."
        )


    # =========================================================
    # PRUEBA T DE UNA MUESTRA
    # =========================================================

    def ejecutarPruebaT(
            self,
            referencia,
            significancia
    ):

        n = len(self.tiemposEspera)

        if n < 2:
            raise ValueError(
                "Se necesitan al menos 2 datos para realizar la prueba."
            )

        # -----------------------------------------------------
        # MEDIA
        # -----------------------------------------------------

        suma = 0.0

        for valor in self.tiemposEspera:
            suma += valor

        media = suma / n

        # -----------------------------------------------------
        # DESVIACIÓN ESTÁNDAR
        # -----------------------------------------------------

        sumaCuadrados = 0.0

        for valor in self.tiemposEspera:

            sumaCuadrados += math.pow(
                valor - media,
                2
            )

        varianza = sumaCuadrados / (n - 1)

        desviacion = math.sqrt(varianza)

        if desviacion == 0:
            raise ValueError(
                "La desviación estándar es 0. "
                "No se puede realizar la prueba t."
            )

        # -----------------------------------------------------
        # ESTADÍSTICO t
        # -----------------------------------------------------

        t = (
            (media - referencia)
            /
            (desviacion / math.sqrt(n))
        )

        gradosLibertad = n - 1

        # -----------------------------------------------------
        # P-VALOR BILATERAL
        # -----------------------------------------------------

        pValor = 2 * (
            1 -
            self.studentTCDF(
                abs(t),
                gradosLibertad
            )
        )

        # Evitar valores fuera del rango 0 - 1

        pValor = max(
            0,
            min(
                1,
                pValor
            )
        )

        # -----------------------------------------------------
        # CONCLUSIÓN
        # -----------------------------------------------------

        if pValor < significancia:

            conclusion = (
                "Se rechaza H0. La diferencia entre la media "
                "simulada y el valor de referencia es "
                "estadísticamente significativa."
            )

        else:

            conclusion = (
                "No se rechaza H0. No se encontró evidencia "
                "suficiente de una diferencia significativa "
                "respecto al valor de referencia."
            )

        return {
            "prueba": "t de Student",
            "estadistico": f"t = {t:.4f}",
            "pValor": f"p = {pValor:.4f}",
            "valorEstadistico": t,
            "valorP": pValor,
            "media": media,
            "gradosLibertad": gradosLibertad,
            "conclusion": conclusion
        }


    # =========================================================
    # PRUEBA NO PARAMÉTRICA DE WILCOXON
    # =========================================================

    def ejecutarWilcoxon(
            self,
            referencia,
            significancia
    ):

        diferencias = []

        # -----------------------------------------------------
        # CALCULAR DIFERENCIAS
        # -----------------------------------------------------

        for valor in self.tiemposEspera:

            diferencia = valor - referencia

            # Las diferencias iguales a cero
            # se eliminan de Wilcoxon.

            if abs(diferencia) > 0.0000001:
                diferencias.append(diferencia)

        n = len(diferencias)

        if n < 5:
            raise ValueError(
                "Para esta implementación de Wilcoxon "
                "se requieren al menos 5 diferencias "
                "distintas de cero."
            )

        # -----------------------------------------------------
        # VALORES ABSOLUTOS
        # -----------------------------------------------------

        absolutos = []

        for diferencia in diferencias:
            absolutos.append(
                abs(diferencia)
            )

        # Ordenamos los valores absolutos.

        ordenados = sorted(absolutos)

        # -----------------------------------------------------
        # SUMA DE RANGOS POSITIVOS
        # -----------------------------------------------------

        sumaRangosPositivos = 0.0

        for diferencia in diferencias:

            valorAbsoluto = abs(diferencia)

            sumaRangos = 0.0
            cantidadIguales = 0

            # -------------------------------------------------
            # RANGO PROMEDIO PARA EMPATES
            # -------------------------------------------------

            for i in range(len(ordenados)):

                if abs(
                    ordenados[i] - valorAbsoluto
                ) < 0.0000001:

                    sumaRangos += i + 1
                    cantidadIguales += 1

            rango = (
                sumaRangos /
                cantidadIguales
            )

            if diferencia > 0:
                sumaRangosPositivos += rango

        # -----------------------------------------------------
        # ESTADÍSTICO
        # -----------------------------------------------------

        mediaRangos = (
            n * (n + 1)
            /
            4.0
        )

        desviacionRangos = math.sqrt(
            n
            *
            (n + 1)
            *
            (2 * n + 1)
            /
            24.0
        )

        z = (
            sumaRangosPositivos -
            mediaRangos
        ) / desviacionRangos

        # -----------------------------------------------------
        # CORRECCIÓN DE CONTINUIDAD
        # -----------------------------------------------------

        if z > 0:

            z = (
                sumaRangosPositivos
                -
                mediaRangos
                -
                0.5
            ) / desviacionRangos

        elif z < 0:

            z = (
                sumaRangosPositivos
                -
                mediaRangos
                +
                0.5
            ) / desviacionRangos

        # -----------------------------------------------------
        # P-VALOR
        # -----------------------------------------------------

        pValor = 2 * (
            1 -
            self.normalCDF(
                abs(z)
            )
        )

        pValor = max(
            0,
            min(
                1,
                pValor
            )
        )

        # -----------------------------------------------------
        # CONCLUSIÓN
        # -----------------------------------------------------

        if pValor < significancia:

            conclusion = (
                "Se rechaza H0. La distribución de las esperas "
                "presenta una diferencia estadísticamente "
                "significativa respecto al valor de referencia."
            )

        else:

            conclusion = (
                "No se rechaza H0. No se encontró evidencia "
                "suficiente de una diferencia significativa "
                "respecto al valor de referencia."
            )

        return {
            "prueba": "Wilcoxon",
            "estadistico": (
                f"W+ = {sumaRangosPositivos:.4f} | "
                f"z = {z:.4f}"
            ),
            "pValor": f"p = {pValor:.4f}",
            "valorW": sumaRangosPositivos,
            "valorZ": z,
            "valorP": pValor,
            "conclusion": conclusion
        }


    # =========================================================
    # DISTRIBUCIÓN NORMAL
    # =========================================================

    def normalCDF(self, x):

        return 0.5 * (
            1 +
            self.erf(
                x / math.sqrt(2)
            )
        )


    # =========================================================
    # FUNCIÓN DE ERROR
    # =========================================================

    def erf(self, x):

        signo = 1 if x >= 0 else -1

        x = abs(x)

        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        t = (
            1.0 /
            (1.0 + p * x)
        )

        y = 1.0 - (
            (
                (
                    (
                        (
                            a5 * t
                            +
                            a4
                        ) * t
                        +
                        a3
                    ) * t
                    +
                    a2
                ) * t
                +
                a1
            ) * t
            *
            math.exp(
                -x * x
            )
        )

        return signo * y


    # =========================================================
    # DISTRIBUCIÓN t DE STUDENT
    # =========================================================

    def studentTCDF(
            self,
            t,
            gradosLibertad
    ):

        if t == 0:
            return 0.5

        x = (
            gradosLibertad
            /
            (
                gradosLibertad
                +
                t * t
            )
        )

        ibeta = self.regularizedBeta(
            x,
            gradosLibertad / 2.0,
            0.5
        )

        if t > 0:

            return (
                1 -
                0.5 * ibeta
            )

        else:

            return 0.5 * ibeta


    # =========================================================
    # BETA REGULARIZADA
    # =========================================================

    def regularizedBeta(
            self,
            x,
            a,
            b
    ):

        if x <= 0:
            return 0

        if x >= 1:
            return 1

        bt = math.exp(
            self.logGamma(a + b)
            -
            self.logGamma(a)
            -
            self.logGamma(b)
            +
            a * math.log(x)
            +
            b * math.log(1 - x)
        )

        if x < (
            (a + 1)
            /
            (a + b + 2)
        ):

            return (
                bt
                *
                self.betaFraction(
                    x,
                    a,
                    b
                )
                /
                a
            )

        else:

            return (
                1
                -
                bt
                *
                self.betaFraction(
                    1 - x,
                    b,
                    a
                )
                /
                b
            )


    # =========================================================
    # FRACCIÓN CONTINUA DE BETA
    # =========================================================

    def betaFraction(
            self,
            x,
            a,
            b
    ):

        maxIterations = 100

        epsilon = 3.0e-7

        qab = a + b
        qap = a + 1
        qam = a - 1

        c = 1.0

        d = (
            1
            -
            qab * x / qap
        )

        if abs(d) < 1e-30:
            d = 1e-30

        d = 1 / d

        h = d

        for m in range(
            1,
            maxIterations + 1
        ):

            m2 = 2 * m

            aa = (
                m
                *
                (b - m)
                *
                x
                /
                (
                    (qam + m2)
                    *
                    (a + m2)
                )
            )

            d = 1 + aa * d

            if abs(d) < 1e-30:
                d = 1e-30

            c = 1 + aa / c

            if abs(c) < 1e-30:
                c = 1e-30

            d = 1 / d

            h *= d * c

            aa = (
                -(
                    a + m
                )
                *
                (qab + m)
                *
                x
                /
                (
                    (a + m2)
                    *
                    (qap + m2)
                )
            )

            d = 1 + aa * d

            if abs(d) < 1e-30:
                d = 1e-30

            c = 1 + aa / c

            if abs(c) < 1e-30:
                c = 1e-30

            d = 1 / d

            delta = d * c

            h *= delta

            if abs(delta - 1) < epsilon:
                break

        return h


    # =========================================================
    # FUNCIÓN GAMMA
    # =========================================================

    def logGamma(self, x):

        coef = [
            76.18009172947146,
            -86.50532032941677,
            24.01409824083091,
            -1.231739572450155,
            0.001208650973866179,
            -0.000005395239384953
        ]

        y = x

        tmp = x + 5.5

        tmp -= (
            x + 0.5
        ) * math.log(tmp)

        ser = 1.000000000190015

        for c in coef:

            y += 1

            ser += c / y

        return (
            -tmp
            +
            math.log(
                2.5066282746310005
                *
                ser
                /
                x
            )
        )