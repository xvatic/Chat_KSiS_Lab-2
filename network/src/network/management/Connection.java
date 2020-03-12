package network.management;

import com.sun.xml.internal.ws.policy.privateutil.PolicyUtils;
import sun.rmi.transport.tcp.TCPChannel;
import sun.rmi.transport.tcp.TCPConnection;

import java.io.*;
import java.net.Socket;
import java.nio.charset.Charset;

public class Connection {
    private final Socket socket;
    private final Thread recieveThread;
    private final ConnectionListener eventListener;
    private final BufferedReader inputStream;
    private final BufferedWriter outputStream;

    public Connection(ConnectionListener eventListener, String ipAddress, int port) throws IOException  {
        this(eventListener, new Socket(ipAddress,port));
    }

    public Connection(ConnectionListener eventListener,Socket socket) throws IOException {
        this.socket = socket;
        this.eventListener = eventListener;
        inputStream = new BufferedReader(new InputStreamReader(socket.getInputStream(), Charset.forName("UTF-8")));
        outputStream = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(),Charset.forName("UTF-8")));
        recieveThread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    eventListener.onConnectionReady(Connection.this);
                    while (!recieveThread.isInterrupted()){
                        eventListener.onRecieveString(Connection.this, inputStream.readLine());
                    }


                }   catch (IOException e)  {
                    eventListener.onException(Connection.this,e);

                }   finally {
                    eventListener.onDisconnect(Connection.this);

                }

            }
        });
        recieveThread.start();
    }

    public synchronized void sendString(String value){
        try {
            outputStream.write(value+"\r\n");
            outputStream.flush();
        }   catch (IOException e)   {
            eventListener.onException(Connection.this, e);
        }   finally {

        }

    }

    public synchronized void disconnect() {
        recieveThread.interrupt();
        try {
            socket.close();
        }   catch (IOException e) {
            eventListener.onException(Connection.this, e);
        }
    }

    @Override
    public String toString() {
        return "Connection: " + socket.getInetAddress() + ":" + socket.getPort();
    }
}
