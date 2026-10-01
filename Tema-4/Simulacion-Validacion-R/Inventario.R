# ============================================================
# Inventario.R
# Lógica de simulación del sistema de inventario
# ============================================================

library(R6)


Inventario <- R6Class(
  "Inventario",
  
  public = list(
    
    # ========================================================
    # ATRIBUTOS
    # ========================================================
    
    registros = NULL,
    datosValidacion = NULL,
    
    
    # ========================================================
    # CONSTRUCTOR
    # ========================================================
    
    initialize = function() {
      
      self$registros <- list()
      self$datosValidacion <- numeric(0)
      
    },
    
    
    # ========================================================
    # SIMULACIÓN
    # ========================================================
    
    simular = function(
    inventarioInicial,
    periodos,
    demandaMinima,
    demandaMaxima,
    puntoReorden,
    cantidadPedido
    ) {
      
      # ------------------------------------------------------
      # VALIDACIONES
      # ------------------------------------------------------
      
      if (
        inventarioInicial < 0 ||
        periodos <= 0 ||
        demandaMinima < 0 ||
        demandaMaxima < 0 ||
        puntoReorden < 0 ||
        cantidadPedido <= 0
      ) {
        
        stop(
          "Los valores ingresados no son válidos."
        )
      }
      
      
      if (demandaMinima > demandaMaxima) {
        
        stop(
          paste(
            "La demanda mínima no puede ser mayor",
            "que la demanda máxima."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # LIMPIAR DATOS ANTERIORES
      # ------------------------------------------------------
      
      self$registros <- list()
      self$datosValidacion <- numeric(0)
      
      
      # ------------------------------------------------------
      # VARIABLES DE LA SIMULACIÓN
      # ------------------------------------------------------
      
      inventarioActual <- inventarioInicial
      
      pedidosRealizados <- 0
      
      faltanteTotal <- 0
      
      sumaInventarios <- 0.0
      
      inventarioMinimo <- Inf
      
      
      # ======================================================
      # SIMULAR CADA PERÍODO
      # ======================================================
      
      for (periodo in seq_len(periodos)) {
        
        inventarioInicioPeriodo <-
          inventarioActual
        
        
        # ----------------------------------------------------
        # GENERAR DEMANDA ALEATORIA
        # ----------------------------------------------------
        
        demanda <- self$generarEntero(
          demandaMinima,
          demandaMaxima
        )
        
        
        # ----------------------------------------------------
        # CALCULAR UNIDADES ATENDIDAS
        # ----------------------------------------------------
        
        unidadesAtendidas <- min(
          inventarioInicioPeriodo,
          demanda
        )
        
        
        # ----------------------------------------------------
        # CALCULAR FALTANTE
        # ----------------------------------------------------
        
        faltante <- max(
          0,
          demanda - inventarioInicioPeriodo
        )
        
        
        # ----------------------------------------------------
        # INVENTARIO DESPUÉS DE LA DEMANDA
        # ----------------------------------------------------
        
        inventarioDespuesDemanda <- (
          inventarioInicioPeriodo -
            unidadesAtendidas
        )
        
        
        pedido <- 0
        
        
        # ----------------------------------------------------
        # PUNTO DE REORDEN
        # ----------------------------------------------------
        
        if (
          inventarioDespuesDemanda <=
          puntoReorden
        ) {
          
          pedido <- cantidadPedido
          
          pedidosRealizados <-
            pedidosRealizados + 1
        }
        
        
        # ----------------------------------------------------
        # INVENTARIO FINAL
        # ----------------------------------------------------
        
        inventarioFinal <- (
          inventarioDespuesDemanda +
            pedido
        )
        
        
        # ----------------------------------------------------
        # ACUMULAR ESTADÍSTICAS
        # ----------------------------------------------------
        
        faltanteTotal <- (
          faltanteTotal +
            faltante
        )
        
        
        sumaInventarios <- (
          sumaInventarios +
            inventarioFinal
        )
        
        
        inventarioMinimo <- min(
          inventarioMinimo,
          inventarioFinal
        )
        
        
        # ----------------------------------------------------
        # CREAR REGISTRO
        # ----------------------------------------------------
        
        registro <- RegistroInventario$new(
          periodo,
          inventarioInicioPeriodo,
          demanda,
          pedido,
          inventarioFinal,
          faltante
        )
        
        
        # Guardar el registro correctamente en la lista
        
        self$registros[[length(self$registros) + 1]] <- registro
        
        
        # ----------------------------------------------------
        # DATOS PARA VALIDACIÓN
        # ----------------------------------------------------
        
        self$datosValidacion <- c(
          self$datosValidacion,
          as.numeric(inventarioFinal)
        )
        
        
        # ----------------------------------------------------
        # ACTUALIZAR INVENTARIO
        # ----------------------------------------------------
        
        inventarioActual <- inventarioFinal
      }
      
      
      # ======================================================
      # RESULTADOS GENERALES
      # ======================================================
      
      promedio <- (
        sumaInventarios /
          periodos
      )
      
      
      estadoInventario <- self$evaluarInventario(
        inventarioActual,
        puntoReorden,
        cantidadPedido
      )
      
      
      # ======================================================
      # DEVOLVER RESULTADOS
      # ======================================================
      
      return(
        list(
          registros = self$registros,
          inventarioPromedio = promedio,
          inventarioMinimo = as.integer(inventarioMinimo),
          pedidosRealizados = pedidosRealizados,
          faltanteTotal = faltanteTotal,
          inventarioActual = inventarioActual,
          estadoInventario = estadoInventario
        )
      )
      
    },
    
    
    # ========================================================
    # ESTADO DEL INVENTARIO
    # ========================================================
    
    evaluarInventario = function(
    inventarioActual,
    puntoReorden,
    cantidadPedido
    ) {
      
      # ------------------------------------------------------
      # INVENTARIO CRÍTICO
      # ------------------------------------------------------
      
      if (inventarioActual <= 0) {
        
        return(
          paste0(
            "🔴 INVENTARIO CRÍTICO\n",
            "Inventario actual: ",
            inventarioActual,
            " unidades.\n",
            "Se requiere reabastecimiento."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # REORDEN RECOMENDADO
      # ------------------------------------------------------
      
      else if (
        inventarioActual <=
        puntoReorden
      ) {
        
        return(
          paste0(
            "🟠 REORDEN RECOMENDADO\n",
            "Inventario actual: ",
            inventarioActual,
            " unidades.\n",
            "Punto de reorden: ",
            puntoReorden,
            " unidades.\n",
            "Pedido sugerido: ",
            cantidadPedido,
            " unidades.\n",
            "Es recomendable solicitar nueva mercancía."
          )
        )
      }
      
      
      # ------------------------------------------------------
      # INVENTARIO SUFICIENTE
      # ------------------------------------------------------
      
      else {
        
        return(
          paste0(
            "🟢 INVENTARIO SUFICIENTE\n",
            "Inventario actual: ",
            inventarioActual,
            " unidades.\n",
            "Punto de reorden: ",
            puntoReorden,
            " unidades.\n",
            "Por el momento no es necesario ",
            "realizar otro pedido."
          )
        )
      }
      
    },
    
    
    # ========================================================
    # VALIDACIÓN DE LA SIMULACIÓN
    # ========================================================
    
    validarSimulacion = function(
    referencia,
    significancia
    ) {
      
      if (
        length(self$datosValidacion) < 2
      ) {
        
        stop(
          paste(
            "Primero debe ejecutar una simulación",
            "con al menos 2 períodos."
          )
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
      
      
      return(
        self$ejecutarPruebaT(
          referencia,
          significancia
        )
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
        self$datosValidacion
      )
      
      
      # ------------------------------------------------------
      # PROMEDIO
      # ------------------------------------------------------
      
      suma <- 0.0
      
      for (dato in self$datosValidacion) {
        
        suma <- suma + dato
      }
      
      
      promedio <- (
        suma /
          n
      )
      
      
      # ------------------------------------------------------
      # DESVIACIÓN ESTÁNDAR MUESTRAL
      # ------------------------------------------------------
      
      sumaCuadrados <- 0.0
      
      for (dato in self$datosValidacion) {
        
        sumaCuadrados <- (
          sumaCuadrados +
            (dato - promedio)^2
        )
      }
      
      
      desviacion <- sqrt(
        sumaCuadrados /
          (n - 1)
      )
      
      
      # ------------------------------------------------------
      # SIN VARIABILIDAD
      # ------------------------------------------------------
      
      if (desviacion == 0) {
        
        return(
          list(
            estadistico = "No calculable",
            pValor = "No calculable",
            valorEstadistico = NULL,
            valorP = NULL,
            promedio = promedio,
            conclusion = paste(
              "No es posible realizar la prueba t porque",
              "los resultados no presentan variabilidad."
            )
          )
        )
      }
      
      
      # ------------------------------------------------------
      # ESTADÍSTICO T
      # ------------------------------------------------------
      
      tEstadistico <- (
        promedio -
          referencia
      ) /
        (
          desviacion /
            sqrt(n)
        )
      
      
      # ------------------------------------------------------
      # P-VALOR BILATERAL
      # ------------------------------------------------------
      #
      # Conservamos el comportamiento de tu versión
      # Python/Java utilizando aproximación normal.
      # ------------------------------------------------------
      
      pValor <- (
        2.0 *
          (
            1.0 -
              self$normalCDF(
                abs(tEstadistico)
              )
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
      
      if (
        pValor <
        significancia
      ) {
        
        conclusion <- paste0(
          "El p-valor es menor que el nivel de ",
          "significancia (",
          significancia,
          "). ",
          "Existe evidencia estadística de que ",
          "el inventario promedio simulado es diferente ",
          "del valor de referencia de ",
          sprintf("%.2f", referencia),
          " unidades."
        )
        
      } else {
        
        conclusion <- paste0(
          "El p-valor es mayor o igual que el nivel de ",
          "significancia (",
          significancia,
          "). ",
          "No se encontró evidencia estadística ",
          "suficiente para afirmar que el inventario ",
          "promedio simulado sea diferente del valor ",
          "de referencia de ",
          sprintf("%.2f", referencia),
          " unidades."
        )
      }
      
      
      return(
        list(
          estadistico = sprintf(
            "%.4f",
            tEstadistico
          ),
          pValor = sprintf(
            "%.4f",
            pValor
          ),
          valorEstadistico = tEstadistico,
          valorP = pValor,
          promedio = promedio,
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
    # FUNCIÓN DE ERROR
    # ========================================================
    
    erf = function(x) {
      
      signo <- ifelse(
        x < 0,
        -1,
        1
      )
      
      
      x <- abs(x)
      
      
      a1 <- 0.254829592
      a2 <- -0.284496736
      a3 <- 1.421413741
      a4 <- -1.453152027
      a5 <- 1.061405429
      p <- 0.3275911
      
      
      t <- (
        1.0 /
          (
            1.0 +
              p * x
          )
      )
      
      
      y <- (
        1.0 -
          (
            (
              (
                (
                  (
                    a5 * t +
                      a4
                  ) * t +
                    a3
                ) * t +
                  a2
              ) * t +
                a1
            ) *
              t *
              exp(
                -x * x
              )
          )
      )
      
      
      return(
        signo * y
      )
      
    },
    
    
    # ========================================================
    # NÚMERO ALEATORIO ENTERO
    # ========================================================
    
    generarEntero = function(
    minimo,
    maximo
    ) {
      
      return(
        sample(
          minimo:maximo,
          size = 1
        )
      )
      
    }
    
  )
)