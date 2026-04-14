package dao.impl;

import dao.DBConnection;
import dao.interfaces.ReviewDAO;
import model.resource.Resource;
import model.review.Review;
import model.user.Student;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ReviewDAOImpl implements ReviewDAO {

    @Override
    public void save(Review review) {
        String sql = "INSERT INTO Review (ReviewId, Rating, Comment, ReviewerId, ResourceId) VALUES (?, ?, ?, ?, ?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, 0); // ReviewId auto-generated
            ps.setInt(2, review.getRating());
            ps.setString(3, review.getComment());
            ps.setString(4, "reviewer_id"); // Get from review object when fully implemented
            ps.setInt(5, 0); // ResourceId - get from review object

            ps.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public List<Review> findByResource(int resourceId) {
        List<Review> reviews = new ArrayList<>();
        String sql = "SELECT ReviewId, Rating, Comment, ReviewerId, ResourceId FROM Review WHERE ResourceId = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, resourceId);
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                int reviewId = rs.getInt("ReviewId");
                int rating = rs.getInt("Rating");
                String comment = rs.getString("Comment");
                String reviewerId = rs.getString("ReviewerId");
                int resId = rs.getInt("ResourceId");
            
            
                Student reviewer = null; 
                Resource resource = null; 
            
                Review review = new Review(reviewId, rating, comment, reviewer, resource);
                reviews.add(review);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return reviews;
    }
}