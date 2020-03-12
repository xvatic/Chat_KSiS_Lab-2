package server.management;

import network.management.Connection;
import network.management.ConnectionListener;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;

public class ChatServer implements ConnectionListener {

    public static void main(String[] args) {
        new ChatServer();

    }

    private final ArrayList<Connection> connections = new ArrayList<>();


    private ChatServer() {
        System.out.println("Server running...");
        try (ServerSocket serverSocket = new ServerSocket(8189)){
            while (true) {
                try {
                    new Connection(this, serverSocket.accept());
                } catch (IOException e) {
                    System.out.println("Connection exception: " + e);

                }

            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public synchronized void onConnectionReady(Connection connection) {
        connections.add(connection);
        sendToAll("Client connected: " + connection);


    }

    @Override
    public synchronized void onRecieveString(Connection connection, String value) {
        sendToAll(value);

    }

    @Override
    public synchronized void onDisconnect(Connection connection) {
        connections.remove(connection);
        sendToAll("Client disconnected: " + connection);

    }

    @Override
    public synchronized void  onException(Connection connection, Exception e) {

    }

    private void sendToAll(String value) {
        System.out.println(value);
        for (int i=0; i<connections.size(); i++) {
            connections.get(i).sendString(value);
        }
    }
}
