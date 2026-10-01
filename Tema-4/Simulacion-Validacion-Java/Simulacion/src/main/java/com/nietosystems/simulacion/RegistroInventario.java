package com.nietosystems.simulacion;

public class RegistroInventario {

    private final int periodo;
    private final int inventarioInicial;
    private final int demanda;
    private final int pedido;
    private final int inventarioFinal;
    private final int faltante;

    public RegistroInventario(
            int periodo,
            int inventarioInicial,
            int demanda,
            int pedido,
            int inventarioFinal,
            int faltante) {

        this.periodo = periodo;
        this.inventarioInicial = inventarioInicial;
        this.demanda = demanda;
        this.pedido = pedido;
        this.inventarioFinal = inventarioFinal;
        this.faltante = faltante;
    }

    public int getPeriodo() {
        return periodo;
    }

    public int getInventarioInicial() {
        return inventarioInicial;
    }

    public int getDemanda() {
        return demanda;
    }

    public int getPedido() {
        return pedido;
    }

    public int getInventarioFinal() {
        return inventarioFinal;
    }

    public int getFaltante() {
        return faltante;
    }
}