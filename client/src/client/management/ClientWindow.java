package client.management;

import javafx.application.Application;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import network.management.Connection;
import network.management.ConnectionListener;

public class ClientWindow extends Application implements ConnectionListener {

    public Connection connection;

    @Override
    public void start(Stage primaryStage) throws Exception {
        AnchorPane root = FXMLLoader.load(getClass().getResource("chatgui.fxml"));
        primaryStage.setTitle("Better than Skype");
        primaryStage.setScene(new Scene(root,700,700));
        primaryStage.show();
    }

    public static void main(String[] args) {
        Application.launch(args);


    }

    @Override
    public void onConnectionReady(Connection connection) {

    }

    @Override
    public void onRecieveString(Connection connection, String value) {

    }

    @Override
    public void onDisconnect(Connection connection) {

    }

    @Override
    public void onException(Connection connection, Exception e) {

    }
}
