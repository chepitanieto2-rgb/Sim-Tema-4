library(R6)

Cliente <- R6Class(
  "Cliente",
  
  public = list(
    
    numero = NULL,
    servidor = NULL,
    llegada = NULL,
    servicio = NULL,
    espera = NULL,
    inicio = NULL,
    fin = NULL,
    
    initialize = function(
    numero,
    servidor,
    llegada,
    servicio,
    espera,
    inicio,
    fin
    ) {
      self$numero <- numero
      self$servidor <- servidor
      self$llegada <- llegada
      self$servicio <- servicio
      self$espera <- espera
      self$inicio <- inicio
      self$fin <- fin
    },
    
    getNumero = function() {
      return(self$numero)
    },
    
    getServidor = function() {
      return(self$servidor)
    },
    
    getLlegada = function() {
      return(self$llegada)
    },
    
    getServicio = function() {
      return(self$servicio)
    },
    
    getEspera = function() {
      return(self$espera)
    },
    
    getInicio = function() {
      return(self$inicio)
    },
    
    getFin = function() {
      return(self$fin)
    }
  )
)