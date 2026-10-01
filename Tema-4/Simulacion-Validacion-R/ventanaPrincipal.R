# ============================================================
# ventanaPrincipal.R
# Ventana principal de la aplicación
# ============================================================

library(shiny)
library(R6)


# ============================================================
# CARGAR ARCHIVOS DEL PROYECTO
# ============================================================

source("Cliente.R")
source("Espera.R")

source("RegistroInventario.R")
source("Inventario.R")

source("ventanaEspera.R")
source("ventanaInventario.R")


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

ventanaPrincipalUI <- function() {
  
  tagList(
    
    # ========================================================
    # ESTILOS GENERALES
    # ========================================================
    
    tags$head(
      
      tags$style(
        
        HTML(
          "

          body {
            background-color: #f4f6f8;
            font-family: Arial, Helvetica, sans-serif;
          }


          /* ================================================
             CONTENEDOR PRINCIPAL
             ================================================ */

          .principal-container {

            max-width: 1100px;

            margin: 0 auto;

            padding: 40px 25px;

          }


          /* ================================================
             ENCABEZADO
             ================================================ */

          .principal-header {

            background: #263238;

            color: white;

            padding: 35px;

            border-radius: 12px;

            text-align: center;

            margin-bottom: 35px;

            box-shadow:
              0px 3px 8px
              rgba(0, 0, 0, 0.15);

          }


          .principal-header h1 {

            margin: 0;

            font-size: 34px;

            font-weight: bold;

          }


          .principal-header p {

            margin-top: 12px;

            margin-bottom: 0;

            font-size: 17px;

            color: #CFD8DC;

          }


          /* ================================================
             TARJETAS
             ================================================ */

          .menu-card {

            background: white;

            border-radius: 12px;

            padding: 30px;

            min-height: 300px;

            text-align: center;

            margin-bottom: 25px;

            box-shadow:
              0px 3px 10px
              rgba(0, 0, 0, 0.10);

            transition:
              transform 0.2s,
              box-shadow 0.2s;

          }


          .menu-card:hover {

            transform:
              translateY(-4px);

            box-shadow:
              0px 6px 15px
              rgba(0, 0, 0, 0.15);

          }


          /* ================================================
             ICONOS
             ================================================ */

          .menu-icon {

            font-size: 65px;

            margin-bottom: 15px;

          }


          /* ================================================
             TÍTULOS
             ================================================ */

          .menu-card h3 {

            font-size: 24px;

            font-weight: bold;

            margin-bottom: 15px;

          }


          .menu-card p {

            color: #666666;

            font-size: 15px;

            min-height: 70px;

          }


          /* ================================================
             ESPERA
             ================================================ */

          .card-espera {

            border-top:
              6px solid #1565C0;

          }


          .card-espera h3 {

            color: #1565C0;

          }


          /* ================================================
             INVENTARIO
             ================================================ */

          .card-inventario {

            border-top:
              6px solid #2E7D32;

          }


          .card-inventario h3 {

            color: #2E7D32;

          }


          /* ================================================
             BOTONES
             ================================================ */

          .btn-menu {

            width: 100%;

            padding: 12px;

            font-size: 16px;

            font-weight: bold;

            border-radius: 7px;

            margin-top: 15px;

          }


          /* ================================================
             PIE DE PÁGINA
             ================================================ */

          .principal-footer {

            text-align: center;

            margin-top: 25px;

            padding: 15px;

            color: #777777;

            font-size: 13px;

          }

          "
        )
        
      )
      
    ),
    
    
    # ========================================================
    # CONTENEDOR DINÁMICO
    # ========================================================
    
    uiOutput(
      "contenidoPrincipal"
    )
    
  )
  
}


# ============================================================
# SERVIDOR PRINCIPAL
# ============================================================

ventanaPrincipalServer <- function(
    input,
    output,
    session
) {
  
  
  # ==========================================================
  # PANTALLA ACTUAL
  # ==========================================================
  #
  # Puede contener:
  #
  # "principal"
  # "espera"
  # "inventario"
  #
  # ==========================================================
  
  pantallaActual <- reactiveVal(
    "principal"
  )
  
  
  # ==========================================================
  # FUNCIÓN PARA VOLVER AL MENÚ PRINCIPAL
  # ==========================================================
  
  volverPrincipal <- function() {
    
    pantallaActual(
      "principal"
    )
    
  }
  
  
  # ==========================================================
  # GENERAR CONTENIDO
  # ==========================================================
  
  output$contenidoPrincipal <- renderUI({
    
    
    # --------------------------------------------------------
    # PANTALLA PRINCIPAL
    # --------------------------------------------------------
    
    if (
      pantallaActual() ==
      "principal"
    ) {
      
      return(
        
        div(
          
          class =
            "principal-container",
          
          
          # ==================================================
          # ENCABEZADO
          # ==================================================
          
          div(
            
            class =
              "principal-header",
            
            h1(
              "Sistema de Simulación"
            ),
            
            p(
              paste(
                "Simulación y validación de",
                "líneas de espera e inventarios"
              )
            )
            
          ),
          
          
          # ==================================================
          # OPCIONES
          # ==================================================
          
          fluidRow(
            
            
            # =================================================
            # ESPERA
            # =================================================
            
            column(
              
              width = 6,
              
              
              div(
                
                class =
                  "menu-card card-espera",
                
                
                div(
                  
                  class =
                    "menu-icon",
                  
                  "⏱️"
                  
                ),
                
                
                h3(
                  "Líneas de Espera"
                ),
                
                
                p(
                  paste(
                    "Simula la llegada y atención",
                    "de clientes mediante uno o",
                    "varios servidores y analiza",
                    "los tiempos de espera."
                  )
                ),
                
                
                actionButton(
                  
                  inputId =
                    "btnAbrirEspera",
                  
                  label =
                    "Abrir simulador de espera",
                  
                  class =
                    paste(
                      "btn",
                      "btn-primary",
                      "btn-menu"
                    )
                  
                )
                
              )
              
            ),
            
            
            # =================================================
            # INVENTARIO
            # =================================================
            
            column(
              
              width = 6,
              
              
              div(
                
                class =
                  "menu-card card-inventario",
                
                
                div(
                  
                  class =
                    "menu-icon",
                  
                  "📦"
                  
                ),
                
                
                h3(
                  "Inventario"
                ),
                
                
                p(
                  paste(
                    "Simula el comportamiento",
                    "de un sistema de inventario,",
                    "demanda, punto de reorden,",
                    "pedidos y faltantes."
                  )
                ),
                
                
                actionButton(
                  
                  inputId =
                    "btnAbrirInventario",
                  
                  label =
                    "Abrir simulador de inventario",
                  
                  class =
                    paste(
                      "btn",
                      "btn-success",
                      "btn-menu"
                    )
                  
                )
                
              )
              
            )
            
          ),
          
          
          # ==================================================
          # PIE
          # ==================================================
          
          div(
            
            class =
              "principal-footer",
            
            p(
              "Sistema de Simulación y Validación"
            )
            
          )
          
        )
        
      )
      
    }
    
    
    # --------------------------------------------------------
    # PANTALLA DE ESPERA
    # --------------------------------------------------------
    
    else if (
      pantallaActual() ==
      "espera"
    ) {
      
      return(
        
        ventanaEsperaUI(
          "moduloEspera"
        )
        
      )
      
    }
    
    
    # --------------------------------------------------------
    # PANTALLA DE INVENTARIO
    # --------------------------------------------------------
    
    else if (
      pantallaActual() ==
      "inventario"
    ) {
      
      return(
        
        ventanaInventarioUI(
          "moduloInventario"
        )
        
      )
      
    }
    
  })
  
  
  # ==========================================================
  # ABRIR ESPERA
  # ==========================================================
  
  observeEvent(
    input$btnAbrirEspera,
    {
      
      pantallaActual(
        "espera"
      )
      
    },
    
    ignoreInit = TRUE
    
  )
  
  
  # ==========================================================
  # ABRIR INVENTARIO
  # ==========================================================
  
  observeEvent(
    input$btnAbrirInventario,
    {
      
      pantallaActual(
        "inventario"
      )
      
    },
    
    ignoreInit = TRUE
    
  )
  
  
  # ==========================================================
  # SERVIDOR DE ESPERA
  # ==========================================================
  
  ventanaEsperaServer(
    
    "moduloEspera",
    
    volverPrincipal =
      volverPrincipal
    
  )
  
  
  # ==========================================================
  # SERVIDOR DE INVENTARIO
  # ==========================================================
  #
  # Esta función estará disponible cuando creemos:
  #
  # ventanaInventario.R
  #
  # ==========================================================
  
  ventanaInventarioServer(
    
    "moduloInventario",
    
    volverPrincipal =
      volverPrincipal
    
  )
  
}

# ============================================================
# CREAR VENTANA PRINCIPAL
# ============================================================

crear_ventana_principal <- function() {
  
  ui <- fluidPage(
    
    tags$head(
      
      tags$title(
        "Sistema de Simulación"
      )
      
    ),
    
    ventanaPrincipalUI()
    
  )
  
  
  server <- function(
    input,
    output,
    session
  ) {
    
    ventanaPrincipalServer(
      input,
      output,
      session
    )
    
  }
  
  
  shinyApp(
    ui = ui,
    server = server
  )
}