package com.nietosystems.simulacion;

import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.stage.Screen;
import javafx.stage.Stage;

public class InventarioApplication {

    public static void abrir(Stage ventanaPrincipal) {

        try {

            FXMLLoader loader =
                    new FXMLLoader(
                            InventarioApplication.class.getResource(
                                    "inventario-view.fxml"
                            )
                    );

            Scene scene =
                    new Scene(
                            loader.load()
                    );

            Stage stage =
                    new Stage();

            stage.setTitle(
                    "Simulación de Inventario"
            );

            stage.setScene(scene);

            stage.setOnHidden(event -> {
                ventanaPrincipal.show();
            });

            // Área visible de la pantalla
            Rectangle2D pantalla =
                    Screen.getPrimary()
                            .getVisualBounds();

            /*
             * La ventana no debe superar
             * los límites visibles.
             */
            stage.setMaxWidth(
                    pantalla.getWidth()
            );

            stage.setMaxHeight(
                    pantalla.getHeight()
            );

            // Tamaño inicial
            stage.setWidth(
                    Math.min(
                            1000,
                            pantalla.getWidth()
                    )
            );

            stage.setHeight(
                    Math.min(
                            700,
                            pantalla.getHeight()
                    )
            );

            stage.centerOnScreen();

            stage.show();

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}