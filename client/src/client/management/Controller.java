package client.management;

import javafx.fxml.FXML;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import network.management.Connection;

public class Controller {

    private final String IP_ADDR = "192.168.0.106";
    private final int PORT = 8189;

    private Connection connection;

    @FXML
    public TextField fieldMessageInput;

    @FXML
    public TextField fieldNickname;

    @FXML
    public TextArea areaMessageDisplay;

    @FXML
    void initialize() {
        connection = new Connection(this,IP_ADDR, PORT);

    }
}
