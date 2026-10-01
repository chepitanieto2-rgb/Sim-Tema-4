package com.nietosystems.simulacion;

public class Cliente {

    private int numero;
    private int servidor;
    private double llegada;
    private double servicio;
    private double espera;
    private double inicio;
    private double fin;

    public Cliente(
            int numero,
            int servidor,
            double llegada,
            double servicio,
            double espera,
            double inicio,
            double fin
    ) {
        this.numero = numero;
        this.servidor = servidor;
        this.llegada = llegada;
        this.servicio = servicio;
        this.espera = espera;
        this.inicio = inicio;
        this.fin = fin;
    }

    public int getNumero() {
        return numero;
    }

    public int getServidor() {
        return servidor;
    }

    public double getLlegada() {
        return llegada;
    }

    public double getServicio() {
        return servicio;
    }

    public double getEspera() {
        return espera;
    }

    public double getInicio() {
        return inicio;
    }

    public double getFin() {
        return fin;
    }
}