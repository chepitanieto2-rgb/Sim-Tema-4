import tkinter as tk
from tkinter import ttk, messagebox

from Inventario import Inventario


class VentanaInventario:

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

        # Si se presiona la X de Windows,
        # regresar a la ventana principal
        if self.ventana_principal is not None:
            self.ventana.protocol(
                "WM_DELETE_WINDOW",
                self.volver_principal
            )

        self.ventana.title(
            "Simulador de Inventario"
        )

        # =====================================================
        # TAMAÑO ADAPTABLE DE LA VENTANA
        # =====================================================

        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Mantener un ancho cómodo sin ocupar toda la pantalla
        ancho_ventana = min(1100, ancho_pantalla - 40)

        # Aprovechar la altura disponible
        # dejando espacio para barra de tareas y márgenes
        alto_ventana = alto_pantalla - 80

        # Limitar altura en pantallas muy grandes
        alto_ventana = min(alto_ventana, 900)

        # Evitar tamaños demasiado pequeños
        alto_ventana = max(alto_ventana, 550)

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
        self.inventario = Inventario()

        # =====================================================
        # ESTILOS
        # =====================================================

        self.configurar_estilos()

        # =====================================================
        # CONSTRUIR INTERFAZ
        # =====================================================

        # Primero se crea el encabezado
        self.crear_encabezado()

        # Después se reserva el espacio del pie.
        # De esta manera SALIR siempre queda visible.
        self.crear_pie()

        # Finalmente el contenido ocupa todo
        # el espacio disponible entre ambos.
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
            bg="#2E7D32",
            height=95
        )

        encabezado.pack(
            fill="x",
            side="top"
        )

        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="SIMULADOR DE INVENTARIO",
            bg="#2E7D32",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            encabezado,
            text=(
                "Simulación y validación "
                "de un sistema de inventario"
            ),
            bg="#2E7D32",
            fg="#E8F5E9",
            font=("Arial", 11)
        ).pack()

    # =========================================================
    # PIE DE VENTANA
    # =========================================================

    def crear_pie(self):

        self.pie = tk.Frame(
            self.ventana,
            bg="#E8F5E9",
            height=55
        )

        self.pie.pack(
            fill="x",
            side="bottom"
        )

        # Impide que el pie se reduzca por el contenido
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

        # Permitir desplazamiento con la rueda del mouse
        self.canvas.bind_all(
            "<MouseWheel>",
            self.desplazar_mouse
        )

        # Secciones
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

        # FILA 1

        tk.Label(
            frame,
            text="Inventario inicial:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtInventarioInicial = ttk.Entry(
            frame,
            width=20
        )

        self.txtInventarioInicial.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Número de períodos:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtPeriodos = ttk.Entry(
            frame,
            width=20
        )

        self.txtPeriodos.grid(
            row=0,
            column=3,
            sticky="w",
            pady=7
        )

        # FILA 2

        tk.Label(
            frame,
            text="Demanda mínima:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtDemandaMinima = ttk.Entry(
            frame,
            width=20
        )

        self.txtDemandaMinima.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Demanda máxima:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtDemandaMaxima = ttk.Entry(
            frame,
            width=20
        )

        self.txtDemandaMaxima.grid(
            row=1,
            column=3,
            sticky="w",
            pady=7
        )

        # FILA 3

        tk.Label(
            frame,
            text="Punto de reorden:",
            bg="#F4F6F8"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtPuntoReorden = ttk.Entry(
            frame,
            width=20
        )

        self.txtPuntoReorden.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Cantidad de pedido:",
            bg="#F4F6F8"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.txtCantidadPedido = ttk.Entry(
            frame,
            width=20
        )

        self.txtCantidadPedido.grid(
            row=2,
            column=3,
            sticky="w",
            pady=7
        )

        # BOTONES

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
            bg="#388E3C",
            fg="white",
            activebackground="#2E7D32",
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
            padx=30
        )

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
            text="Inventario promedio",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lblInventarioPromedio = tk.Label(
            bloque1,
            text="0.00",
            bg="#F4F6F8",
            fg="#2E7D32",
            font=("Arial", 12)
        )

        self.lblInventarioPromedio.pack(
            anchor="w",
            pady=(5, 0)
        )

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
            text="Inventario mínimo",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lblInventarioMinimo = tk.Label(
            bloque2,
            text="0",
            bg="#F4F6F8",
            fg="#C00000",
            font=("Arial", 12)
        )

        self.lblInventarioMinimo.pack(
            anchor="w",
            pady=(5, 0)
        )

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
            text="Pedidos realizados",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lblPedidosRealizados = tk.Label(
            bloque3,
            text="0",
            bg="#F4F6F8",
            fg="#548235",
            font=("Arial", 12)
        )

        self.lblPedidosRealizados.pack(
            anchor="w",
            pady=(5, 0)
        )

        bloque4 = tk.Frame(
            frame,
            bg="#F4F6F8"
        )

        bloque4.pack(side="left")

        tk.Label(
            bloque4,
            text="Faltante total",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lblFaltanteTotal = tk.Label(
            bloque4,
            text="0",
            bg="#F4F6F8",
            fg="#7030A0",
            font=("Arial", 12)
        )

        self.lblFaltanteTotal.pack(
            anchor="w",
            pady=(5, 0)
        )

        estado = tk.Frame(
            self.frame_contenido,
            bg="#F4F6F8"
        )

        estado.pack(
            fill="x",
            padx=30,
            pady=(15, 5)
        )

        tk.Label(
            estado,
            text="Estado del inventario:",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.lblEstadoInventario = tk.Label(
            estado,
            text="Ejecute una simulación.",
            bg="#F4F6F8",
            fg="#333333",
            justify="left",
            anchor="w",
            font=("Arial", 10),
            wraplength=950
        )

        self.lblEstadoInventario.pack(
            fill="x",
            pady=(5, 0)
        )

    # =========================================================
    # TABLA
    # =========================================================

    def crear_tabla(self):

        ttk.Separator(
            self.frame_contenido,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=30,
            pady=(15, 0)
        )

        self.titulo_seccion(
            "DETALLE DEL INVENTARIO"
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
            "periodo",
            "inicial",
            "demanda",
            "pedido",
            "final",
            "faltante"
        )

        self.tablaInventario = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=9
        )

        encabezados = {
            "periodo": "Período",
            "inicial": "Inventario inicial",
            "demanda": "Demanda",
            "pedido": "Pedido",
            "final": "Inventario final",
            "faltante": "Faltante"
        }

        anchos = {
            "periodo": 90,
            "inicial": 150,
            "demanda": 120,
            "pedido": 120,
            "final": 150,
            "faltante": 120
        }

        for columna in columnas:

            self.tablaInventario.heading(
                columna,
                text=encabezados[columna]
            )

            self.tablaInventario.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        scroll_tabla = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tablaInventario.yview
        )

        self.tablaInventario.configure(
            yscrollcommand=scroll_tabla.set
        )

        self.tablaInventario.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_tabla.pack(
            side="right",
            fill="y"
        )

    # =========================================================
    # VALIDACIÓN ESTADÍSTICA
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

        tk.Label(
            frame,
            text="Valor de referencia:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=0,
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
            column=1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )

        tk.Label(
            frame,
            text="Nivel de significancia:",
            bg="#F4F6F8"
        ).grid(
            row=0,
            column=2,
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
            row=0,
            column=3,
            sticky="w",
            pady=7
        )

        tk.Label(
            frame,
            text="Prueba estadística:",
            bg="#F4F6F8"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        tk.Label(
            frame,
            text="t de una muestra",
            bg="#F4F6F8",
            fg="#2E7D32",
            font=("Arial", 10, "bold")
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=7
        )

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
            text="Estadístico t",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

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

        bloque2.pack(side="left")

        tk.Label(
            bloque2,
            text="p-valor",
            bg="#F4F6F8",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

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
        ).pack(anchor="w")

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
    # EJECUTAR SIMULACIÓN
    # =========================================================

    def simular(self):

        try:

            inventarioInicial = int(
                self.txtInventarioInicial.get()
            )

            periodos = int(
                self.txtPeriodos.get()
            )

            demandaMinima = int(
                self.txtDemandaMinima.get()
            )

            demandaMaxima = int(
                self.txtDemandaMaxima.get()
            )

            puntoReorden = int(
                self.txtPuntoReorden.get()
            )

            cantidadPedido = int(
                self.txtCantidadPedido.get()
            )

            resultado = self.inventario.simular(
                inventarioInicial,
                periodos,
                demandaMinima,
                demandaMaxima,
                puntoReorden,
                cantidadPedido
            )

            for fila in self.tablaInventario.get_children():
                self.tablaInventario.delete(fila)

            for registro in resultado["registros"]:

                self.tablaInventario.insert(
                    "",
                    "end",
                    values=(
                        registro.getPeriodo(),
                        registro.getInventarioInicial(),
                        registro.getDemanda(),
                        registro.getPedido(),
                        registro.getInventarioFinal(),
                        registro.getFaltante()
                    )
                )

            self.lblInventarioPromedio.config(
                text=f"{resultado['inventarioPromedio']:.2f}"
            )

            self.lblInventarioMinimo.config(
                text=str(resultado["inventarioMinimo"])
            )

            self.lblPedidosRealizados.config(
                text=str(resultado["pedidosRealizados"])
            )

            self.lblFaltanteTotal.config(
                text=str(resultado["faltanteTotal"])
            )

            self.lblEstadoInventario.config(
                text=resultado["estadoInventario"]
            )

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
    # VALIDACIÓN ESTADÍSTICA
    # =========================================================

    def validar_simulacion(self):

        try:

            referencia = float(
                self.txtReferencia.get()
            )

            significancia = float(
                self.txtSignificancia.get()
            )

            resultado = self.inventario.validarSimulacion(
                referencia,
                significancia
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
            self.txtInventarioInicial,
            self.txtPeriodos,
            self.txtDemandaMinima,
            self.txtDemandaMaxima,
            self.txtPuntoReorden,
            self.txtCantidadPedido,
            self.txtReferencia
        )

        for campo in campos:
            campo.delete(
                0,
                tk.END
            )

        self.txtSignificancia.delete(
            0,
            tk.END
        )

        self.txtSignificancia.insert(
            0,
            "0.05"
        )

        self.lblInventarioPromedio.config(
            text="0.00"
        )

        self.lblInventarioMinimo.config(
            text="0"
        )

        self.lblPedidosRealizados.config(
            text="0"
        )

        self.lblFaltanteTotal.config(
            text="0"
        )

        self.lblEstadoInventario.config(
            text="Ejecute una simulación."
        )

        for fila in self.tablaInventario.get_children():
            self.tablaInventario.delete(fila)

        self.inventario.registros.clear()
        self.inventario.datosValidacion.clear()

        self.limpiar_resultados_validacion()

        self.canvas.yview_moveto(0)

        self.txtInventarioInicial.focus_set()

    # =========================================================
    # REGRESAR A LA VENTANA PRINCIPAL
    # =========================================================

    def volver_principal(self):

        # Evitar que el evento de la rueda quede asociado
        # a una ventana que ya fue destruida
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except Exception:
            pass

        self.ventana.destroy()

        if self.ventana_principal is not None:

            self.ventana_principal.deiconify()
            self.ventana_principal.lift()
            self.ventana_principal.focus_force()


# =============================================================
# PRUEBA INDIVIDUAL
# =============================================================

if __name__ == "__main__":

    app = VentanaInventario()

    app.ventana.mainloop()