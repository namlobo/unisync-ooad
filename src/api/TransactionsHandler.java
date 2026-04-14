package api;

import com.sun.net.httpserver.*;
import org.json.JSONArray;
import org.json.JSONObject;
import service.TransactionService;
import model.transaction.Transaction;

import java.io.IOException;
import java.util.List;

public class TransactionsHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange exchange) throws IOException {

        if (!exchange.getRequestMethod().equalsIgnoreCase("GET")) {
            send(exchange, 405, new JSONObject().put("status", "fail"));
            return;
        }

        try {
            String path = exchange.getRequestURI().getPath();
            String[] parts = path.split("/");

            if (parts.length < 3) {
                send(exchange, 400, new JSONObject().put("message", "User ID missing"));
                return;
            }

            String userId = parts[2];

            System.out.println("🔥 TRANSACTIONS API HIT for user: " + userId);

            TransactionService service = new TransactionService();
            List<Transaction> transactions = service.getAllTransactions();

            JSONArray arr = new JSONArray();

            for (Transaction t : transactions) {

                JSONObject obj = new JSONObject();

                obj.put("transactionId", t.getTransactionId());

                // 🔥 SAFE fallback (since type not directly available)
                obj.put("type", t.getClass().getSimpleName());

                obj.put("status", t.getStatus().name());

                // ⚠️ TEMP: skip user filtering (we'll fix later cleanly)
                arr.put(obj);
            }

            JSONObject res = new JSONObject();
            res.put("data", arr);

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