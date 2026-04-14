package api;

import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;

public class ApiServer {

    public static void main(String[] args) throws Exception {

        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", exchange -> {
        String response = "UniSync API Running 🚀";
        exchange.sendResponseHeaders(200, response.length());
        exchange.getResponseBody().write(response.getBytes());
        exchange.close();
    });
        server.createContext("/login", new LoginHandler());
        server.createContext("/signup", new SignupHandler());
        server.createContext("/addResource", new ResourceHandler());
        server.createContext("/resources", new GetResourcesHandler());
        server.createContext("/borrow", new BorrowHandler());
        server.createContext("/transactions", new TransactionsHandler());
        server.createContext("/return", new ReturnHandler());

        server.setExecutor(null);
        server.start();

        System.out.println("🚀 API running on http://localhost:8080");
    }
}