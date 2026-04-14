package api;

import com.sun.net.httpserver.*;
import service.ResourceService;
import model.resource.*;
import model.user.Student;
import org.json.JSONObject;

import java.io.*;

public class ResourceHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange exchange) throws IOException {

        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) return;

        String body = new BufferedReader(
                new InputStreamReader(exchange.getRequestBody())
        ).lines().reduce("", (a, b) -> a + b);

        JSONObject json = new JSONObject(body);

        String title = json.getString("title");
        String description = json.getString("description");
        String condition = json.getString("condition");
        String type = json.getString("type");
        String ownerId = json.getString("ownerId");
        int categoryId = json.getInt("categoryId");

        Resource resource = new Resource(
                0,
                title,
                description,
                condition,
                ListingType.valueOf(type),
                new Student(ownerId, "", "", "", "", ""),
                new Category(categoryId, "", "")
        );

        ResourceService service = new ResourceService();
        service.addResource(resource);

        JSONObject response = new JSONObject();
        response.put("status", "success");

        send(exchange, 200, response);
    }

    private void send(HttpExchange ex, int code, JSONObject res) throws IOException {
        ex.getResponseHeaders().add("Content-Type", "application/json");
        byte[] bytes = res.toString().getBytes();
        ex.sendResponseHeaders(code, bytes.length);
        ex.getResponseBody().write(bytes);
        ex.close();
    }
}