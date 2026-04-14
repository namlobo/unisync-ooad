package dao.impl;

import dao.DBConnection;
import dao.interfaces.ResourceDAO;
import model.resource.*;
import model.user.Student;

import java.sql.*;
import java.util.*;

public class ResourceDAOImpl implements ResourceDAO {

    @Override
    public void save(Resource resource) {

        String sql = "INSERT INTO Resource (Title, Description, ItemCondition, Status, ListingType, OwnerId, CategoryId) VALUES (?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, resource.getTitle());
            ps.setString(2, resource.getDescription());
            ps.setString(3, resource.getCondition());
            ps.setString(4, resource.getStatus().name());
            ps.setString(5, resource.getListingType().name());
            ps.setString(6, resource.getOwner().getId());
            ps.setInt(7, resource.getCategory().getCategoryId());

            ps.executeUpdate();

            System.out.println("✅ Resource added successfully!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Optional<Resource> findById(int id) {

        String sql = "SELECT * FROM Resource WHERE ResourceId = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                return Optional.of(mapResource(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return Optional.empty();
    }

    @Override
    public List<Resource> findAvailableResources() {

        List<Resource> resources = new ArrayList<>();

        String sql = "SELECT * FROM Resource WHERE Status = 'AVAILABLE'";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement()) {

            ResultSet rs = stmt.executeQuery(sql);

            while (rs.next()) {
                resources.add(mapResource(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return resources;
    }

    @Override
    public void update(Resource resource) {

        String sql = "UPDATE Resource SET Title=?, Description=?, Status=? WHERE ResourceId=?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, resource.getTitle());
            ps.setString(2, resource.getDescription()); // ✅ FIXED
            ps.setString(3, resource.getStatus().name());
            ps.setInt(4, resource.getResourceId());

            ps.executeUpdate();

            System.out.println("✅ Resource updated!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void delete(int id) {

        String sql = "DELETE FROM Resource WHERE ResourceId=?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, id);
            ps.executeUpdate();

            System.out.println("✅ Resource deleted!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // 🔥 CLEAN MAPPING METHOD
    private Resource mapResource(ResultSet rs) throws SQLException {

        // Minimal dummy objects (for now — enough for demo)
        Student owner = new Student(
                rs.getString("OwnerId"),
                "Temp", "temp@email.com", "0000000000", "pass", "Dept"
        );

        Category category = new Category(
    rs.getInt("CategoryId"),
    "Temp",
    "Temp"
);

        return new Resource(
                rs.getInt("ResourceId"),
                rs.getString("Title"),
                rs.getString("Description"),
                rs.getString("ItemCondition"),
                ListingType.valueOf(rs.getString("ListingType")),
                owner,
                category
        );
    }
}