module com.nietosystems.simulacion {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires org.kordamp.bootstrapfx.core;

    opens com.nietosystems.simulacion to javafx.fxml;
    exports com.nietosystems.simulacion;

    opens com.nietosystems.simulacion.controller to javafx.fxml;
    exports com.nietosystems.simulacion.controller;
}