package com.nietosystems.simulacion.controller;

import com.nietosystems.simulacion.EsperaApplication;
import com.nietosystems.simulacion.InventarioApplication;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.stage.Stage;

public class MainController {

    @FXML
    private void abrirEspera(ActionEvent event) {

        Stage ventanaPrincipal = (Stage)
                ((Node) event.getSource())
                        .getScene()
                        .getWindow();

        ventanaPrincipal.hide();

        EsperaApplication.abrir(ventanaPrincipal);
    }


    @FXML
    private void abrirInventario(ActionEvent event) {

        Stage ventanaPrincipal = (Stage)
                ((Node) event.getSource())
                        .getScene()
                        .getWindow();

        ventanaPrincipal.hide();

        InventarioApplication.abrir(ventanaPrincipal);
    }


    @FXML
    private void salir(ActionEvent event) {

        Stage stage = (Stage)
                ((Node) event.getSource())
                        .getScene()
                        .getWindow();

        stage.close();
    }
}
