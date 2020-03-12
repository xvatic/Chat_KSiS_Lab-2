package network.management;

public interface ConnectionListener {
    void onConnectionReady(Connection connection);
    void onRecieveString(Connection connection, String value);
    void onDisconnect(Connection connection);
    void onException(Connection connection, Exception e);

}
