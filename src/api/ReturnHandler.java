package api;

import com.sun.net.httpserver.*;
import org.json.JSONObject;
import service.TransactionService;

import java.io.*;

public class ReturnHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange exchange) throws IOException {

        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            send(exchange, 405, new JSONObject().put("status", "fail"));
            return;
        }

        try {
            String body = new BufferedReader(
                    new InputStreamReader(exchange.getRequestBody())
            ).lines().reduce("", (a, b) -> a + b);

            JSONObject json = new JSONObject(body);

            int transactionId = json.getInt("transactionId");

            System.out.println("🔥 RETURN API HIT: " + transactionId);

            TransactionService service = new TransactionService();

            service.completeLendBorrowTransaction(transactionId);

            JSONObject res = new JSONObject();
            res.put("status", "success");

            send(exchange, 200, res);

        } catch (Exception e) {
            JSONObject res = new JSONObject();
            res.put("status", "fail");
            res.put("message", e.getMessage());

            send(exchange, 500, res);
        }
    }

    private void send(HttpExchange ex, int code, JSONObject res) throws IOException {
        ex.getResponseHeaders().add("Content-Type", "application/json");
        byte[] bytes = res.toString().getBytes();
        ex.sendResponseHeaders(code, bytes.length);
        ex.getResponseBody().write(bytes);
        ex.close();
    }
}