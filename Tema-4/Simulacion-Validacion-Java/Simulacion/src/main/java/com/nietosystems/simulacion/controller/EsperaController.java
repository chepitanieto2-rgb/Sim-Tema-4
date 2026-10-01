package com.nietosystems.simulacion.controller;

import com.nietosystems.simulacion.Cliente;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.Alert;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class EsperaController {

    // =========================================================
    // CAMPOS DE LA SIMULACIÓN
    // =========================================================

    @FXML
    private TextField txtClientes;

    @FXML
    private TextField txtServidores;

    @FXML
    private TextField txtLlegadaMinima;

    @FXML
    private TextField txtLlegadaMaxima;

    @FXML
    private TextField txtServicioMinimo;

    @FXML
    private TextField txtServicioMaximo;


    // =========================================================
    // RESULTADOS
    // =========================================================

    @FXML
    private Label lblEsperaPromedio;

    @FXML
    private Label lblEsperaMaxima;

    @FXML
    private Label lblClientesEsperaron;

    @FXML
    private Label lblUtilizacion;


    // =========================================================
    // TABLA
    // =========================================================

    @FXML
    private TableView<Cliente> tablaClientes;

    @FXML
    private TableColumn<Cliente, Integer> colCliente;

    @FXML
    private TableColumn<Cliente, Integer> colServidor;

    @FXML
    private TableColumn<Cliente, Double> colLlegada;

    @FXML
    private TableColumn<Cliente, Double> colServicio;

    @FXML
    private TableColumn<Cliente, Double> colEspera;

    @FXML
    private TableColumn<Cliente, Double> colInicio;

    @FXML
    private TableColumn<Cliente, Double> colFin;


    // =========================================================
    // VALIDACIÓN
    // =========================================================

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


    // =========================================================
    // DATOS
    // =========================================================

    private final ObservableList<Cliente> clientes =
            FXCollections.observableArrayList();

    private final Random random = new Random();

    /*
     * Guardamos los tiempos de espera para posteriormente
     * utilizarlos en la validación estadística.
     */
    private final List<Double> tiemposEspera =
            new ArrayList<>();


    // =========================================================
    // INICIALIZACIÓN
    // =========================================================

    @FXML
    public void initialize() {

        colCliente.setCellValueFactory(
                new PropertyValueFactory<>("numero")
        );

        colServidor.setCellValueFactory(
                new PropertyValueFactory<>("servidor")
        );

        colLlegada.setCellValueFactory(
                new PropertyValueFactory<>("llegada")
        );

        colServicio.setCellValueFactory(
                new PropertyValueFactory<>("servicio")
        );

        colEspera.setCellValueFactory(
                new PropertyValueFactory<>("espera")
        );

        colInicio.setCellValueFactory(
                new PropertyValueFactory<>("inicio")
        );

        colFin.setCellValueFactory(
                new PropertyValueFactory<>("fin")
        );

        tablaClientes.setItems(clientes);

        cmbTipoPrueba.setItems(
                FXCollections.observableArrayList(
                        "Prueba paramétrica - t de una muestra",
                        "Prueba no paramétrica - Wilcoxon"
                )
        );

        cmbTipoPrueba.getSelectionModel().selectFirst();
    }


    // =========================================================
    // SIMULACIÓN
    // =========================================================

    @FXML
    private void simular(ActionEvent event) {

        try {

            int cantidadClientes =
                    Integer.parseInt(
                            txtClientes.getText()
                    );

            int cantidadServidores =
                    Integer.parseInt(
                            txtServidores.getText()
                    );

            double llegadaMinima =
                    Double.parseDouble(
                            txtLlegadaMinima.getText()
                    );

            double llegadaMaxima =
                    Double.parseDouble(
                            txtLlegadaMaxima.getText()
                    );

            double servicioMinimo =
                    Double.parseDouble(
                            txtServicioMinimo.getText()
                    );

            double servicioMaximo =
                    Double.parseDouble(
                            txtServicioMaximo.getText()
                    );


            // =================================================
            // VALIDACIONES
            // =================================================

            if (cantidadClientes <= 0) {

                mostrarError(
                        "El número de clientes debe ser mayor que 0."
                );

                return;
            }


            if (cantidadServidores <= 0) {

                mostrarError(
                        "El número de servidores debe ser mayor que 0."
                );

                return;
            }


            if (llegadaMinima < 0 ||
                    llegadaMaxima <= llegadaMinima) {

                mostrarError(
                        "Revise los tiempos de llegada."
                );

                return;
            }


            if (servicioMinimo < 0 ||
                    servicioMaximo <= servicioMinimo) {

                mostrarError(
                        "Revise los tiempos de servicio."
                );

                return;
            }


            // =================================================
            // LIMPIAR DATOS ANTERIORES
            // =================================================

            clientes.clear();
            tiemposEspera.clear();


            /*
             * Cada posición del arreglo representa un servidor.
             *
             * servidorDisponible[0] = servidor 1
             * servidorDisponible[1] = servidor 2
             * servidorDisponible[2] = servidor 3
             */

            double[] servidoresDisponibles =
                    new double[cantidadServidores];


            double tiempoLlegada = 0;

            double sumaEspera = 0;

            double esperaMaxima = 0;

            int clientesEsperaron = 0;

            double sumaServicio = 0;

            double tiempoFinalSimulacion = 0;


            // =================================================
            // GENERACIÓN DE CLIENTES
            // =================================================

            for (int i = 1;
                 i <= cantidadClientes;
                 i++) {


                // ---------------------------------------------
                // TIEMPO ENTRE LLEGADAS
                // ---------------------------------------------

                double intervaloLlegada =
                        generarAleatorio(
                                llegadaMinima,
                                llegadaMaxima
                        );

                tiempoLlegada += intervaloLlegada;


                // ---------------------------------------------
                // TIEMPO DE SERVICIO
                // ---------------------------------------------

                double tiempoServicio =
                        generarAleatorio(
                                servicioMinimo,
                                servicioMaximo
                        );


                // ---------------------------------------------
                // BUSCAR SERVIDOR DISPONIBLE PRIMERO
                // ---------------------------------------------

                int indiceServidor = 0;

                double menorDisponibilidad =
                        servidoresDisponibles[0];


                for (int j = 1;
                     j < cantidadServidores;
                     j++) {

                    if (servidoresDisponibles[j]
                            < menorDisponibilidad) {

                        menorDisponibilidad =
                                servidoresDisponibles[j];

                        indiceServidor = j;
                    }
                }


                /*
                 * Convertimos el índice en número de servidor.
                 *
                 * índice 0 -> servidor 1
                 * índice 1 -> servidor 2
                 */

                int numeroServidor =
                        indiceServidor + 1;


                // ---------------------------------------------
                // INICIO DEL SERVICIO
                // ---------------------------------------------

                double inicioServicio =
                        Math.max(
                                tiempoLlegada,
                                menorDisponibilidad
                        );


                // ---------------------------------------------
                // TIEMPO DE ESPERA
                // ---------------------------------------------

                double espera =
                        inicioServicio -
                                tiempoLlegada;


                // ---------------------------------------------
                // FIN DEL SERVICIO
                // ---------------------------------------------

                double finServicio =
                        inicioServicio +
                                tiempoServicio;


                // ---------------------------------------------
                // ACTUALIZAR SERVIDOR
                // ---------------------------------------------

                servidoresDisponibles[indiceServidor] =
                        finServicio;


                // ---------------------------------------------
                // ESTADÍSTICAS
                // ---------------------------------------------

                sumaEspera += espera;

                sumaServicio += tiempoServicio;

                tiempoFinalSimulacion =
                        Math.max(
                                tiempoFinalSimulacion,
                                finServicio
                        );


                if (espera > esperaMaxima) {

                    esperaMaxima = espera;
                }


                if (espera > 0) {

                    clientesEsperaron++;
                }


                tiemposEspera.add(espera);


                // ---------------------------------------------
                // CREAR CLIENTE
                // ---------------------------------------------

                Cliente cliente =
                        new Cliente(
                                i,
                                numeroServidor,
                                tiempoLlegada,
                                tiempoServicio,
                                espera,
                                inicioServicio,
                                finServicio
                        );


                clientes.add(cliente);
            }


            // =================================================
            // RESULTADOS
            // =================================================

            double esperaPromedio =
                    sumaEspera /
                            cantidadClientes;


            /*
             * Utilización promedio de los servidores.
             *
             * Se calcula:
             *
             * tiempo total de servicio /
             * (número de servidores * tiempo total)
             */

            double utilizacion = 0;

            if (tiempoFinalSimulacion > 0) {

                utilizacion =
                        (sumaServicio /
                                (cantidadServidores *
                                        tiempoFinalSimulacion))
                                * 100;
            }


            lblEsperaPromedio.setText(
                    String.format(
                            "%.2f min",
                            esperaPromedio
                    )
            );


            lblEsperaMaxima.setText(
                    String.format(
                            "%.2f min",
                            esperaMaxima
                    )
            );


            lblClientesEsperaron.setText(
                    String.valueOf(
                            clientesEsperaron
                    )
            );


            lblUtilizacion.setText(
                    String.format(
                            "%.2f %%",
                            utilizacion
                    )
            );


            /*
             * Limpiamos los resultados de una validación
             * anterior.
             */

            limpiarResultadosValidacion();


        } catch (NumberFormatException e) {

            mostrarError(
                    "Todos los campos deben contener números."
            );
        }
    }


    // =========================================================
    // NÚMERO ALEATORIO
    // =========================================================

    private double generarAleatorio(
            double minimo,
            double maximo
    ) {

        return minimo +
                random.nextDouble()
                        *
                        (maximo - minimo);
    }


    // =========================================================
    // VALIDACIÓN ESTADÍSTICA
    // =========================================================

    @FXML
    private void validarSimulacion(ActionEvent event) {

        try {

            if (tiemposEspera.isEmpty()) {

                mostrarError(
                        "Primero debe ejecutar una simulación."
                );

                return;
            }


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
                        "El nivel de significancia debe estar entre 0 y 1."
                );

                return;
            }


            String tipo =
                    cmbTipoPrueba
                            .getSelectionModel()
                            .getSelectedItem();


            if (tipo == null) {

                mostrarError(
                        "Seleccione un tipo de prueba."
                );

                return;
            }


            // =================================================
            // PRUEBA PARAMÉTRICA
            // =================================================

            if (tipo.startsWith("Prueba paramétrica")) {

                double resultado =
                        ejecutarPruebaT(
                                referencia,
                                significancia
                        );

                return;
            }


            // =================================================
            // PRUEBA NO PARAMÉTRICA
            // =================================================

            if (tipo.startsWith("Prueba no paramétrica")) {

                ejecutarWilcoxon(
                        referencia,
                        significancia
                );
            }


        } catch (NumberFormatException e) {

            mostrarError(
                    "La referencia y la significancia deben ser números."
            );
        }
    }


    // =========================================================
    // PRUEBA T DE UNA MUESTRA
    // =========================================================

    private double ejecutarPruebaT(
            double referencia,
            double significancia
    ) {

        int n = tiemposEspera.size();


        if (n < 2) {

            mostrarError(
                    "Se necesitan al menos 2 datos para realizar la prueba."
            );

            return 0;
        }


        // ---------------------------------------------
        // MEDIA
        // ---------------------------------------------

        double suma = 0;

        for (double valor : tiemposEspera) {

            suma += valor;
        }

        double media = suma / n;


        // ---------------------------------------------
        // DESVIACIÓN ESTÁNDAR
        // ---------------------------------------------

        double sumaCuadrados = 0;

        for (double valor : tiemposEspera) {

            sumaCuadrados +=
                    Math.pow(
                            valor - media,
                            2
                    );
        }


        double varianza =
                sumaCuadrados /
                        (n - 1);


        double desviacion =
                Math.sqrt(varianza);


        if (desviacion == 0) {

            mostrarError(
                    "La desviación estándar es 0. No se puede realizar la prueba t."
            );

            return 0;
        }


        // ---------------------------------------------
        // ESTADÍSTICO t
        // ---------------------------------------------

        double t =
                (media - referencia) /
                        (desviacion /
                                Math.sqrt(n));


        int gradosLibertad = n - 1;


        /*
         * Calculamos el p-valor bilateral.
         */

        double pValor =
                2 *
                        (1 -
                                studentTCDF(
                                        Math.abs(t),
                                        gradosLibertad
                                )
                        );


        // Evitar valores fuera del rango
        pValor =
                Math.max(
                        0,
                        Math.min(
                                1,
                                pValor
                        )
                );


        mostrarResultadoValidacion(
                "t = " +
                        String.format(
                                "%.4f",
                                t
                        ),
                "p = " +
                        String.format(
                                "%.4f",
                                pValor
                        ),
                pValor < significancia
                        ?
                        "Se rechaza H0. La diferencia entre la media simulada y el valor de referencia es estadísticamente significativa."
                        :
                        "No se rechaza H0. No se encontró evidencia suficiente de una diferencia significativa respecto al valor de referencia."
        );


        return pValor;
    }


    // =========================================================
    // PRUEBA NO PARAMÉTRICA DE WILCOXON
    // =========================================================

    private void ejecutarWilcoxon(
            double referencia,
            double significancia
    ) {

        /*
         * Calculamos las diferencias entre cada espera
         * simulada y el valor de referencia.
         */

        List<Double> diferencias =
                new ArrayList<>();


        for (double valor : tiemposEspera) {

            double diferencia =
                    valor - referencia;


            /*
             * Las diferencias iguales a cero
             * se eliminan de Wilcoxon.
             */

            if (Math.abs(diferencia) > 0.0000001) {

                diferencias.add(diferencia);
            }
        }


        int n = diferencias.size();


        if (n < 5) {

            mostrarError(
                    "Para esta implementación de Wilcoxon se requieren al menos 5 diferencias distintas de cero."
            );

            return;
        }


        // ---------------------------------------------
        // ORDENAR VALORES ABSOLUTOS
        // ---------------------------------------------

        List<Double> absolutos =
                new ArrayList<>();


        for (double diferencia : diferencias) {

            absolutos.add(
                    Math.abs(diferencia)
            );
        }


        List<Double> ordenados =
                new ArrayList<>(absolutos);

        Collections.sort(ordenados);


        // ---------------------------------------------
        // SUMA DE RANGOS POSITIVOS
        // ---------------------------------------------

        double sumaRangosPositivos = 0;


        for (double diferencia : diferencias) {

            double valorAbsoluto =
                    Math.abs(diferencia);


            /*
             * Rango promedio para empates.
             */

            double sumaRangos = 0;

            int cantidadIguales = 0;


            for (int i = 0;
                 i < ordenados.size();
                 i++) {

                if (Math.abs(
                        ordenados.get(i)
                                -
                                valorAbsoluto
                ) < 0.0000001) {

                    sumaRangos += i + 1;
                    cantidadIguales++;
                }
            }


            double rango =
                    sumaRangos /
                            cantidadIguales;


            if (diferencia > 0) {

                sumaRangosPositivos += rango;
            }
        }


        // ---------------------------------------------
        // ESTADÍSTICO
        // ---------------------------------------------

        double mediaRangos =
                n * (n + 1) / 4.0;


        double desviacionRangos =
                Math.sqrt(
                        n *
                                (n + 1) *
                                (2 * n + 1)
                                /
                                24.0
                );


        double z =
                (sumaRangosPositivos -
                        mediaRangos)
                        /
                        desviacionRangos;


        /*
         * Corrección de continuidad.
         */

        if (z > 0) {

            z =
                    (sumaRangosPositivos -
                            mediaRangos -
                            0.5)
                            /
                            desviacionRangos;

        } else if (z < 0) {

            z =
                    (sumaRangosPositivos -
                            mediaRangos +
                            0.5)
                            /
                            desviacionRangos;
        }


        double pValor =
                2 *
                        (1 -
                                normalCDF(
                                        Math.abs(z)
                                )
                        );


        pValor =
                Math.max(
                        0,
                        Math.min(
                                1,
                                pValor
                        )
                );


        mostrarResultadoValidacion(
                "W+ = " +
                        String.format(
                                "%.4f",
                                sumaRangosPositivos
                        ) +
                        " | z = " +
                        String.format(
                                "%.4f",
                                z
                        ),
                "p = " +
                        String.format(
                                "%.4f",
                                pValor
                        ),
                pValor < significancia
                        ?
                        "Se rechaza H0. La distribución de las esperas presenta una diferencia estadísticamente significativa respecto al valor de referencia."
                        :
                        "No se rechaza H0. No se encontró evidencia suficiente de una diferencia significativa respecto al valor de referencia."
        );
    }


    // =========================================================
    // DISTRIBUCIÓN NORMAL
    // =========================================================

    private double normalCDF(double x) {

        return 0.5 *
                (
                        1 +
                                erf(
                                        x /
                                                Math.sqrt(2)
                                )
                );
    }


    private double erf(double x) {

        double signo =
                x >= 0 ? 1 : -1;

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
                        (
                                (
                                        (
                                                (
                                                        (
                                                                a5 * t
                                                                        +
                                                                        a4
                                                        ) * t
                                                                +
                                                                a3
                                                ) * t
                                                        +
                                                        a2
                                        ) * t
                                                +
                                                a1
                                ) * t
                                        *
                                        Math.exp(
                                                -x * x
                                        )
                        );


        return signo * y;
    }


    // =========================================================
    // DISTRIBUCIÓN t DE STUDENT
    // =========================================================

    private double studentTCDF(
            double t,
            int gradosLibertad
    ) {

        if (t == 0) {
            return 0.5;
        }


        double x =
                gradosLibertad /
                        (
                                gradosLibertad
                                        +
                                        t * t
                        );


        double ibeta =
                regularizedBeta(
                        x,
                        gradosLibertad / 2.0,
                        0.5
                );


        if (t > 0) {

            return 1 -
                    0.5 * ibeta;

        } else {

            return 0.5 * ibeta;
        }
    }


    // =========================================================
    // BETA REGULARIZADA
    // =========================================================

    private double regularizedBeta(
            double x,
            double a,
            double b
    ) {

        if (x <= 0) {
            return 0;
        }

        if (x >= 1) {
            return 1;
        }


        double bt =
                Math.exp(
                        logGamma(a + b)
                                -
                                logGamma(a)
                                -
                                logGamma(b)
                                +
                                a * Math.log(x)
                                +
                                b * Math.log(1 - x)
                );


        if (x <
                (a + 1) /
                        (a + b + 2)) {

            return bt *
                    betaFraction(
                            x,
                            a,
                            b
                    ) /
                    a;

        } else {

            return 1 -
                    bt *
                            betaFraction(
                                    1 - x,
                                    b,
                                    a
                            ) /
                            b;
        }
    }


    // =========================================================
    // FRACCIÓN CONTINUA DE BETA
    // =========================================================

    private double betaFraction(
            double x,
            double a,
            double b
    ) {

        int maxIterations = 100;

        double epsilon = 3.0e-7;

        double qab = a + b;

        double qap = a + 1;

        double qam = a - 1;


        double c = 1;

        double d =
                1 -
                        qab * x /
                                qap;


        if (Math.abs(d) < 1e-30) {
            d = 1e-30;
        }


        d = 1 / d;

        double h = d;


        for (int m = 1;
             m <= maxIterations;
             m++) {

            int m2 = 2 * m;


            double aa =
                    m *
                            (b - m) *
                            x /
                            (
                                    (qam + m2) *
                                            (a + m2)
                            );


            d =
                    1 +
                            aa * d;


            if (Math.abs(d) < 1e-30) {
                d = 1e-30;
            }


            c =
                    1 +
                            aa / c;


            if (Math.abs(c) < 1e-30) {
                c = 1e-30;
            }


            d = 1 / d;

            h *= d * c;


            aa =
                    -(
                            a + m
                    ) *
                            (qab + m) *
                            x /
                            (
                                    (a + m2) *
                                            (qap + m2)
                            );


            d =
                    1 +
                            aa * d;


            if (Math.abs(d) < 1e-30) {
                d = 1e-30;
            }


            c =
                    1 +
                            aa / c;


            if (Math.abs(c) < 1e-30) {
                c = 1e-30;
            }


            d = 1 / d;


            double del =
                    d * c;


            h *= del;


            if (Math.abs(del - 1) <
                    epsilon) {

                break;
            }
        }


        return h;
    }


    // =========================================================
    // FUNCIÓN GAMMA
    // =========================================================

    private double logGamma(double x) {

        double[] coef = {
                76.18009172947146,
                -86.50532032941677,
                24.01409824083091,
                -1.231739572450155,
                0.001208650973866179,
                -0.000005395239384953
        };


        double y = x;

        double tmp =
                x + 5.5;

        tmp -=
                (x + 0.5) *
                        Math.log(tmp);


        double ser =
                1.000000000190015;


        for (double c : coef) {

            y += 1;

            ser += c / y;
        }


        return -tmp +
                Math.log(
                        2.5066282746310005 *
                                ser /
                                x
                );
    }


    // =========================================================
    // MOSTRAR RESULTADO DE VALIDACIÓN
    // =========================================================

    private void mostrarResultadoValidacion(
            String estadistico,
            String pValor,
            String conclusion
    ) {

        lblEstadistico.setText(
                estadistico
        );

        lblPValor.setText(
                pValor
        );

        lblConclusion.setText(
                conclusion
        );
    }


    // =========================================================
    // LIMPIAR VALIDACIÓN
    // =========================================================

    private void limpiarResultadosValidacion() {

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


    // =========================================================
    // LIMPIAR TODO
    // =========================================================

    @FXML
    private void limpiar(ActionEvent event) {

        txtClientes.clear();

        txtServidores.clear();

        txtLlegadaMinima.clear();

        txtLlegadaMaxima.clear();

        txtServicioMinimo.clear();

        txtServicioMaximo.clear();

        txtReferencia.clear();

        txtSignificancia.clear();


        lblEsperaPromedio.setText(
                "0.00 min"
        );

        lblEsperaMaxima.setText(
                "0.00 min"
        );

        lblClientesEsperaron.setText(
                "0"
        );

        lblUtilizacion.setText(
                "0.00 %"
        );


        clientes.clear();

        tiemposEspera.clear();


        limpiarResultadosValidacion();
    }


    // =========================================================
    // CERRAR
    // =========================================================

    @FXML
    private void cerrar(ActionEvent event) {

        Stage stage =
                (Stage)
                        ((Node) event.getSource())
                                .getScene()
                                .getWindow();


        stage.close();
    }


    // =========================================================
    // MENSAJE DE ERROR
    // =========================================================

    private void mostrarError(
            String mensaje
    ) {

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
}