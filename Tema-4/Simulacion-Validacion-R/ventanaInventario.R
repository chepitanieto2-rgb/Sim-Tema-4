# ============================================================
# ventanaInventario.R
# Interfaz Shiny para la simulación de inventarios
# ============================================================

library(shiny)


# ============================================================
# INTERFAZ DE LA VENTANA DE INVENTARIO
# ============================================================

ventanaInventarioUI <- function(id) {
  
  ns <- NS(id)
  
  tagList(
    
    # ========================================================
    # ESTILOS
    # ========================================================
    
    tags$style(
      HTML(
        "
        .inventario-container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 25px;
        }

        .inventario-titulo {
          background: #2E7D32;
          color: white;
          padding: 20px;
          border-radius: 10px;
          margin-bottom: 20px;
          text-align: center;
        }

        .inventario-panel {
          background: white;
          border: 1px solid #dddddd;
          border-radius: 10px;
          padding: 20px;
          margin-bottom: 20px;
          box-shadow: 0px 2px 5px rgba(0,0,0,0.08);
        }

        .inventario-subtitulo {
          font-size: 20px;
          font-weight: bold;
          color: #2E7D32;
          margin-bottom: 15px;
        }

        .inventario-card {
          background: #F4FBF4;
          border-left: 5px solid #2E7D32;
          border-radius: 7px;
          padding: 15px;
          margin-bottom: 10px;
          min-height: 95px;
        }

        .inventario-card-titulo {
          font-size: 14px;
          color: #555555;
          margin-bottom: 5px;
        }

        .inventario-card-valor {
          font-size: 24px;
          font-weight: bold;
          color: #2E7D32;
        }

        .inventario-estado {
          background: #F5F5F5;
          border-radius: 8px;
          padding: 18px;
          margin-top: 15px;
          white-space: pre-line;
        }

        .inventario-validacion {
          background: #F7F7F7;
          border-radius: 8px;
          padding: 18px;
          margin-top: 15px;
        }

        .btn-simular-inventario {
          width: 100%;
          font-size: 17px;
          font-weight: bold;
          margin-top: 10px;
        }

        .btn-volver-inventario {
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
      
      class = "inventario-container",
      
      
      # ======================================================
      # BOTÓN VOLVER
      # ======================================================
      
      actionButton(
        ns("btnVolver"),
        "Volver al menú principal",
        class = "btn btn-secondary btn-volver-inventario"
      ),
      
      
      # ======================================================
      # ENCABEZADO
      # ======================================================
      
      div(
        
        class = "inventario-titulo",
        
        h2(
          "Simulación de Inventario"
        ),
        
        p(
          paste(
            "Modelo de inventario con demanda aleatoria,",
            "punto de reorden y reabastecimiento"
          )
        )
        
      ),
      
      
      # ======================================================
      # PARÁMETROS
      # ======================================================
      
      div(
        
        class = "inventario-panel",
        
        div(
          class = "inventario-subtitulo",
          "Parámetros de la simulación"
        ),
        
        
        fluidRow(
          
          # --------------------------------------------------
          # INVENTARIO INICIAL
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("inventarioInicial"),
              "Inventario inicial:",
              value = 100,
              min = 0,
              step = 1
            )
            
          ),
          
          
          # --------------------------------------------------
          # PERIODOS
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("periodos"),
              "Número de períodos:",
              value = 10,
              min = 1,
              step = 1
            )
            
          ),
          
          
          # --------------------------------------------------
          # PUNTO DE REORDEN
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("puntoReorden"),
              "Punto de reorden:",
              value = 30,
              min = 0,
              step = 1
            )
            
          )
          
        ),
        
        
        fluidRow(
          
          # --------------------------------------------------
          # DEMANDA MÍNIMA
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("demandaMinima"),
              "Demanda mínima:",
              value = 10,
              min = 0,
              step = 1
            )
            
          ),
          
          
          # --------------------------------------------------
          # DEMANDA MÁXIMA
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("demandaMaxima"),
              "Demanda máxima:",
              value = 30,
              min = 0,
              step = 1
            )
            
          ),
          
          
          # --------------------------------------------------
          # CANTIDAD DEL PEDIDO
          # --------------------------------------------------
          
          column(
            
            width = 4,
            
            numericInput(
              ns("cantidadPedido"),
              "Cantidad de pedido para reorden:",
              value = 1,
              min = 1,
              step = 1
            )
            
          )
          
        ),
        
        
        # ----------------------------------------------------
        # BOTÓN SIMULAR
        # ----------------------------------------------------
        
        actionButton(
          ns("btnSimular"),
          "Ejecutar simulación",
          class = "btn btn-success btn-simular-inventario"
        )
        
      ),
      
      
      # ======================================================
      # RESULTADOS GENERALES
      # ======================================================
      
      div(
        
        class = "inventario-panel",
        
        div(
          class = "inventario-subtitulo",
          "Resultados generales"
        ),
        
        
        fluidRow(
          
          # --------------------------------------------------
          # INVENTARIO PROMEDIO
          # --------------------------------------------------
          
          column(
            
            width = 3,
            
            div(
              
              class = "inventario-card",
              
              div(
                class = "inventario-card-titulo",
                "Inventario promedio"
              ),
              
              div(
                class = "inventario-card-valor",
                
                textOutput(
                  ns("inventarioPromedio"),
                  inline = TRUE
                )
                
              )
              
            )
            
          ),
          
          
          # --------------------------------------------------
          # INVENTARIO MÍNIMO
          # --------------------------------------------------
          
          column(
            
            width = 3,
            
            div(
              
              class = "inventario-card",
              
              div(
                class = "inventario-card-titulo",
                "Inventario mínimo"
              ),
              
              div(
                class = "inventario-card-valor",
                
                textOutput(
                  ns("inventarioMinimo"),
                  inline = TRUE
                )
                
              )
              
            )
            
          ),
          
          
          # --------------------------------------------------
          # PEDIDOS REALIZADOS
          # --------------------------------------------------
          
          column(
            
            width = 3,
            
            div(
              
              class = "inventario-card",
              
              div(
                class = "inventario-card-titulo",
                "Pedidos realizados"
              ),
              
              div(
                class = "inventario-card-valor",
                
                textOutput(
                  ns("pedidosRealizados"),
                  inline = TRUE
                )
                
              )
              
            )
            
          ),
          
          
          # --------------------------------------------------
          # FALTANTE TOTAL
          # --------------------------------------------------
          
          column(
            
            width = 3,
            
            div(
              
              class = "inventario-card",
              
              div(
                class = "inventario-card-titulo",
                "Faltante total"
              ),
              
              div(
                class = "inventario-card-valor",
                
                textOutput(
                  ns("faltanteTotal"),
                  inline = TRUE
                )
                
              )
              
            )
            
          )
          
        ),
        
        
        # ====================================================
        # INVENTARIO ACTUAL
        # ====================================================
        
        fluidRow(
          
          column(
            
            width = 12,
            
            div(
              
              class = "inventario-card",
              
              div(
                class = "inventario-card-titulo",
                "Inventario actual al finalizar"
              ),
              
              div(
                class = "inventario-card-valor",
                
                textOutput(
                  ns("inventarioActual"),
                  inline = TRUE
                )
                
              )
              
            )
            
          )
          
        )
        
      ),
      
      
      # ======================================================
      # ESTADO DEL INVENTARIO
      # ======================================================
      
      div(
        
        class = "inventario-panel",
        
        div(
          class = "inventario-subtitulo",
          "Estado del inventario"
        ),
        
        div(
          
          class = "inventario-estado",
          
          textOutput(
            ns("estadoInventario")
          )
          
        )
        
      ),
      
      
      # ======================================================
      # TABLA DE PERIODOS
      # ======================================================
      
      div(
        
        class = "inventario-panel",
        
        div(
          class = "inventario-subtitulo",
          "Detalle de la simulación"
        ),
        
        tableOutput(
          ns("tablaInventario")
        )
        
      ),
      
      
      # ======================================================
      # VALIDACIÓN ESTADÍSTICA
      # ======================================================
      
      div(
        
        class = "inventario-panel",
        
        div(
          class = "inventario-subtitulo",
          "Validación estadística"
        ),
        
        
        fluidRow(
          
          # --------------------------------------------------
          # REFERENCIA
          # --------------------------------------------------
          
          column(
            
            width = 6,
            
            numericInput(
              ns("valorReferencia"),
              "Inventario promedio de referencia:",
              value = 50,
              min = 0,
              step = 0.1
            )
            
          ),
          
          
          # --------------------------------------------------
          # SIGNIFICANCIA
          # --------------------------------------------------
          
          column(
            
            width = 6,
            
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
            
          )
          
        ),
        
        
        # ----------------------------------------------------
        # BOTÓN VALIDAR
        # ----------------------------------------------------
        
        actionButton(
          ns("btnValidar"),
          "Validar simulación",
          class = "btn btn-success"
        ),
        
        
        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------
        
        div(
          
          class = "inventario-validacion",
          
          h4(
            "Resultado de la validación"
          ),
          
          
          strong(
            "Prueba:"
          ),
          
          span(
            "Prueba t de una muestra"
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
            "Promedio simulado:"
          ),
          
          textOutput(
            ns("promedioValidacion"),
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
# SERVIDOR DE LA VENTANA DE INVENTARIO
# ============================================================

ventanaInventarioServer <- function(
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
      # OBJETO INVENTARIO
      # ======================================================
      
      simulador <- Inventario$new()
      
      
      # ======================================================
      # VARIABLES REACTIVAS
      # ======================================================
      
      resultadoSimulacion <- reactiveVal(
        NULL
      )
      
      
      resultadoValidacion <- reactiveVal(
        NULL
      )
      
      
      # ======================================================
      # BOTÓN EJECUTAR SIMULACIÓN
      # ======================================================
      
      observeEvent(
        input$btnSimular,
        {
          
          tryCatch(
            
            {
              
              # ==============================================
              # EJECUTAR SIMULACIÓN
              # ==============================================
              
              resultado <- simulador$simular(
                
                inventarioInicial =
                  as.integer(
                    input$inventarioInicial
                  ),
                
                periodos =
                  as.integer(
                    input$periodos
                  ),
                
                demandaMinima =
                  as.integer(
                    input$demandaMinima
                  ),
                
                demandaMaxima =
                  as.integer(
                    input$demandaMaxima
                  ),
                
                puntoReorden =
                  as.integer(
                    input$puntoReorden
                  ),
                
                cantidadPedido =
                  as.integer(
                    input$cantidadPedido
                  )
                
              )
              
              
              # ==============================================
              # GUARDAR RESULTADO
              # ==============================================
              
              resultadoSimulacion(
                resultado
              )
              
              
              # Al realizar una nueva simulación,
              # borramos cualquier validación anterior.
              
              resultadoValidacion(
                NULL
              )
              
              
              showNotification(
                "Simulación de inventario realizada correctamente.",
                type = "message"
              )
              
            },
            
            
            # ================================================
            # ERROR
            # ================================================
            
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
      # INVENTARIO PROMEDIO
      # ======================================================
      
      output$inventarioPromedio <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          sprintf(
            "%.2f",
            resultado$inventarioPromedio
          ),
          " unidades"
        )
        
      })
      
      
      # ======================================================
      # INVENTARIO MÍNIMO
      # ======================================================
      
      output$inventarioMinimo <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          resultado$inventarioMinimo,
          " unidades"
        )
        
      })
      
      
      # ======================================================
      # PEDIDOS REALIZADOS
      # ======================================================
      
      output$pedidosRealizados <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        resultado$pedidosRealizados
        
      })
      
      
      # ======================================================
      # FALTANTE TOTAL
      # ======================================================
      
      output$faltanteTotal <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          resultado$faltanteTotal,
          " unidades"
        )
        
      })
      
      
      # ======================================================
      # INVENTARIO ACTUAL
      # ======================================================
      
      output$inventarioActual <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          resultado$inventarioActual,
          " unidades"
        )
        
      })
      
      
      # ======================================================
      # ESTADO DEL INVENTARIO
      # ======================================================
      
      output$estadoInventario <- renderText({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return(
            paste(
              "Ejecute una simulación para",
              "consultar el estado del inventario."
            )
          )
          
        }
        
        
        resultado$estadoInventario
        
      })
      
      
      # ======================================================
      # TABLA DE INVENTARIO
      # ======================================================
      
      output$tablaInventario <- renderTable({
        
        resultado <-
          resultadoSimulacion()
        
        
        if (is.null(resultado)) {
          
          return(NULL)
          
        }
        
        
        registros <-
          resultado$registros
        
        
        if (
          length(registros) == 0
        ) {
          
          return(NULL)
          
        }
        
        
        # ====================================================
        # CREAR DATA FRAME
        # ====================================================
        
        tabla <- data.frame(
          
          Periodo =
            integer(0),
          
          InventarioInicial =
            integer(0),
          
          Demanda =
            integer(0),
          
          Pedido =
            integer(0),
          
          InventarioFinal =
            integer(0),
          
          Faltante =
            integer(0)
          
        )
        
        
        # ====================================================
        # RECORRER REGISTROS
        # ====================================================
        
        for (
          registro in registros
        ) {
          
          fila <- data.frame(
            
            Periodo =
              registro$getPeriodo(),
            
            InventarioInicial =
              registro$getInventarioInicial(),
            
            Demanda =
              registro$getDemanda(),
            
            Pedido =
              registro$getPedido(),
            
            InventarioFinal =
              registro$getInventarioFinal(),
            
            Faltante =
              registro$getFaltante()
            
          )
          
          
          tabla <- rbind(
            tabla,
            fila
          )
          
        }
        
        
        # ====================================================
        # NOMBRES VISIBLES
        # ====================================================
        
        names(tabla) <- c(
          "Período",
          "Inventario inicial",
          "Demanda",
          "Pedido",
          "Inventario final",
          "Faltante"
        )
        
        
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
          
          # ==================================================
          # COMPROBAR SIMULACIÓN
          # ==================================================
          
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
              
              # ==============================================
              # EJECUTAR VALIDACIÓN
              # ==============================================
              
              validacion <-
                simulador$validarSimulacion(
                  
                  referencia =
                    as.numeric(
                      input$valorReferencia
                    ),
                  
                  significancia =
                    as.numeric(
                      input$significancia
                    )
                  
                )
              
              
              # ==============================================
              # GUARDAR RESULTADO
              # ==============================================
              
              resultadoValidacion(
                validacion
              )
              
              
              showNotification(
                "Validación estadística realizada correctamente.",
                type = "message"
              )
              
            },
            
            
            # ================================================
            # ERROR
            # ================================================
            
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
      # PROMEDIO DE VALIDACIÓN
      # ======================================================
      
      output$promedioValidacion <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return("-")
          
        }
        
        
        paste0(
          sprintf(
            "%.2f",
            resultado$promedio
          ),
          " unidades"
        )
        
      })
      
      
      # ======================================================
      # CONCLUSIÓN
      # ======================================================
      
      output$conclusion <- renderText({
        
        resultado <-
          resultadoValidacion()
        
        
        if (is.null(resultado)) {
          
          return(
            paste(
              "Ejecute la simulación y posteriormente",
              "realice la validación estadística."
            )
          )
          
        }
        
        
        resultado$conclusion
        
      })
      
      
      
      
      # ======================================================
      # BOTÓN VOLVER
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