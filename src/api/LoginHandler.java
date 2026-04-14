package api;

import com.sun.net.httpserver.*;
import service.StudentService;
import model.user.Student;
import org.json.JSONObject;

import java.io.*;

public class LoginHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange exchange) throws IOException {

        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            send(exchange, 405, new JSONObject().put("status", "fail").put("message", "Method not allowed"));
            return;
        }

        try {
            String body = new BufferedReader(
                    new InputStreamReader(exchange.getRequestBody())
            ).lines().reduce("", (a, b) -> a + b);

            JSONObject json = new JSONObject(body);

            String email = json.getString("email");
            String password = json.getString("password");

            StudentService service = new StudentService();
            Student s = service.login(email, password);

            JSONObject response = new JSONObject();
            response.put("status", "success");
            response.put("srn", s.getId());
            response.put("name", s.getName());

            send(exchange, 200, response);

        } catch (Exception e) {
            JSONObject response = new JSONObject();
            response.put("status", "fail");
            response.put("message", "Invalid credentials");

            send(exchange, 401, response);
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