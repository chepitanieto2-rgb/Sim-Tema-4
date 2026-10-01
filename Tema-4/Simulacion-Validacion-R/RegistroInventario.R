# ============================================================
# RegistroInventario.R
# Registro de cada periodo de la simulación de inventario
# ============================================================

library(R6)


RegistroInventario <- R6Class(
  "RegistroInventario",
  
  public = list(
    
    # ========================================================
    # ATRIBUTOS
    # ========================================================
    
    periodo = NULL,
    inventarioInicial = NULL,
    demanda = NULL,
    pedido = NULL,
    inventarioFinal = NULL,
    faltante = NULL,
    
    
    # ========================================================
    # CONSTRUCTOR
    # ========================================================
    
    initialize = function(
    periodo,
    inventarioInicial,
    demanda,
    pedido,
    inventarioFinal,
    faltante
    ) {
      
      self$periodo <- periodo
      
      self$inventarioInicial <- inventarioInicial
      
      self$demanda <- demanda
      
      self$pedido <- pedido
      
      self$inventarioFinal <- inventarioFinal
      
      self$faltante <- faltante
      
    },
    
    
    # ========================================================
    # GET PERIODO
    # ========================================================
    
    getPeriodo = function() {
      
      return(
        self$periodo
      )
      
    },
    
    
    # ========================================================
    # GET INVENTARIO INICIAL
    # ========================================================
    
    getInventarioInicial = function() {
      
      return(
        self$inventarioInicial
      )
      
    },
    
    
    # ========================================================
    # GET DEMANDA
    # ========================================================
    
    getDemanda = function() {
      
      return(
        self$demanda
      )
      
    },
    
    
    # ========================================================
    # GET PEDIDO
    # ========================================================
    
    getPedido = function() {
      
      return(
        self$pedido
      )
      
    },
    
    
    # ========================================================
    # GET INVENTARIO FINAL
    # ========================================================
    
    getInventarioFinal = function() {
      
      return(
        self$inventarioFinal
      )
      
    },
    
    
    # ========================================================
    # GET FALTANTE
    # ========================================================
    
    getFaltante = function() {
      
      return(
        self$faltante
      )
      
    }
    
  )
)