package api;

import com.sun.net.httpserver.*;
import org.json.JSONObject;
import service.TransactionService;

import java.io.*;

public class BorrowHandler implements HttpHandler {

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

            int resourceId = json.getInt("resourceId");
            String borrowerId = json.getString("borrowerId");
            String lenderId = json.getString("lenderId");
            String startDate = json.getString("startDate");
            String endDate = json.getString("endDate");

            TransactionService service = new TransactionService();

            // 👉 You should already have something like this
            service.createLendBorrowTransaction(
                    resourceId, lenderId, borrowerId, startDate, endDate
            );

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