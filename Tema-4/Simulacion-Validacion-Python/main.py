import tkinter as tk

from ventanaPrincipal import VentanaPrincipal


def main():

    # =========================================================
    # CREAR VENTANA PRINCIPAL
    # =========================================================

    root = tk.Tk()

    # Crear la interfaz principal
    VentanaPrincipal(root)

    # =========================================================
    # INICIAR APLICACIÓN
    # =========================================================

    root.mainloop()


# =============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================

if __name__ == "__main__":

    main()