# ============================================================
# Espera.R
# Lógica de simulación de líneas de espera
# ============================================================

library(R6)


Espera <- R6Class(
  "Espera",
  
  public = list(
    
    # ========================================================
    # ATRIBUTOS
    # ========================================================
    
    clientes = NULL,
    tiemposEspera = NULL,
    
    
    # ========================================================
    # CONSTRUCTOR
    # ========================================================
    
    initialize = function() {
      
      self$clientes <- list()
      self$tiemposEspera <- numeric(0)
      
    },
    
    
    # ========================================================
    # SIMULACIÓN
    # ========================================================
    
    simular = function(
    cantidadClientes,
    cantidadServidores,
    llegadaMinima,
    llegadaMaxima,
    servicioMinimo,
    servicioMaximo
    ) {
      
      # ------------------------------------------------------
      # VALIDACIONES
      # ------------------------------------------------------
      
      if (cantidadClientes <= 0) {
        stop(
          "El número de clientes debe ser mayor que 0."
        )
      }
      
      if (cantidadServidores <= 0) {
        stop(
          "El número de servidores debe ser mayor que 0."
        )
      }
      
      if (
        llegadaMinima < 0 ||
        llegadaMaxima <= llegadaMinima
      ) {
        stop(
          "Revise los tiempos de llegada."
        )
      }
      
      if (
        servicioMinimo < 0 ||
        servicioMaximo <= servicioMinimo
      ) {
        stop(
          "Revise los tiempos de servicio."
        )
      }
      
      
      # ------------------------------------------------------
      # LIMPIAR DATOS ANTERIORES
      # ------------------------------------------------------
      
      self$clientes <- list()
      self$tiemposEspera <- numeric(0)
      
      
      # Cada posición representa un servidor.
      servidoresDisponibles <- rep(
        0.0,
        cantidadServidores
      )
      
      
      tiempoLlegada <- 0.0
      sumaEspera <- 0.0
      esperaMaxima <- 0.0
      clientesEsperaron <- 0
      sumaServicio <- 0.0
      tiempoFinalSimulacion <- 0.0
      
      
      # ======================================================
      # GENERACIÓN DE CLIENTES
      # ======================================================
      
      for (i in seq_len(cantidadClientes)) {
        
        # ----------------------------------------------------
        # TIEMPO ENTRE LLEGADAS
        # ----------------------------------------------------
        
        intervaloLlegada <- self$generarAleatorio(
          llegadaMinima,
          llegadaMaxima
        )
        
        tiempoLlegada <-
          tiempoLlegada +
          intervaloLlegada
        
        
        # ----------------------------------------------------
        # TIEMPO DE SERVICIO
        # ----------------------------------------------------
        
        tiempoServicio <- self$generarAleatorio(
          servicioMinimo,
          servicioMaximo
        )
        
        
        # ----------------------------------------------------
        # BUSCAR EL SERVIDOR DISPONIBLE PRIMERO
        # ----------------------------------------------------
        
        indiceServidor <- 1
        
        menorDisponibilidad <-
          servidoresDisponibles[1]
        
        if (cantidadServidores > 1) {
          
          for (j in 2:cantidadServidores) {
            
            if (
              servidoresDisponibles[j] <
              menorDisponibilidad
            ) {
              
              menorDisponibilidad <-
                servidoresDisponibles[j]
              
              indiceServidor <- j
            }
          }
        }
        
        
        numeroServidor <- indiceServidor
        
        
        # ----------------------------------------------------
        # INICIO DEL SERVICIO
        # ----------------------------------------------------
        
        inicioServicio <- max(
          tiempoLlegada,
          menorDisponibilidad
        )
        
        
        # ----------------------------------------------------
        # TIEMPO DE ESPERA
        # ----------------------------------------------------
        
        espera <-
          inicioServicio -
          tiempoLlegada
        
        
        # ----------------------------------------------------
        # FIN DEL SERVICIO
        # ----------------------------------------------------
        
        finServicio <-
          inicioServicio +
          tiempoServicio
        
        
        # ----------------------------------------------------
        # ACTUALIZAR SERVIDOR
        # ----------------------------------------------------
        
        servidoresDisponibles[indiceServidor] <-
          finServicio
        
        
        # ----------------------------------------------------
        # ESTADÍSTICAS
        # ----------------------------------------------------
        
        sumaEspera <-
          sumaEspera +
          espera
        
        sumaServicio <-
          sumaServicio +
          tiempoServicio
        
        tiempoFinalSimulacion <- max(
          tiempoFinalSimulacion,
          finServicio
        )
        
        if (espera > esperaMaxima) {
          esperaMaxima <- espera
        }
        
        if (espera > 0) {
          clientesEsperaron <-
            clientesEsperaron + 1
        }
        
        
        # Guardar tiempo de espera
        
        self$tiemposEspera <- c(
          self$tiemposEspera,
          espera
        )
        
        
        # ----------------------------------------------------
        # CREAR CLIENTE
        # ----------------------------------------------------
        
        cliente <- Cliente$new(
          i,
          numeroServidor,
          tiempoLlegada,
          tiempoServicio,
          espera,
          inicioServicio,
          finServicio
        )
        
        self$clientes[[i]] <- cliente
      }
      
      
      # ======================================================
      # RESULTADOS
      # ======================================================
      
      esperaPromedio <-
        sumaEspera /
        cantidadClientes
      
      
      utilizacion <- 0.0
      
      if (tiempoFinalSimulacion > 0) {
        
        utilizacion <- (
          sumaServicio /
            (
              cantidadServidores *
                tiempoFinalSimulacion
            )
        ) * 100
      }
      
      
      return(
        list(
          clientes = self$clientes,
          esperaPromedio = esperaPromedio,
          esperaMaxima = esperaMaxima,
          clientesEsperaron = clientesEsperaron,
          utilizacion = utilizacion
        )
      )
      
    },
    
    
    # ========================================================
    # NÚMERO ALEATORIO
    # ========================================================
    
    generarAleatorio = function(
    minimo,
    maximo
    ) {
      
      return(
        minimo +
          (maximo - minimo) *
          runif(1)
      )
      
    },
    
    
    # ========================================================
    # VALIDACIÓN ESTADÍSTICA
    # ========================================================
    
    validarSimulacion = function(
    referencia,
    significancia,
    tipoPrueba
    ) {
      
      if (length(self$tiemposEspera) == 0) {
        
        stop(
          "Primero debe ejecutar una simulación."
        )
      }
      
      
      if (
        significancia <= 0 ||
        significancia >= 1
      ) {
        
        stop(
          paste(
            "El nivel de significancia debe",
            "estar entre 0 y 1."
          )
        )
      }
      
      
      if (
        is.null(tipoPrueba) ||
        length(tipoPrueba) == 0 ||
        tipoPrueba == ""
      ) {
        
        stop(
          "Seleccione un tipo de prueba."
        )
      }
      
      
      # ------------------------------------------------------
      # PRUEBA PARAMÉTRICA
      # ------------------------------------------------------
      
      if (
        startsWith(
          tipoPrueba,
          "Prueba paramétrica"
        )
      ) {
        
        return(
          self$ejecutarPruebaT(
            referencia,
            significancia
          )
        )
      }
      
      
      # ------------------------------------------------------
      # PRUEBA NO PARAMÉTRICA
      # ------------------------------------------------------
      
      if (
        startsWith(
          tipoPrueba,
          "Prueba no paramétrica"
        )
      ) {
        
        return(
          self$ejecutarWilcoxon(
            referencia,
            significancia
          )
        )
      }
      
      
      stop(
        "El tipo de prueba seleccionado no es válido."
      )
      
    },
    
    
    # ========================================================
    # PRUEBA T DE UNA MUESTRA
    # ========================================================
    
    ejecutarPruebaT = function(
    referencia,
    significancia
    ) {
      
      n <- length(
        self$tiemposEspera
      )
      
      
      if (n < 2) {
        
        stop(
          paste(
            "Se necesitan al menos 2 datos",
            "para realizar la prueba."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # MEDIA
      # ------------------------------------------------------
      
      suma <- 0.0
      
      for (valor in self$tiemposEspera) {
        
        suma <-
          suma +
          valor
      }
      
      media <-
        suma /
        n
      
      
      # ------------------------------------------------------
      # DESVIACIÓN ESTÁNDAR
      # ------------------------------------------------------
      
      sumaCuadrados <- 0.0
      
      for (valor in self$tiemposEspera) {
        
        sumaCuadrados <-
          sumaCuadrados +
          (valor - media)^2
      }
      
      
      varianza <-
        sumaCuadrados /
        (n - 1)
      
      
      desviacion <-
        sqrt(
          varianza
        )
      
      
      if (desviacion == 0) {
        
        stop(
          paste(
            "La desviación estándar es 0.",
            "No se puede realizar la prueba t."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # ESTADÍSTICO T
      # ------------------------------------------------------
      
      tEstadistico <- (
        media -
          referencia
      ) /
        (
          desviacion /
            sqrt(n)
        )
      
      
      gradosLibertad <- n - 1
      
      
      # ------------------------------------------------------
      # P-VALOR BILATERAL
      # ------------------------------------------------------
      
      pValor <- 2 * (
        1 -
          pt(
            abs(tEstadistico),
            df = gradosLibertad
          )
      )
      
      
      pValor <- max(
        0,
        min(
          1,
          pValor
        )
      )
      
      
      # ------------------------------------------------------
      # CONCLUSIÓN
      # ------------------------------------------------------
      
      if (pValor < significancia) {
        
        conclusion <- paste(
          "Se rechaza H0. La diferencia entre la media",
          "simulada y el valor de referencia es",
          "estadísticamente significativa."
        )
        
      } else {
        
        conclusion <- paste(
          "No se rechaza H0. No se encontró evidencia",
          "suficiente de una diferencia significativa",
          "respecto al valor de referencia."
        )
      }
      
      
      return(
        list(
          prueba = "t de Student",
          estadistico = sprintf(
            "t = %.4f",
            tEstadistico
          ),
          pValor = sprintf(
            "p = %.4f",
            pValor
          ),
          valorEstadistico = tEstadistico,
          valorP = pValor,
          media = media,
          gradosLibertad = gradosLibertad,
          conclusion = conclusion
        )
      )
      
    },
    
    
    # ========================================================
    # PRUEBA NO PARAMÉTRICA DE WILCOXON
    # ========================================================
    
    ejecutarWilcoxon = function(
    referencia,
    significancia
    ) {
      
      diferencias <- numeric(0)
      
      
      # ------------------------------------------------------
      # CALCULAR DIFERENCIAS
      # ------------------------------------------------------
      
      for (valor in self$tiemposEspera) {
        
        diferencia <-
          valor -
          referencia
        
        
        # Las diferencias iguales a cero se eliminan.
        
        if (
          abs(diferencia) >
          0.0000001
        ) {
          
          diferencias <- c(
            diferencias,
            diferencia
          )
        }
      }
      
      
      n <- length(
        diferencias
      )
      
      
      if (n < 5) {
        
        stop(
          paste(
            "Para esta implementación de Wilcoxon",
            "se requieren al menos 5 diferencias",
            "distintas de cero."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # VALORES ABSOLUTOS
      # ------------------------------------------------------
      
      absolutos <- numeric(0)
      
      for (diferencia in diferencias) {
        
        absolutos <- c(
          absolutos,
          abs(diferencia)
        )
      }
      
      
      ordenados <- sort(
        absolutos
      )
      
      
      # ------------------------------------------------------
      # SUMA DE RANGOS POSITIVOS
      # ------------------------------------------------------
      
      sumaRangosPositivos <- 0.0
      
      
      for (diferencia in diferencias) {
        
        valorAbsoluto <-
          abs(diferencia)
        
        sumaRangos <- 0.0
        
        cantidadIguales <- 0
        
        
        # ----------------------------------------------------
        # RANGO PROMEDIO PARA EMPATES
        # ----------------------------------------------------
        
        for (i in seq_along(ordenados)) {
          
          if (
            abs(
              ordenados[i] -
              valorAbsoluto
            ) <
            0.0000001
          ) {
            
            sumaRangos <-
              sumaRangos +
              i
            
            cantidadIguales <-
              cantidadIguales +
              1
          }
        }
        
        
        rango <-
          sumaRangos /
          cantidadIguales
        
        
        if (diferencia > 0) {
          
          sumaRangosPositivos <-
            sumaRangosPositivos +
            rango
        }
      }
      
      
      # ------------------------------------------------------
      # ESTADÍSTICO
      # ------------------------------------------------------
      
      mediaRangos <- (
        n *
          (n + 1)
      ) /
        4.0
      
      
      desviacionRangos <- sqrt(
        n *
          (n + 1) *
          (2 * n + 1) /
          24.0
      )
      
      
      z <- (
        sumaRangosPositivos -
          mediaRangos
      ) /
        desviacionRangos
      
      
      # ------------------------------------------------------
      # CORRECCIÓN DE CONTINUIDAD
      # ------------------------------------------------------
      
      if (z > 0) {
        
        z <- (
          sumaRangosPositivos -
            mediaRangos -
            0.5
        ) /
          desviacionRangos
        
      } else if (z < 0) {
        
        z <- (
          sumaRangosPositivos -
            mediaRangos +
            0.5
        ) /
          desviacionRangos
      }
      
      
      # ------------------------------------------------------
      # P-VALOR
      # ------------------------------------------------------
      
      pValor <- 2 * (
        1 -
          pnorm(
            abs(z)
          )
      )
      
      
      pValor <- max(
        0,
        min(
          1,
          pValor
        )
      )
      
      
      # ------------------------------------------------------
      # CONCLUSIÓN
      # ------------------------------------------------------
      
      if (pValor < significancia) {
        
        conclusion <- paste(
          "Se rechaza H0. La distribución de las esperas",
          "presenta una diferencia estadísticamente",
          "significativa respecto al valor de referencia."
        )
        
      } else {
        
        conclusion <- paste(
          "No se rechaza H0. No se encontró evidencia",
          "suficiente de una diferencia significativa",
          "respecto al valor de referencia."
        )
      }
      
      
      return(
        list(
          prueba = "Wilcoxon",
          estadistico = sprintf(
            "W+ = %.4f | z = %.4f",
            sumaRangosPositivos,
            z
          ),
          pValor = sprintf(
            "p = %.4f",
            pValor
          ),
          valorW = sumaRangosPositivos,
          valorZ = z,
          valorP = pValor,
          conclusion = conclusion
        )
      )
      
    },
    
    
    # ========================================================
    # DISTRIBUCIÓN NORMAL
    # ========================================================
    
    normalCDF = function(x) {
      
      return(
        pnorm(x)
      )
      
    },
    
    
    # ========================================================
    # DISTRIBUCIÓN T DE STUDENT
    # ========================================================
    
    studentTCDF = function(
    t,
    gradosLibertad
    ) {
      
      return(
        pt(
          t,
          df = gradosLibertad
        )
      )
      
    },
    
    
    # ========================================================
    # BETA REGULARIZADA
    # ========================================================
    
    regularizedBeta = function(
    x,
    a,
    b
    ) {
      
      return(
        pbeta(
          x,
          shape1 = a,
          shape2 = b
        )
      )
      
    },
    
    
    # ========================================================
    # FUNCIÓN GAMMA
    # ========================================================
    
    logGamma = function(x) {
      
      return(
        lgamma(x)
      )
      
    }
    
  )
)