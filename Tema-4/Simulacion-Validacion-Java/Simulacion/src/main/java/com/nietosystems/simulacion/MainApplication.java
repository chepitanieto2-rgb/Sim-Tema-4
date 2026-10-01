package com.nietosystems.simulacion;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class MainApplication extends Application {

    @Override
    public void start(Stage stage) throws Exception {

        FXMLLoader fxmlLoader = new FXMLLoader(
                MainApplication.class.getResource(
                        "main-view.fxml"
                )
        );

        Scene scene = new Scene(
                fxmlLoader.load()
        );

        stage.setTitle("Sistema de Simulación");
        stage.setScene(scene);
        stage.show();
    }
}

