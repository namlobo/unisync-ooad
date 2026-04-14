package service;

import dao.interfaces.ReviewDAO;
import dao.impl.ReviewDAOImpl;
import model.review.Review;

import java.util.List;

public class ReviewService {

    private final ReviewDAO reviewDAO;

    public ReviewService() {
        this.reviewDAO = new ReviewDAOImpl();
    }

    public void submitReview(Review review) {

        if (review.getRating() < 1 || review.getRating() > 5) {
            throw new IllegalArgumentException("Rating must be between 1 and 5.");
        }

        reviewDAO.save(review);
    }

    public List<Review> getReviewsForResource(int resourceId) {
        return reviewDAO.findByResource(resourceId);
    }
}