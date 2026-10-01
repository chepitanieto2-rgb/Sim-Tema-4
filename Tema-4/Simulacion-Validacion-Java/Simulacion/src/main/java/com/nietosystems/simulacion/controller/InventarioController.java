package com.nietosystems.simulacion.controller;

import com.nietosystems.simulacion.RegistroInventario;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class InventarioController {

    // =========================
    // CAMPOS DE ENTRADA
    // =========================

    @FXML
    private TextField txtInventarioInicial;

    @FXML
    private TextField txtPeriodos;

    @FXML
    private TextField txtDemandaMinima;

    @FXML
    private TextField txtDemandaMaxima;

    @FXML
    private TextField txtPuntoReorden;

    @FXML
    private TextField txtCantidadPedido;


    // =========================
    // RESULTADOS
    // =========================

    @FXML
    private Label lblInventarioPromedio;

    @FXML
    private Label lblInventarioMinimo;

    @FXML
    private Label lblInventarioResurtido;

    @FXML
    private Label lblFaltanteTotal;

    @FXML
    private Label lblEstadoInventario;


    // =========================
    // TABLA
    // =========================

    @FXML
    private TableView<RegistroInventario> tablaInventario;

    @FXML
    private TableColumn<RegistroInventario, Integer> colPeriodo;

    @FXML
    private TableColumn<RegistroInventario, Integer> colInventarioInicial;

    @FXML
    private TableColumn<RegistroInventario, Integer> colDemanda;

    @FXML
    private TableColumn<RegistroInventario, Integer> colPedido;

    @FXML
    private TableColumn<RegistroInventario, Integer> colInventarioFinal;

    @FXML
    private TableColumn<RegistroInventario, Integer> colFaltante;


    // =========================
    // VALIDACIÓN
    // =========================

    @FXML
    private ComboBox<String> cmbTipoPrueba;

    @FXML
    private TextField txtReferencia;

    @FXML
    private TextField txtSignificancia;

    @FXML
    private Label lblEstadistico;

    @FXML
    private Label lblPValor;

    @FXML
    private Label lblConclusion;


    private final ObservableList<RegistroInventario> registros =
            FXCollections.observableArrayList();

    private final List<Double> datosValidacion =
            new ArrayList<>();

    private final Random random = new Random();


    // =========================
    // INICIALIZACIÓN
    // =========================

    @FXML
    public void initialize() {

        colPeriodo.setCellValueFactory(
                new PropertyValueFactory<>("periodo")
        );

        colInventarioInicial.setCellValueFactory(
                new PropertyValueFactory<>("inventarioInicial")
        );

        colDemanda.setCellValueFactory(
                new PropertyValueFactory<>("demanda")
        );

        colPedido.setCellValueFactory(
                new PropertyValueFactory<>("pedido")
        );

        colInventarioFinal.setCellValueFactory(
                new PropertyValueFactory<>("inventarioFinal")
        );

        colFaltante.setCellValueFactory(
                new PropertyValueFactory<>("faltante")
        );

        tablaInventario.setItems(registros);

        cmbTipoPrueba.setItems(
                FXCollections.observableArrayList(
                        "Prueba t de una muestra"
                )
        );

        cmbTipoPrueba.getSelectionModel().selectFirst();
    }


    // =========================
    // SIMULACIÓN
    // =========================

    @FXML
    private void simular(ActionEvent event) {

        try {

            int inventarioInicial =
                    Integer.parseInt(txtInventarioInicial.getText());

            int periodos =
                    Integer.parseInt(txtPeriodos.getText());

            int demandaMinima =
                    Integer.parseInt(txtDemandaMinima.getText());

            int demandaMaxima =
                    Integer.parseInt(txtDemandaMaxima.getText());

            int puntoReorden =
                    Integer.parseInt(txtPuntoReorden.getText());

            int cantidadPedido =
                    Integer.parseInt(txtCantidadPedido.getText());


            // Validaciones
            if (inventarioInicial < 0 ||
                    periodos <= 0 ||
                    demandaMinima < 0 ||
                    demandaMaxima < 0 ||
                    puntoReorden < 0 ||
                    cantidadPedido <= 0) {

                mostrarError(
                        "Los valores ingresados no son válidos."
                );

                return;
            }

            if (demandaMinima > demandaMaxima) {

                mostrarError(
                        "La demanda mínima no puede ser mayor " +
                                "que la demanda máxima."
                );

                return;
            }


            registros.clear();
            datosValidacion.clear();


            int inventarioActual = inventarioInicial;

            int pedidosRealizados = 0;
            int faltanteTotal = 0;

            double sumaInventarios = 0;

            int inventarioMinimo = Integer.MAX_VALUE;


            for (int periodo = 1;
                 periodo <= periodos;
                 periodo++) {

                int inventarioInicioPeriodo =
                        inventarioActual;


                // Generar demanda aleatoria
                int demanda =
                        generarEntero(
                                demandaMinima,
                                demandaMaxima
                        );


                // Calcular cuánto puede atenderse
                int unidadesAtendidas =
                        Math.min(
                                inventarioInicioPeriodo,
                                demanda
                        );


                // Calcular faltante
                int faltante =
                        Math.max(
                                0,
                                demanda - inventarioInicioPeriodo
                        );


                // Inventario después de atender demanda
                int inventarioDespuesDemanda =
                        inventarioInicioPeriodo -
                                unidadesAtendidas;


                int pedido = 0;


                /*
                 * Si el inventario llega o baja del
                 * punto de reorden, se genera un pedido.
                 */
                if (inventarioDespuesDemanda <= puntoReorden) {

                    pedido = cantidadPedido;
                    pedidosRealizados++;
                }


                /*
                 * Para esta versión suponemos que el pedido
                 * se recibe al final del período.
                 */
                int inventarioFinal =
                        inventarioDespuesDemanda + pedido;


                faltanteTotal += faltante;

                sumaInventarios += inventarioFinal;

                inventarioMinimo =
                        Math.min(
                                inventarioMinimo,
                                inventarioFinal
                        );


                RegistroInventario registro =
                        new RegistroInventario(
                                periodo,
                                inventarioInicioPeriodo,
                                demanda,
                                pedido,
                                inventarioFinal,
                                faltante
                        );


                registros.add(registro);

                datosValidacion.add(
                        (double) inventarioFinal
                );


                inventarioActual =
                        inventarioFinal;
            }


            // =========================
            // MOSTRAR RESULTADOS
            // =========================

            double promedio =
                    sumaInventarios / periodos;


            lblInventarioPromedio.setText(
                    String.format(
                            "%.2f unidades",
                            promedio
                    )
            );

            lblInventarioMinimo.setText(
                    inventarioMinimo + " unidades"
            );

            lblInventarioResurtido.setText(
                    String.valueOf(pedidosRealizados)
            );

            lblFaltanteTotal.setText(
                    faltanteTotal + " unidades"
            );


            // Evaluar estado final
            evaluarInventario(
                    inventarioActual,
                    puntoReorden,
                    cantidadPedido
            );


            // Reiniciar validación
            lblEstadistico.setText("Pendiente");
            lblPValor.setText("Pendiente");

            lblConclusion.setText(
                    "Ejecute una prueba de validación."
            );


        } catch (NumberFormatException e) {

            mostrarError(
                    "Ingrese únicamente valores numéricos enteros " +
                            "en los parámetros del inventario."
            );
        }
    }


    // =========================
    // ESTADO DEL INVENTARIO
    // =========================

    private void evaluarInventario(
            int inventarioActual,
            int puntoReorden,
            int cantidadPedido) {

        if (inventarioActual <= 0) {

            lblEstadoInventario.setText(
                    "🔴 INVENTARIO CRÍTICO\n" +
                            "Inventario actual: " +
                            inventarioActual +
                            " unidades.\n" +
                            "Se requiere reabastecimiento."
            );

        } else if (inventarioActual <= puntoReorden) {

            lblEstadoInventario.setText(
                    "🟠 REORDEN RECOMENDADO\n" +
                            "Inventario actual: " +
                            inventarioActual +
                            " unidades.\n" +
                            "Punto de reorden: " +
                            puntoReorden +
                            " unidades.\n" +
                            "Pedido sugerido: " +
                            cantidadPedido +
                            " unidades.\n" +
                            "Es recomendable solicitar nueva mercancía."
            );

        } else {

            lblEstadoInventario.setText(
                    "🟢 INVENTARIO SUFICIENTE\n" +
                            "Inventario actual: " +
                            inventarioActual +
                            " unidades.\n" +
                            "Punto de reorden: " +
                            puntoReorden +
                            " unidades.\n" +
                            "Por el momento no es necesario " +
                            "realizar otro pedido."
            );
        }
    }


    // =========================
    // VALIDACIÓN
    // =========================

    @FXML
    private void validarSimulacion(ActionEvent event) {

        if (datosValidacion.size() < 2) {

            mostrarError(
                    "Primero debe ejecutar una simulación " +
                            "con al menos 2 períodos."
            );

            return;
        }


        try {

            double referencia =
                    Double.parseDouble(
                            txtReferencia.getText()
                    );

            double significancia =
                    Double.parseDouble(
                            txtSignificancia.getText()
                    );


            if (significancia <= 0 ||
                    significancia >= 1) {

                mostrarError(
                        "El nivel de significancia debe " +
                                "estar entre 0 y 1."
                );

                return;
            }


            ejecutarPruebaT(
                    referencia,
                    significancia
            );


        } catch (NumberFormatException e) {

            mostrarError(
                    "Ingrese valores numéricos válidos " +
                            "para la referencia y significancia."
            );
        }
    }


    // =========================
    // PRUEBA T
    // =========================

    private void ejecutarPruebaT(
            double referencia,
            double significancia) {

        int n = datosValidacion.size();


        // Promedio
        double suma = 0;

        for (double dato : datosValidacion) {
            suma += dato;
        }

        double promedio = suma / n;


        // Desviación estándar muestral
        double sumaCuadrados = 0;

        for (double dato : datosValidacion) {

            sumaCuadrados +=
                    Math.pow(
                            dato - promedio,
                            2
                    );
        }

        double desviacion =
                Math.sqrt(
                        sumaCuadrados / (n - 1)
                );


        if (desviacion == 0) {

            lblEstadistico.setText("No calculable");
            lblPValor.setText("No calculable");

            lblConclusion.setText(
                    "No es posible realizar la prueba t porque " +
                            "los resultados no presentan variabilidad."
            );

            return;
        }


        // Estadístico t
        double t =
                (promedio - referencia) /
                        (desviacion / Math.sqrt(n));


        /*
         * Aproximación normal para obtener un
         * p-valor bilateral.
         *
         * Es adecuada como aproximación educativa
         * para esta versión del simulador.
         */
        double pValor =
                2.0 *
                        (1.0 -
                                normalCDF(
                                        Math.abs(t)
                                ));


        lblEstadistico.setText(
                String.format(
                        "%.4f",
                        t
                )
        );

        lblPValor.setText(
                String.format(
                        "%.4f",
                        pValor
                )
        );


        if (pValor < significancia) {

            lblConclusion.setText(
                    "El p-valor es menor que el nivel de " +
                            "significancia (" +
                            significancia +
                            "). Existe evidencia estadística de que " +
                            "el inventario promedio simulado es diferente " +
                            "del valor de referencia de " +
                            String.format("%.2f", referencia) +
                            " unidades."
            );

        } else {

            lblConclusion.setText(
                    "El p-valor es mayor o igual que el nivel de " +
                            "significancia (" +
                            significancia +
                            "). No se encontró evidencia estadística " +
                            "suficiente para afirmar que el inventario " +
                            "promedio simulado sea diferente del valor " +
                            "de referencia de " +
                            String.format("%.2f", referencia) +
                            " unidades."
            );
        }
    }


    // =========================
    // DISTRIBUCIÓN NORMAL
    // =========================

    private double normalCDF(double x) {

        return 0.5 *
                (1.0 +
                        erf(
                                x / Math.sqrt(2.0)
                        ));
    }


    private double erf(double x) {

        // Aproximación numérica de erf

        double signo =
                x < 0 ? -1 : 1;

        x = Math.abs(x);

        double a1 = 0.254829592;
        double a2 = -0.284496736;
        double a3 = 1.421413741;
        double a4 = -1.453152027;
        double a5 = 1.061405429;
        double p = 0.3275911;

        double t =
                1.0 /
                        (1.0 + p * x);

        double y =
                1.0 -
                        (((((a5 * t + a4) * t)
                                + a3) * t
                                + a2) * t
                                + a1) * t *
                                Math.exp(-x * x);

        return signo * y;
    }


    // =========================
    // NÚMERO ALEATORIO
    // =========================

    private int generarEntero(
            int minimo,
            int maximo) {

        return random.nextInt(
                maximo - minimo + 1
        ) + minimo;
    }


    // =========================
    // LIMPIAR
    // =========================

    @FXML
    private void limpiar(ActionEvent event) {

        txtInventarioInicial.clear();
        txtPeriodos.clear();
        txtDemandaMinima.clear();
        txtDemandaMaxima.clear();
        txtPuntoReorden.clear();
        txtCantidadPedido.clear();

        txtReferencia.clear();
        txtSignificancia.setText("0.05");

        registros.clear();
        datosValidacion.clear();

        lblInventarioPromedio.setText(
                "0.00 unidades"
        );

        lblInventarioMinimo.setText(
                "0 unidades"
        );

        lblInventarioResurtido.setText("0");

        lblFaltanteTotal.setText(
                "0 unidades"
        );

        lblEstadoInventario.setText(
                "Ejecute la simulación para conocer " +
                        "el estado del inventario."
        );

        lblEstadistico.setText(
                "Pendiente"
        );

        lblPValor.setText(
                "Pendiente"
        );

        lblConclusion.setText(
                "Ejecute una prueba de validación."
        );
    }


    // =========================
    // MENSAJE DE ERROR
    // =========================

    private void mostrarError(String mensaje) {

        Alert alerta =
                new Alert(
                        Alert.AlertType.ERROR
                );

        alerta.setTitle(
                "Error"
        );

        alerta.setHeaderText(
                "Datos incorrectos"
        );

        alerta.setContentText(
                mensaje
        );

        alerta.showAndWait();
    }


    // =========================
    // CERRAR
    // =========================

    @FXML
    private void cerrar(ActionEvent event) {

        Stage stage =
                (Stage)
                        ((Node) event.getSource())
                                .getScene()
                                .getWindow();

        stage.close();
    }
}