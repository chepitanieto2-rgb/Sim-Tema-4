# ============================================================
# ventanaEspera.R
# Interfaz Shiny para la simulación de líneas de espera
# ============================================================

library(shiny)


# ============================================================
# INTERFAZ DE LA VENTANA DE ESPERA
# ============================================================

ventanaEsperaUI <- function(id) {
  
  ns <- NS(id)
  
  tagList(
    
    # ========================================================
    # ESTILOS
    # ========================================================
    
    tags$style(
      HTML(
        "
        .espera-container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 25px;
        }

        .espera-titulo {
          background: #1565C0;
          color: white;
          padding: 20px;
          border-radius: 10px;
          margin-bottom: 20px;
          text-align: center;
        }

        .espera-panel {
          background: white;
          border: 1px solid #dddddd;
          border-radius: 10px;
          padding: 20px;
          margin-bottom: 20px;
          box-shadow: 0px 2px 5px rgba(0,0,0,0.08);
        }

        .espera-subtitulo {
          font-size: 20px;
          font-weight: bold;
          color: #1565C0;
          margin-bottom: 15px;
        }

        .resultado-card {
          background: #F5F9FF;
          border-left: 5px solid #1565C0;
          border-radius: 7px;
          padding: 15px;
          margin-bottom: 10px;
          min-height: 95px;
        }

        .resultado-titulo {
          font-size: 14px;
          color: #555555;
          margin-bottom: 5px;
        }

        .resultado-valor {
          font-size: 24px;
          font-weight: bold;
          color: #1565C0;
        }

        .validacion-resultado {
          background: #F7F7F7;
          border-radius: 8px;
          padding: 18px;
          margin-top: 15px;
        }

        .btn-simular {
          width: 100%;
          font-size: 17px;
          font-weight: bold;
          margin-top: 10px;
        }

        .btn-volver {
          margin-bottom: 15px;
          background: #FFA500;
        }

        table {
          width: 100%;
        }
        "
      )
    ),
    
    
    div(
      
      class = "espera-container",
      
      
      # ======================================================
      # BOTÓN VOLVER
      # ======================================================
      
      actionButton(
        ns("btnVolver"),
        "Volver al menú principal",
        class = "btn btn-secondary btn-volver"
      ),
      
      
      # ======================================================
      # ENCABEZADO
      # ======================================================
      
      div(
        
        class = "espera-titulo",
        
        h2(
          "Simulación de Líneas de Espera"
        ),
        
        p(
          "Modelo de atención de clientes con múltiples servidores"
        )
        
      ),
      
      
      # ======================================================
      # PARÁMETROS
      # ======================================================
      
      div(
        
        class = "espera-panel",
        
        div(
          class = "espera-subtitulo",
          "Parámetros de la simulación"
        ),
        
        
        fluidRow(
          
          column(
            
            width = 4,
            
            numericInput(
              ns("cantidadClientes"),
              "Cantidad de clientes:",
              value = 20,
              min = 1,
              step = 1
            )
            
          ),
          
          
          column(
            
            width = 4,
            
            numericInput(
              ns("cantidadServidores"),
              "Cantidad de servidores:",
              value = 2,
              min = 1,
              step = 1
            )
            
          )
          
        ),
        
        
        fluidRow(
          
          column(
            
            width = 3,
            
            numericInput(
              ns("llegadaMinima"),
              "Llegada mínima:",
              value = 1,
              min = 0,
              step = 0.1
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            numericInput(
              ns("llegadaMaxima"),
              "Llegada máxima:",
              value = 5,
              min = 0,
              step = 0.1
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            numericInput(
              ns("servicioMinimo"),
              "Servicio mínimo:",
              value = 2,
              min = 0,
              step = 0.1
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            numericInput(
              ns("servicioMaximo"),
              "Servicio máximo:",
              value = 6,
              min = 0,
              step = 0.1
            )
            
          )
          
        ),
        
        
        actionButton(
          ns("btnSimular"),
          "Ejecutar simulación",
          class = "btn btn-primary btn-simular"
        )
        
      ),
      
      
      # ======================================================
      # RESULTADOS GENERALES
      # ======================================================
      
      div(
        
        class = "espera-panel",
        
        div(
          class = "espera-subtitulo",
          "Resultados generales"
        ),
        
        
        fluidRow(
          
          column(
            
            width = 3,
            
            div(
              
              class = "resultado-card",
              
              div(
                class = "resultado-titulo",
                "Espera promedio"
              ),
              
              div(
                class = "resultado-valor",
                textOutput(
                  ns("esperaPromedio"),
                  inline = TRUE
                )
              )
              
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            div(
              
              class = "resultado-card",
              
              div(
                class = "resultado-titulo",
                "Espera máxima"
              ),
              
              div(
                class = "resultado-valor",
                textOutput(
                  ns("esperaMaxima"),
                  inline = TRUE
                )
              )
              
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            div(
              
              class = "resultado-card",
              
              div(
                class = "resultado-titulo",
                "Clientes que esperaron"
              ),
              
              div(
                class = "resultado-valor",
                textOutput(
                  ns("clientesEsperaron"),
                  inline = TRUE
                )
              )
              
            )
            
          ),
          
          
          column(
            
            width = 3,
            
            div(
              
              class = "resultado-card",
              
              div(
                class = "resultado-titulo",
                "Utilización"
              ),
              
              div(
                class = "resultado-valor",
                textOutput(
                  ns("utilizacion"),
                  inline = TRUE
                )
              )
              
            )
            
          )
          
        )
        
      ),
      
      
      # ======================================================
      # TABLA
      # ======================================================
      
      div(
        
        class = "espera-panel",
        
        div(
          class = "espera-subtitulo",
          "Detalle de clientes"
        ),
        
        tableOutput(
          ns("tablaClientes")
        )
        
      ),
      
      
      # ======================================================
      # VALIDACIÓN ESTADÍSTICA
      # ======================================================
      
      div(
        
        class = "espera-panel",
        
        div(
          class = "espera-subtitulo",
          "Validación estadística"
        ),
        
        
        fluidRow(
          
          column(
            
            width = 4,
            
            numericInput(
              ns("valorReferencia"),
              "Valor de referencia:",
              value = 2,
              min = 0,
              step = 0.1
            )
            
          ),
          
          
          column(
            
            width = 4,
            
            selectInput(
              ns("significancia"),
              "Nivel de significancia:",
              choices = c(
                "0.10" = 0.10,
                "0.05" = 0.05,
                "0.01" = 0.01
              ),
              selected = 0.05
            )
            
          ),
          
          
          column(
            
            width = 4,
            
            selectInput(
              ns("tipoPrueba"),
              "Tipo de prueba:",
              choices = c(
                "Prueba paramétrica (t de Student)",
                "Prueba no paramétrica (Wilcoxon)"
              )
            )
            
          )
          
        ),
        
        
        actionButton(
          ns("btnValidar"),
          "Validar simulación",
          class = "btn btn-success"
        ),
        
        
        div(
          
          class = "validacion-resultado",
          
          h4(
            "Resultado de la validación"
          ),
          
          strong(
            "Prueba:"
          ),
          
          textOutput(
            ns("nombrePrueba"),
            inline = TRUE
          ),
          
          br(),
          br(),
          
          strong(
            "Estadístico:"
          ),
          
          textOutput(
            ns("estadistico"),
            inline = TRUE
          ),
          
          br(),
          
          strong(
            "P-valor:"
          ),
          
          textOutput(
            ns("pValor"),
            inline = TRUE
          ),
          
          br(),
          br(),
          
          strong(
            "Conclusión:"
          ),
          
          textOutput(
            ns("conclusion")
          )
          
        )
        
      )
      
    )
    
  )
  
}


# ============================================================
# SERVIDOR DE LA VENTANA DE ESPERA
# ============================================================

ventanaEsperaServer <- function(
    id,
    volverPrincipal = NULL
) {
  
  moduleServer(
    
    id,
    
    function(
    input,
    output,
    session
    ) {
      
      
      # ======================================================
      # OBJETO DE SIMULACIÓN
      # ======================================================
      
      simulador <- Espera$new()
      
      
      # ======================================================
      # ALMACENAR RESULTADOS
      # ======================================================
      
      resultadoSimulacion <- reactiveVal(
        NULL
      )
      
      
      resultadoValidacion <- reactiveVal(
        NULL
      )
      
      
      # ======================================================
      # BOTÓN SIMULAR
      # ======================================================
      
      observeEvent(
        input$btnSimular,
        {
          
          tryCatch(
            
            {
              
              resultado <- simulador$simular(
                
                cantidadClientes =
                  as.integer(
                    input$cantidadClientes
                  ),
                
                cantidadServidores =
                  as.integer(
                    input$cantidadServidores
                  ),
                
                llegadaMinima =
                  as.numeric(
                    input$llegadaMinima
                  ),
                
                llegadaMaxima =
                  as.numeric(
                    input$llegadaMaxima
                  ),
                
                servicioMinimo =
                  as.numeric(
                    input$servicioMinimo
                  ),
                
                servicioMaximo =
                  as.numeric(
                    input$servicioMaximo
                  )
                
              )
              
              
              resultadoSimulacion(
                resultado
              )
              
              
              # Borrar validación anterior
              
              resultadoValidacion(
                NULL
              )
              
              
              showNotification(
                "Simulación realizada correctamente.",
                type = "message"
              )
              
            },
            
            error = function(e) {
              
              showNotification(
                e$message,
                type = "error",
                duration = 6
              )
              
            }
            
          )
          
        }
        
      )
      
      
      # ======================================================
      # ESPERA PROMEDIO
      # ======================================================
      
      output$esperaPromedio <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          sprintf(
            "%.2f",
            resultado$esperaPromedio
          ),
          " min"
        )
        
      })
      
      
      # ======================================================
      # ESPERA MÁXIMA
      # ======================================================
      
      output$esperaMaxima <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          sprintf(
            "%.2f",
            resultado$esperaMaxima
          ),
          " min"
        )
        
      })
      
      
      # ======================================================
      # CLIENTES QUE ESPERARON
      # ======================================================
      
      output$clientesEsperaron <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        resultado$clientesEsperaron
        
      })
      
      
      # ======================================================
      # UTILIZACIÓN
      # ======================================================
      
      output$utilizacion <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          sprintf(
            "%.2f",
            resultado$utilizacion
          ),
          "%"
        )
        
      })
      
      
      # ======================================================
      # TABLA DE CLIENTES
      # ======================================================
      
      output$tablaClientes <- renderTable({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return(NULL)
          
        }
        
        
        clientes <-
          resultado$clientes
        
        
        if (
          length(clientes) == 0
        ) {
          
          return(NULL)
          
        }
        
        
        tabla <- data.frame(
          
          Cliente =
            integer(0),
          
          Servidor =
            integer(0),
          
          Llegada =
            numeric(0),
          
          Servicio =
            numeric(0),
          
          Espera =
            numeric(0),
          
          Inicio =
            numeric(0),
          
          Fin =
            numeric(0)
          
        )
        
        
        for (
          cliente in clientes
        ) {
          
          fila <- data.frame(
            
            Cliente =
              cliente$getNumero(),
            
            Servidor =
              cliente$getServidor(),
            
            Llegada =
              round(
                cliente$getLlegada(),
                2
              ),
            
            Servicio =
              round(
                cliente$getServicio(),
                2
              ),
            
            Espera =
              round(
                cliente$getEspera(),
                2
              ),
            
            Inicio =
              round(
                cliente$getInicio(),
                2
              ),
            
            Fin =
              round(
                cliente$getFin(),
                2
              )
            
          )
          
          
          tabla <- rbind(
            tabla,
            fila
          )
          
        }
        
        
        tabla
        
      },
      striped = TRUE,
      bordered = TRUE,
      hover = TRUE,
      spacing = "s"
      )
      
      
      # ======================================================
      # BOTÓN VALIDAR
      # ======================================================
      
      observeEvent(
        input$btnValidar,
        {
          
          if (
            is.null(
              resultadoSimulacion()
            )
          ) {
            
            showNotification(
              "Primero debe ejecutar una simulación.",
              type = "warning"
            )
            
            return()
            
          }
          
          
          tryCatch(
            
            {
              
              validacion <-
                simulador$validarSimulacion(
                  
                  referencia =
                    as.numeric(
                      input$valorReferencia
                    ),
                  
                  significancia =
                    as.numeric(
                      input$significancia
                    ),
                  
                  tipoPrueba =
                    input$tipoPrueba
                  
                )
              
              
              resultadoValidacion(
                validacion
              )
              
              
              showNotification(
                "Validación realizada correctamente.",
                type = "message"
              )
              
            },
            
            error = function(e) {
              
              showNotification(
                e$message,
                type = "error",
                duration = 6
              )
              
            }
            
          )
          
        }
        
      )
      
      
      # ======================================================
      # NOMBRE DE PRUEBA
      # ======================================================
      
      output$nombrePrueba <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        resultado$prueba
        
      })
      
      
      # ======================================================
      # ESTADÍSTICO
      # ======================================================
      
      output$estadistico <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        resultado$estadistico
        
      })
      
      
      # ======================================================
      # P-VALOR
      # ======================================================
      
      output$pValor <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        resultado$pValor
        
      })
      
      
      # ======================================================
      # CONCLUSIÓN
      # ======================================================
      
      output$conclusion <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return(
            "Ejecute la simulación y posteriormente realice la validación."
          )
          
        }
        
        
        resultado$conclusion
        
      })
      
      
      # ======================================================
      # VOLVER A LA VENTANA PRINCIPAL
      # ======================================================
      
      observeEvent(
        input$btnVolver,
        {
          
          if (
            !is.null(
              volverPrincipal
            )
          ) {
            
            volverPrincipal()
            
          }
          
        }
        
      )
      
    }
    
  )
  
}