import tkinter as tk
from tkinter import messagebox

from ventanaEspera import VentanaEspera
from ventanaInventario import VentanaInventario


class VentanaPrincipal:

    def __init__(self, ventana):

        # =====================================================
        # VENTANA PRINCIPAL
        # =====================================================

        self.ventana = ventana

        self.ventana.title(
            "Simulación y Validación"
        )

        self.ventana.geometry(
            "900x600"
        )

        self.ventana.minsize(
            800,
            550
        )

        self.ventana.configure(
            bg="#F4F6F8"
        )

        # Centrar la ventana
        self.centrar_ventana(
            900,
            600
        )

        # =====================================================
        # CONSTRUIR INTERFAZ
        # =====================================================

        self.crear_encabezado()
        self.crear_contenido()
        self.crear_pie()

    # =========================================================
    # CENTRAR VENTANA
    # =========================================================

    def centrar_ventana(self, ancho, alto):

        ancho_pantalla = (
            self.ventana.winfo_screenwidth()
        )

        alto_pantalla = (
            self.ventana.winfo_screenheight()
        )

        x = int(
            (ancho_pantalla / 2)
            -
            (ancho / 2)
        )

        y = int(
            (alto_pantalla / 2)
            -
            (alto / 2)
        )

        self.ventana.geometry(
            f"{ancho}x{alto}+{x}+{y}"
        )

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        encabezado = tk.Frame(
            self.ventana,
            bg="#263238",
            height=130
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(
            False
        )

        tk.Label(
            encabezado,
            text="SIMULACIÓN Y VALIDACIÓN",
            bg="#263238",
            fg="white",
            font=(
                "Arial",
                24,
                "bold"
            )
        ).pack(
            pady=(25, 5)
        )

        tk.Label(
            encabezado,
            text=(
                "Sistema de simulación "
                "de eventos discretos"
            ),
            bg="#263238",
            fg="#CFD8DC",
            font=(
                "Arial",
                12
            )
        ).pack()

    # =========================================================
    # CONTENIDO PRINCIPAL
    # =========================================================

    def crear_contenido(self):

        contenido = tk.Frame(
            self.ventana,
            bg="#F4F6F8"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=30
        )

        # -----------------------------------------------------
        # INSTRUCCIÓN
        # -----------------------------------------------------

        tk.Label(
            contenido,
            text="Seleccione el tipo de simulación",
            bg="#F4F6F8",
            fg="#333333",
            font=(
                "Arial",
                16,
                "bold"
            )
        ).pack(
            pady=(5, 25)
        )

        # -----------------------------------------------------
        # CONTENEDOR DE OPCIONES
        # -----------------------------------------------------

        opciones = tk.Frame(
            contenido,
            bg="#F4F6F8"
        )

        opciones.pack(
            expand=True
        )

        # =====================================================
        # TARJETA LÍNEA DE ESPERA
        # =====================================================

        tarjeta_espera = tk.Frame(
            opciones,
            bg="white",
            width=330,
            height=260,
            bd=1,
            relief="solid"
        )

        tarjeta_espera.grid(
            row=0,
            column=0,
            padx=20,
            pady=10
        )

        tarjeta_espera.grid_propagate(
            False
        )

        tk.Label(
            tarjeta_espera,
            text="LÍNEA DE ESPERA",
            bg="white",
            fg="#1F4E78",
            font=(
                "Arial",
                17,
                "bold"
            )
        ).pack(
            pady=(30, 12)
        )

        tk.Label(
            tarjeta_espera,
            text=(
                "Simula la llegada y atención\n"
                "de clientes mediante uno o\n"
                "varios servidores."
            ),
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                11
            ),
            justify="center"
        ).pack(
            pady=(0, 25)
        )

        tk.Button(
            tarjeta_espera,
            text="ABRIR SIMULADOR",
            command=self.abrir_espera,
            width=20,
            height=2,
            bg="#2E75B6",
            fg="white",
            activebackground="#245F96",
            activeforeground="white",
            font=(
                "Arial",
                10,
                "bold"
            ),
            relief="flat",
            cursor="hand2"
        ).pack()

        # =====================================================
        # TARJETA INVENTARIO
        # =====================================================

        tarjeta_inventario = tk.Frame(
            opciones,
            bg="white",
            width=330,
            height=260,
            bd=1,
            relief="solid"
        )

        tarjeta_inventario.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        tarjeta_inventario.grid_propagate(
            False
        )

        tk.Label(
            tarjeta_inventario,
            text="INVENTARIO",
            bg="white",
            fg="#2E7D32",
            font=(
                "Arial",
                17,
                "bold"
            )
        ).pack(
            pady=(30, 12)
        )

        tk.Label(
            tarjeta_inventario,
            text=(
                "Simula el comportamiento\n"
                "de un sistema de inventario\n"
                "y sus puntos de reorden."
            ),
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                11
            ),
            justify="center"
        ).pack(
            pady=(0, 25)
        )

        tk.Button(
            tarjeta_inventario,
            text="ABRIR SIMULADOR",
            command=self.abrir_inventario,
            width=20,
            height=2,
            bg="#388E3C",
            fg="white",
            activebackground="#2E7D32",
            activeforeground="white",
            font=(
                "Arial",
                10,
                "bold"
            ),
            relief="flat",
            cursor="hand2"
        ).pack()

    # =========================================================
    # ABRIR LÍNEA DE ESPERA
    # =========================================================

    def abrir_espera(self):

        try:

            # Ocultar la ventana principal
            self.ventana.withdraw()

            # Crear ventana secundaria
            nueva_ventana = tk.Toplevel(
                self.ventana
            )

            # Abrir simulador y enviar referencia
            # de la ventana principal
            VentanaEspera(
                nueva_ventana,
                self.ventana
            )

        except Exception as error:

            # Si ocurre un error,
            # volver a mostrar la principal
            self.ventana.deiconify()

            messagebox.showerror(
                "Error",
                (
                    "No fue posible abrir el "
                    "simulador de línea de espera.\n\n"
                    f"{error}"
                ),
                parent=self.ventana
            )

    # =========================================================
    # ABRIR INVENTARIO
    # =========================================================

    def abrir_inventario(self):

        try:

            # Ocultar la ventana principal
            self.ventana.withdraw()

            # Crear ventana secundaria
            nueva_ventana = tk.Toplevel(
                self.ventana
            )

            # Abrir simulador y enviar referencia
            # de la ventana principal
            VentanaInventario(
                nueva_ventana,
                self.ventana
            )

        except Exception as error:

            # Si ocurre un error,
            # volver a mostrar la principal
            self.ventana.deiconify()

            messagebox.showerror(
                "Error",
                (
                    "No fue posible abrir el "
                    "simulador de inventario.\n\n"
                    f"{error}"
                ),
                parent=self.ventana
            )

    # =========================================================
    # PIE DE VENTANA
    # =========================================================

    def crear_pie(self):

        pie = tk.Frame(
            self.ventana,
            bg="#ECEFF1",
            height=55
        )

        pie.pack(
            fill="x",
            side="bottom"
        )

        pie.pack_propagate(
            False
        )

        tk.Label(
            pie,
            text=(
                "Sistema de Simulación "
                "y Validación"
            ),
            bg="#ECEFF1",
            fg="#607D8B",
            font=(
                "Arial",
                9
            )
        ).pack(
            side="left",
            padx=20
        )

        # Este botón SÍ cierra todo el programa
        tk.Button(
            pie,
            text="SALIR",
            command=self.salir,
            width=12,
            bg="#C62828",
            fg="white",
            activebackground="#A61F1F",
            activeforeground="white",
            font=(
                "Arial",
                10,
                "bold"
            ),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=20,
            pady=10
        )

    # =========================================================
    # SALIR DEL PROGRAMA
    # =========================================================

    def salir(self):

        respuesta = messagebox.askyesno(
            "Salir",
            "¿Desea cerrar el programa?",
            parent=self.ventana
        )

        if respuesta:
            self.ventana.destroy()


# =============================================================
# PRUEBA INDIVIDUAL
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = VentanaPrincipal(
        root
    )

    root.mainloop()