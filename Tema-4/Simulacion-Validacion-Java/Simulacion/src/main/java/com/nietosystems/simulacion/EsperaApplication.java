


package com.nietosystems.simulacion;

import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.stage.Screen;
import javafx.stage.Stage;

public class EsperaApplication {

    public static void abrir(Stage ventanaPrincipal) {

        try {

            FXMLLoader loader = new FXMLLoader(
                    EsperaApplication.class.getResource(
                            "espera-view.fxml"
                    )
            );

            Scene scene = new Scene(loader.load());

            Stage stage = new Stage();

            stage.setTitle("Simulación de Espera");
            stage.setScene(scene);

            stage.setOnHidden(event -> {
                ventanaPrincipal.show();
            });

            // Mostrar primero la ventana
            stage.show();

            // Obtener únicamente el área UTILIZABLE de la pantalla.
            // Esto excluye la barra de tareas de Windows.
            Rectangle2D areaVisible =
                    Screen.getPrimary().getVisualBounds();

            // Obligar a la ventana a respetar los bordes de la pantalla.
            stage.setX(areaVisible.getMinX());
            stage.setY(areaVisible.getMinY());

            stage.setWidth(areaVisible.getWidth());
            stage.setHeight(areaVisible.getHeight());

            // Impedir que pueda crecer más que el área visible.
            stage.setMaxWidth(areaVisible.getWidth());
            stage.setMaxHeight(areaVisible.getHeight());

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}