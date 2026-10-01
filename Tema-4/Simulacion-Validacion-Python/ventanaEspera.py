import tkinter as tk
from tkinter import ttk, messagebox

from Espera import Espera


class VentanaEspera:

    def __init__(
            self,
            ventana=None,
            ventana_principal=None
    ):

        # =====================================================
        # VENTANA
        # =====================================================

        if ventana is None:
            self.ventana = tk.Tk()
            self.ventana_propia = True
        else:
            self.ventana = ventana
            self.ventana_propia = False

        # Guardar referencia de la ventana principal
        self.ventana_principal = ventana_principal

        # Si se utiliza la X de Windows,
        # regresar también a la ventana principal
        if self.ventana_principal is not None:
            self.ventana.protocol(
                "WM_DELETE_WINDOW",
                self.volver_principal
            )

        self.ventana.title(
            "Simulador de Línea de Espera"
        )

        # =====================================================
        # TAMAÑO ADAPTABLE DE LA VENTANA
        # =====================================================

        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Mantener un ancho cómodo sin ocupar toda la pantalla
        ancho_ventana = min(
            1100,
            ancho_pantalla - 40
        )

        # Aprovechar la altura disponible
        # dejando espacio para barra de tareas y márgenes
        alto_ventana = alto_pantalla - 80

        # Evitar una altura excesiva en monitores grandes
        alto_ventana = min(
            alto_ventana,
            900
        )

        # Evitar una altura demasiado pequeña
        alto_ventana = max(
            alto_ventana,
            550
        )

        # Centrar horizontalmente
        posicion_x = max(
            (ancho_pantalla - ancho_ventana) // 2,
            0
        )

        # Pequeño margen superior
        posicion_y = 10

        self.ventana.geometry(
            f"{ancho_ventana}x{alto_ventana}"
            f"+{posicion_x}+{posicion_y}"
        )

        self.ventana.minsize(
            900,
            550
        )

        self.ventana.configure(
            bg="#F4F6F8"
        )

        # Objeto que contiene la lógica
        self.espera = Espera()

        # =====================================================
        # ESTILOS
        # =====================================================

        self.configurar_estilos()

        # =====================================================
        # CONSTRUIR INTERFAZ
        # =====================================================

        # Primero encabezado
        self.crear_encabezado()

        # Después pie para reservar siempre
        # el espacio del botón SALIR
        self.crear_pie()

        # Finalmente el contenido ocupa
        # todo el espacio restante
        self.crear_contenido()

    # =========================================================
    # ESTILOS
    # =========================================================

    def configurar_estilos(self):

        estilo = ttk.Style()

        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure(
            "Treeview",
            rowheight=27,
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        encabezado = tk.Frame(
            self.ventana,
            bg="#1F4E78",
            height=95
        )

        encabezado.pack(
            fill="x",
            side="top"
        )

        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="SIMULADOR DE LÍNEA DE ESPERA",
            bg="#1F4E78",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            encabezado,
            text="Simulación de llegada y atención de clientes",
            bg="#1F4E78",
            fg="#D9EAF7",
            font=("Arial", 11)
        ).pack()

    # =========================================================
    # PIE DE VENTANA
    # =========================================================

    def crear_pie(self):

        self.pie = tk.Frame(
            self.ventana,
            bg="#D9E1F2",
            height=55
        )

        self.pie.pack(
            fill="x",
            side="bottom"
        )

        # Mantener fija la altura del pie
        self.pie.pack_propagate(False)

        tk.Button(
            self.pie,
            text="SALIR",
            command=self.volver_principal,
            width=14,
            height=1,
            bg="#C00000",
            fg="white",
            activebackground="#980000",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=20,
            pady=10
        )

    # =========================================================
    # CONTENIDO CON SCROLL
    # =========================================================

    def crear_contenido(self):

        contenedor = tk.Frame(
            self.ventana,
            bg="#F4F6F8"
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            contenedor,
            bg="#F4F6F8",
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=self.canvas.yview
        )

        self.frame_contenido = tk.Frame(
            self.canvas,
            bg="#F4F6F8"
        )

        self.frame_contenido.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame_contenido,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            self.ajustar_ancho_contenido
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Permitir desplazamiento con
        # la rueda del mouse
        self.canvas.bind_all(
            "<MouseWheel>",
            self.desplazar_mouse
        )

        # Crear secciones
        self.crear_parametros()
        self.crear_resultados()
        self.crear_tabla()
        self.crear_validacion()

    def ajustar_ancho_contenido(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def desplazar_mouse(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =========================================================
    # TÍTULO DE SECCIÓN
    # =========================================================

    def titulo_seccion(self, texto):

        tk.Label(
            self.frame_contenido,
            text=texto,
            bg="#F4F6F8",
            fg="#1F1F1F",
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

    # =========================================================
    # PARÁMETROS
    # =========================================================

    def crear_parametros(self):

        self.titulo_seccion(
            "PARÁMETROS DE LA SIMULACIÓN"
        )

        frame = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        frame.pack(
            fill="x",
            padx=30
        )

        # -----------------------------------------------------
        # FILA 1
        # -----------------------------------------------------

        tk.Label(
            frame,
            text="Número de clientes:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtClientes = ttk.Entry(
            frame,
            width=20
        )

        self.txtClientes.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Número de servidores:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtServidores = ttk.Entry(
            frame,
            width=20
        )

        self.txtServidores.grid(
            row=0,
            column=3,
            sticky="w",
            pady=7
        )

        # -----------------------------------------------------
        # FILA 2
        # -----------------------------------------------------

        tk.Label(
            frame,
            text="Tiempo mínimo de llegada:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtLlegadaMinima = ttk.Entry(
            frame,
            width=20
        )

        self.txtLlegadaMinima.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Tiempo máximo de llegada:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtLlegadaMaxima = ttk.Entry(
            frame,
            width=20
        )

        self.txtLlegadaMaxima.grid(
            row=1,
            column=3,
            sticky="w",
            pady=7
        )

        # -----------------------------------------------------
        # FILA 3
        # -----------------------------------------------------

        tk.Label(
            frame,
            text="Tiempo mínimo de servicio:",
            bg="#F4F6F8"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtServicioMinimo = ttk.Entry(
            frame,
            width=20
        )

        self.txtServicioMinimo.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Tiempo máximo de servicio:",
            bg="#F4F6F8"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtServicioMaximo = ttk.Entry(
            frame,
            width=20
        )

        self.txtServicioMaximo.grid(
            row=2,
            column=3,
            sticky="w",
            pady=7
        )

        # -----------------------------------------------------
        # BOTONES
        # -----------------------------------------------------

        botones = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=(15, 5)
        )

        tk.Button(
            botones,
            text="INICIAR SIMULACIÓN",
            command=self.simular,
            width=22,
            height=2,
            bg="#2E75B6",
            fg="white",
            activebackground="#245F96",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Button(
            botones,
            text="LIMPIAR",
            command=self.limpiar,
            width=14,
            height=2,
            bg="#7F8C8D",
            fg="white",
            activebackground="#626E6F",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=15
        )

    # =========================================================
    # RESULTADOS
    # =========================================================

    def crear_resultados(self):

        ttk.Separator(
            self.frame_contenido,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=30,
            pady=(15, 0)
        )

        self.titulo_seccion(
            "RESULTADOS DE LA SIMULACIÓN"
        )

        frame = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )

        # Espera promedio

        bloque1 = tk.Frame(
            frame,
            bg="#F4F6F8"
        )

        bloque1.pack(
            side="left",
            padx=(0, 45)
        )

        tk.Label(
            bloque1,
            text="Espera promedio",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblEsperaPromedio = tk.Label(
            bloque1,
            text="0.00 min",
            bg="#F4F6F8",
            fg="#2E75B6",
            font=("Arial", 12)
        )

        self.lblEsperaPromedio.pack(
            anchor="w",
            pady=(5, 0)
        )

        # Espera máxima

        bloque2 = tk.Frame(
            frame,
            bg="#F4F6F8"
        )

        bloque2.pack(
            side="left",
            padx=(0, 45)
        )

        tk.Label(
            bloque2,
            text="Espera máxima",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblEsperaMaxima = tk.Label(
            bloque2,
            text="0.00 min",
            bg="#F4F6F8",
            fg="#C00000",
            font=("Arial", 12)
        )

        self.lblEsperaMaxima.pack(
            anchor="w",
            pady=(5, 0)
        )

        # Clientes que esperaron

        bloque3 = tk.Frame(
            frame,
            bg="#F4F6F8"
        )

        bloque3.pack(
            side="left",
            padx=(0, 45)
        )

        tk.Label(
            bloque3,
            text="Clientes que esperaron",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblClientesEsperaron = tk.Label(
            bloque3,
            text="0",
            bg="#F4F6F8",
            fg="#548235",
            font=("Arial", 12)
        )

        self.lblClientesEsperaron.pack(
            anchor="w",
            pady=(5, 0)
        )

        # Utilización

        bloque4 = tk.Frame(
            frame,
            bg="#F4F6F8"
        )

        bloque4.pack(
            side="left"
        )

        tk.Label(
            bloque4,
            text="Utilización de servidores",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblUtilizacion = tk.Label(
            bloque4,
            text="0.00 %",
            bg="#F4F6F8",
            fg="#7030A0",
            font=("Arial", 12)
        )

        self.lblUtilizacion.pack(
            anchor="w",
            pady=(5, 0)
        )

    # =========================================================
    # TABLA DE CLIENTES
    # =========================================================

    def crear_tabla(self):

        ttk.Separator(
            self.frame_contenido,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=30,
            pady=(10, 0)
        )

        self.titulo_seccion(
            "DETALLE DE CLIENTES"
        )

        frame_tabla = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=30
        )

        columnas = (
            "cliente",
            "servidor",
            "llegada",
            "servicio",
            "espera",
            "inicio",
            "fin"
        )

        self.tablaClientes = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=9
        )

        encabezados = {
            "cliente": "Cliente",
            "servidor": "Servidor",
            "llegada": "Llegada",
            "servicio": "Servicio",
            "espera": "Espera",
            "inicio": "Inicio",
            "fin": "Fin"
        }

        anchos = {
            "cliente": 80,
            "servidor": 90,
            "llegada": 120,
            "servicio": 120,
            "espera": 120,
            "inicio": 120,
            "fin": 120
        }

        for columna in columnas:

            self.tablaClientes.heading(
                columna,
                text=encabezados[columna]
            )

            self.tablaClientes.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        scroll_tabla = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tablaClientes.yview
        )

        self.tablaClientes.configure(
            yscrollcommand=scroll_tabla.set
        )

        self.tablaClientes.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_tabla.pack(
            side="right",
            fill="y"
        )

    # =========================================================
    # VALIDACIÓN
    # =========================================================

    def crear_validacion(self):

        ttk.Separator(
            self.frame_contenido,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=30,
            pady=(20, 0)
        )

        self.titulo_seccion(
            "VALIDACIÓN DEL SIMULADOR"
        )

        frame = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        frame.pack(
            fill="x",
            padx=30
        )

        # Tipo de prueba

        tk.Label(
            frame,
            text="Tipo de prueba:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.cmbTipoPrueba = ttk.Combobox(
            frame,
            width=35,
            state="readonly"
        )

        self.cmbTipoPrueba["values"] = (
            "Prueba paramétrica - t de una muestra",
            "Prueba no paramétrica - Wilcoxon"
        )

        self.cmbTipoPrueba.current(0)

        self.cmbTipoPrueba.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        # Valor de referencia

        tk.Label(
            frame,
            text="Valor de referencia:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtReferencia = ttk.Entry(
            frame,
            width=20
        )

        self.txtReferencia.grid(
            row=0,
            column=3,
            sticky="w",
            pady=7
        )

        # Significancia

        tk.Label(
            frame,
            text="Nivel de significancia:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtSignificancia = ttk.Entry(
            frame,
            width=20
        )

        self.txtSignificancia.insert(
            0,
            "0.05"
        )

        self.txtSignificancia.grid(
            row=1,
            column=1,
            sticky="w",
            pady=7
        )

        # Botón validar

        tk.Button(
            self.frame_contenido,
            text="EJECUTAR PRUEBA DE VALIDACIÓN",
            command=self.validar_simulacion,
            width=30,
            height=2,
            bg="#548235",
            fg="white",
            activebackground="#42692A",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 15)
        )

        # Resultados

        resultados = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        resultados.pack(
            fill="x",
            padx=30
        )

        bloque1 = tk.Frame(
            resultados,
            bg="#F4F6F8"
        )

        bloque1.pack(
            side="left",
            padx=(0, 70)
        )

        tk.Label(
            bloque1,
            text="Estadístico",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblEstadistico = tk.Label(
            bloque1,
            text="Pendiente",
            bg="#F4F6F8",
            font=("Arial", 11)
        )

        self.lblEstadistico.pack(
            anchor="w",
            pady=(5, 0)
        )

        bloque2 = tk.Frame(
            resultados,
            bg="#F4F6F8"
        )

        bloque2.pack(
            side="left"
        )

        tk.Label(
            bloque2,
            text="p-valor",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblPValor = tk.Label(
            bloque2,
            text="Pendiente",
            bg="#F4F6F8",
            font=("Arial", 11)
        )

        self.lblPValor.pack(
            anchor="w",
            pady=(5, 0)
        )

        # Conclusión

        conclusion = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        conclusion.pack(
            fill="x",
            padx=30,
            pady=(15, 30)
        )

        tk.Label(
            conclusion,
            text="Conclusión",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.lblConclusion = tk.Label(
            conclusion,
            text="Ejecute una prueba de validación.",
            bg="#F4F6F8",
            font=("Arial", 10),
            justify="left",
            anchor="w",
            wraplength=950
        )

        self.lblConclusion.pack(
            fill="x",
            pady=(5, 0)
        )

    # =========================================================
    # SIMULAR
    # =========================================================

    def simular(self):

        try:

            cantidadClientes = int(
                self.txtClientes.get()
            )

            cantidadServidores = int(
                self.txtServidores.get()
            )

            llegadaMinima = float(
                self.txtLlegadaMinima.get()
            )

            llegadaMaxima = float(
                self.txtLlegadaMaxima.get()
            )

            servicioMinimo = float(
                self.txtServicioMinimo.get()
            )

            servicioMaximo = float(
                self.txtServicioMaximo.get()
            )

            resultado = self.espera.simular(
                cantidadClientes,
                cantidadServidores,
                llegadaMinima,
                llegadaMaxima,
                servicioMinimo,
                servicioMaximo
            )

            # Limpiar tabla anterior

            for fila in self.tablaClientes.get_children():
                self.tablaClientes.delete(fila)

            # Llenar tabla

            for cliente in resultado["clientes"]:

                self.tablaClientes.insert(
                    "",
                    "end",
                    values=(
                        cliente.getNumero(),
                        cliente.getServidor(),
                        f"{cliente.getLlegada():.2f}",
                        f"{cliente.getServicio():.2f}",
                        f"{cliente.getEspera():.2f}",
                        f"{cliente.getInicio():.2f}",
                        f"{cliente.getFin():.2f}"
                    )
                )

            # Mostrar resultados

            self.lblEsperaPromedio.config(
                text=(
                    f"{resultado['esperaPromedio']:.2f} min"
                )
            )

            self.lblEsperaMaxima.config(
                text=(
                    f"{resultado['esperaMaxima']:.2f} min"
                )
            )

            self.lblClientesEsperaron.config(
                text=str(
                    resultado["clientesEsperaron"]
                )
            )

            self.lblUtilizacion.config(
                text=(
                    f"{resultado['utilizacion']:.2f} %"
                )
            )

            # Una simulación nueva elimina
            # la validación anterior
            self.limpiar_resultados_validacion()

        except ValueError as error:

            messagebox.showerror(
                "Datos inválidos",
                str(error),
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Ocurrió un error durante "
                    f"la simulación:\n{error}"
                ),
                parent=self.ventana
            )

    # =========================================================
    # VALIDAR SIMULACIÓN
    # =========================================================

    def validar_simulacion(self):

        try:

            referencia = float(
                self.txtReferencia.get()
            )

            significancia = float(
                self.txtSignificancia.get()
            )

            tipoPrueba = (
                self.cmbTipoPrueba.get()
            )

            resultado = (
                self.espera.validarSimulacion(
                    referencia,
                    significancia,
                    tipoPrueba
                )
            )

            self.lblEstadistico.config(
                text=resultado["estadistico"]
            )

            self.lblPValor.config(
                text=resultado["pValor"]
            )

            self.lblConclusion.config(
                text=resultado["conclusion"]
            )

        except ValueError as error:

            messagebox.showerror(
                "Datos inválidos",
                str(error),
                parent=self.ventana
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Ocurrió un error durante "
                    f"la validación:\n{error}"
                ),
                parent=self.ventana
            )

    # =========================================================
    # LIMPIAR RESULTADOS DE VALIDACIÓN
    # =========================================================

    def limpiar_resultados_validacion(self):

        self.lblEstadistico.config(
            text="Pendiente"
        )

        self.lblPValor.config(
            text="Pendiente"
        )

        self.lblConclusion.config(
            text="Ejecute una prueba de validación."
        )

    # =========================================================
    # LIMPIAR
    # =========================================================

    def limpiar(self):

        campos = (
            self.txtClientes,
            self.txtServidores,
            self.txtLlegadaMinima,
            self.txtLlegadaMaxima,
            self.txtServicioMinimo,
            self.txtServicioMaximo,
            self.txtReferencia
        )

        for campo in campos:

            campo.delete(
                0,
                tk.END
            )

        # Significancia vuelve a 0.05

        self.txtSignificancia.delete(
            0,
            tk.END
        )

        self.txtSignificancia.insert(
            0,
            "0.05"
        )

        # Primera prueba seleccionada

        self.cmbTipoPrueba.current(0)

        # Resultados principales

        self.lblEsperaPromedio.config(
            text="0.00 min"
        )

        self.lblEsperaMaxima.config(
            text="0.00 min"
        )

        self.lblClientesEsperaron.config(
            text="0"
        )

        self.lblUtilizacion.config(
            text="0.00 %"
        )

        # Limpiar tabla

        for fila in self.tablaClientes.get_children():
            self.tablaClientes.delete(fila)

        # Limpiar datos internos

        self.espera.clientes.clear()
        self.espera.tiemposEspera.clear()

        # Limpiar validación

        self.limpiar_resultados_validacion()

        # Regresar scroll arriba

        self.canvas.yview_moveto(0)

        # Cursor en primer campo

        self.txtClientes.focus_set()

    # =========================================================
    # REGRESAR A VENTANA PRINCIPAL
    # =========================================================

    def volver_principal(self):

        # Eliminar asociación de la rueda del mouse
        # antes de destruir esta ventana
        try:
            self.canvas.unbind_all(
                "<MouseWheel>"
            )
        except Exception:
            pass

        # Cerrar ventana secundaria
        self.ventana.destroy()

        # Mostrar nuevamente la principal
        if self.ventana_principal is not None:

            self.ventana_principal.deiconify()

            self.ventana_principal.lift()

            self.ventana_principal.focus_force()


# =============================================================
# PRUEBA INDIVIDUAL
# =============================================================

if __name__ == "__main__":

    app = VentanaEspera()

    app.ventana.mainloop()